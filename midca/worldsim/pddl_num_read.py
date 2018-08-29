# source: https://github.com/hfoffani/pddl-lib
# https://github.com/karpase/pythonpddl
#
# I ran this using Python 3.6 and ubuntu
# this script might not work on windows.

# install pip3
# python3.6 -m pip install


#
# pip3 install antlr4-python3-runtime
# clone https://github.com/karpase/pythonpddl
# follow the steps in the the link above

import midca.worldsim.worldsim as worldsim

from midca.worldsim import pddl
from midca.worldsim.pddl import FExpression, FHead, ConstantNumber, Formula, Predicate
import inspect, os

types = {"obj": worldsim.Type("obj", [])}
# types = {"thing": worldsim.Type("thing", [])}
objects = {}
predicates = {}
atoms = []
operators = {}
cltree = {"rootnode": "", "allnodes": [], "checked": []}
obtree = {"rootnode": "", "allnodes": [], "checked": []}
functions = {}
constants = []
# hidden = ["thing-at-loc"] #the predicates that are hidden from the agent
hidden = []

def load_domain(domainfile, problemfile):
    (dom, prob) = pddl.parseDomainAndProblem(domainfile, problemfile)

    # for a in dom.actions:
    #     for b in [False, True]:
    #            print(a.name, "c", b, list(map(lambda x: x.asPDDL(), a.get_pre(b))))
    #     for b in [False, True]:
    #            print(a.name, "e", b, list(map(lambda x: x.asPDDL(), a.get_eff(b))))

    # print("DOMAIN PROBLEM")
    # print("objects")
    ###############types#########################
    # print('types: ')

    for arg in dom.types.args:
        if arg.arg_type:
            if arg.arg_type not in types:
                wtype(arg.arg_type)
            wtype(arg.arg_name, arg.arg_type)
        else:
            wtype(arg.arg_name)


    # for t in types:
    #     for p in types[t].parents:
    #         print(p.__repr__())

    # print("Objects:")
    objects = parseObjects(prob.objects)
    ###Predicates##########
    # print('predicates: ')
    for a in dom.predicates:
        argnames = parseTypedArgList_names(a.args)
        predicate(a.name, argnames, a.args)

    # print('functions')
    for a in dom.functions:
        # print(a.name)
        argnames = parseTypedArgList_names(a.args)
        argtypes = parseTypedArgList_types_predicate(a.args)
        functions.update({a.name: worldsim.Function(a.name, argnames, argtypes)})

    # print('constants')
    for c in dom.constants.args:
        # print(c.val)
        constants.append(worldsim.Constant(c.val))
    ######### OPERATORS ####################

    # print('actions:')
    for a in dom.actions:
        actions_args = parseTypedArgList(a.parameters)

        prepredicatesfunc = []
        postpredicatesfunc = []
        prepredicates = []
        postpredicates = []
        preobjnames = []
        postobjnames = []
        preobjtypes = []
        postobjtypes = []
        prepos = []
        postpos = []
        prefunnames = []
        postfuncnames = []
        prefuntypes = []
        postfunctypes = []
        prefuncpos = []
        postfuncpos = []
        for pre in a.get_pre(True):

            # a.args is typedArgList
            if type(pre) is Formula:
                # print(pre.asPDDL())
                args = []
                tempargs = []
                temptypes = []
                for sub in pre.subformulas:

                    if type(sub) is Predicate:  # when it is a negate predicate#
                        prepos.append(True)
                        name, argnames, argtypes = parsePredicate(sub, actions_args)

                        prepredicates.append(worldsim.Predicate(name, argnames, argtypes))

                        preobjnames.append(argnames)
                        preobjtypes.append(argtypes)

                    elif type(sub) is FHead:

                        argnames = parseTypedArgList_names(sub.args)
                        argtypes = parseTypedArgList_types(sub.args, actions_args)

                        tempargs.append(argnames)
                        temptypes.append(argtypes)
                        args.append(functions[sub.name])
                    else:
                        args.append(sub.val)

                if args:
                    prefuncpos.append(True)
                    prefunnames.append(tempargs)
                    prefuntypes.append(temptypes)
                    prepredicatesfunc.append(worldsim.Predicate_function(pre.op, args))

            elif type(pre) is Predicate:
                pre.name, pre_args_name, pre_args_type = parsePredicate(pre, actions_args)
                prepredicates.append(worldsim.Predicate(pre.name, pre_args_name, pre_args_type))
                prepos.append(True)
                preobjnames.append(pre_args_name)
                preobjtypes.append(pre_args_type)
                # if "shelter" in pre_args_name:
                #     print(pre.name)
                #     for t in preobjtypes:
                #         for x in t:
                #             print(x.__str__())

        for pre in a.get_pre(False):

            if type(pre) is Formula:
                args = []
                tempargs = []
                temptypes = []
                for sub in pre.subformulas:

                    if type(sub) is Predicate:  # when it is a negate predicate#
                        name, argnames, argtypes = parsePredicate(sub, actions_args)
                        prepos.append(False)
                        prepredicates.append(worldsim.Predicate(name, argnames, argtypes))

                        preobjnames.append(argnames)
                        preobjtypes.append(argtypes)

                    elif type(sub) is FHead:

                        argnames = parseTypedArgList_names(sub.args)
                        argtypes = parseTypedArgList_types(sub.args, actions_args)

                        tempargs.append(argnames)
                        temptypes.append(argtypes)
                        args.append(functions[sub.name])
                    else:
                        args.append(sub.val)

                if args:
                    prefuncpos.append(False)
                    prefunnames.append(tempargs)
                    prefuntypes.append(temptypes)
                    prepredicatesfunc.append(worldsim.Predicate_function(pre.op, args))

            elif type(pre) is Predicate:
                pre.name, pre_args_name, pre_args_type = parsePredicate(pre, actions_args)

                prepredicates.append(worldsim.Predicate(pre.name, pre_args_name, pre_args_type))
                prepos.append(False)
                preobjnames.append(pre_args_name)
                preobjtypes.append(pre_args_type)

        for eff in a.get_eff(True):

            if type(eff) is Formula:
                args = []
                tempargs = []
                temptypes = []
                for sub in eff.subformulas:

                    if type(sub) is Predicate:  # when it is a negate predicate#
                        name, argnames, argtypes = parsePredicate(sub, actions_args)

                        postpredicates.append(worldsim.Predicate(name, argnames, argtypes))
                        postpos.append(True)
                        postobjnames.append(argnames)
                        postobjtypes.append(argtypes)

                    elif type(sub) is FHead:

                        argnames = parseTypedArgList_names(sub.args)
                        argtypes = parseTypedArgList_types(sub.args, actions_args)

                        tempargs.append(argnames)
                        temptypes.append(argtypes)
                        args.append(functions[sub.name])
                    else:
                        args.append(sub.val)

                if args:
                    postfuncpos.append(True)
                    postfuncnames.append(tempargs)
                    postfunctypes.append(temptypes)
                    postpredicatesfunc.append(worldsim.Predicate_function(eff.op, args))

            elif type(eff) is Predicate:
                # a.args is typedArgList
                postpos.append(True)
                eff.name, eff_args_name, eff_args_type = parsePredicate(eff, actions_args)
                postpredicates.append(worldsim.Predicate(eff.name, eff_args_name, eff_args_type))
                postobjnames.append(eff_args_name)
                postobjtypes.append(eff_args_type)
                # print(eff_args_name)

        for eff in a.get_eff(False):
            if type(eff) is Formula:
                args = []
                tempargs = []
                temptypes = []
                for sub in eff.subformulas:

                    if type(sub) is Predicate:  # when it is a negate predicate#
                        name, argnames, argtypes = parsePredicate(sub, actions_args)

                        postpredicates.append(worldsim.Predicate(name, argnames, argtypes))
                        postpos.append(False)
                        postobjnames.append(argnames)
                        postobjtypes.append(argtypes)

                    elif type(sub) is FHead:

                        argnames = parseTypedArgList_names(sub.args)
                        argtypes = parseTypedArgList_types(sub.args, actions_args)

                        tempargs.append(argnames)
                        temptypes.append(argtypes)
                        args.append(functions[sub.name])
                    else:
                        args.append(sub.val)

                if args:
                    postfuncpos.append(False)
                    postfuncnames.append(tempargs)
                    postfunctypes.append(temptypes)
                    postpredicatesfunc.append(worldsim.Predicate_function(eff.op, args))

            elif type(eff) is Predicate:
                postpos.append(False)
                eff.name, eff_args_name, eff_args_type = parsePredicate(eff, actions_args)
                postpredicates.append(worldsim.Predicate(eff.name, eff_args_name, eff_args_type))
                postobjnames.append(eff_args_name)
                postobjtypes.append(eff_args_type)
                # print(eff_args_name)

        operators.update({a.name: worldsim.Operator(a.name, list(actions_args.keys()), prepredicates, preobjnames,
                                                    preobjtypes, prepos,
                                                    postpredicates, postobjnames, postobjtypes, postpos,
                                                    prepredicatesfunc, prefunnames, prefuntypes, postpredicatesfunc, postfuncnames, postfunctypes, prefuncpos, postfuncpos)})


    world = worldsim.World(list(operators.values()), list(predicates.values()), atoms, types, list(objects.values()),list(functions.values()),
                           cltree, obtree)
    # print(world.functions)
    _apply_state_pddl(world, prob)

    # for t in worldsim.func_val_dict:
    #     print(t)
    # print("++++++++++++++++++++++++++++++++++++++++++")
    return world

    # probinitialState = getInitialState(prob.initialstate)


def parsePredicate(pre, actions_args):
    args_names = parseTypedArgList_names(pre.args)
    args_types = parseTypedArgList_types(pre.args, actions_args)
    # print(pre.name)

    return pre.name, args_names, args_types


def parseFormula(a, actions_args):
    # print("formula::::::::")
    # print(a.asPDDL())
    for sub in a.subformulas:
        # print(a.op)
        if type(sub) is Predicate:  # when it is a negate predicate#
            name, argnames, argtypes = parsePredicate(sub, actions_args)

        elif type(sub) is FHead:
            print()


def _apply_state_pddl(world, prob):
    # print("here....................................")

    for a in prob.initialstate:
        """ FExpression: represents a functional / numeric expression"""
        '''Formula: represented a goal description (atom / negated atom / and / or)'''
        '''subformulas is a predicate'''
        if type(a) is FExpression:
            # print("feexpression")
            # print(a.op)
            func = None
            val = None
            func_args = []

            for sub in a.subexps:
                """FHead: represents a functional symbol and terms, e.g.,  (f a b c) (name, args)"""

                if type(sub) is FHead:
                    # print(sub.name)
                    func = sub.name
                    func_args = parseTypedArgList_names(sub.args)
                    # for f in func_args:
                    #     print(f)
                else:
                    # print(sub.val)
                    val = sub.val

            if a.op == "=":
                args = []
                for name in func_args:
                    if not name:
                        continue
                    if name not in world.objects:
                        raise Exception(": Object - " + name + " DNE ")
                    args.append(world.objects[name])
                if not (func in world.functions):
                    raise Exception(func)

                atom = world.functions[func].instantiate(args, val)
                worldsim.func_val_dict.update({atom: val})
                world.add_atom(atom)
        else:

            for sub in a.subformulas:
                call = sub.name
                # print(call)
                argnames = parseTypedArgList_names(sub.args)
                negate = False
                if call in world.predicates:
                    args = []
                    for name in argnames:
                        if not name:
                            continue
                        if name not in world.objects:
                            raise Exception(": Object - " + name + " DNE ")
                        args.append(world.objects[name])

                    atom = world.predicates[call].instantiate(args)
                    if not (call in hidden):
                        if negate:
                            world.remove_atom(atom)
                        else:
                            world.add_atom(atom)
                        # print(atom.__str__())


# def getInitialState(probinitialState):
#     for a in probinitialState:
#         if type(a) is FExpression:
#             # print("feexpression")
#             # print(a.op)
#             for sub in a.subexps:
#                 if type(sub) is FHead:
#                     print(sub.name)
#                     print(parseTypedArgList_names(sub.args))
#                 else:
#                     print(sub.val)
#
#         else:
#             print("formula")
#             print(a.op)
#             for sub in a.subformulas:
#                 print(sub)
#                 print(sub.name)
#                 print(parseTypedArgList_names(sub.args))
#         # goal = prob.goal
#         # print(goal)


def instance(name, typename):
    if typename not in types:
        raise Exception("object type DNE.")
    objects[name] = types[typename].instantiate(name)


def wtype(name, parentnames=["obj"]):
    temp = [name]
    if not parentnames == ["obj"]:
        temp.append(parentnames)
    if isinstance(parentnames, str):
        parentnames = [parentnames]
    parents = []
    for parent in parentnames:
        if parent not in types:
            raise Exception("parent type DNE.")
        parents.append(types[parent])
    types[name] = worldsim.Type(name, parents)
    otree = worldsim.ObjectTree(obtree['rootnode'],
                                obtree['allnodes'],
                                obtree['checked'],
                                temp)
    obtree['rootnode'] = otree.rootnode
    obtree['allnodes'] = otree.allnodes
    obtree['checked'] = otree.checked


def parseObjects(objects):
    worldsimObjects = {}
    for arg in objects.args:
        worldsimObjects.update({arg.arg_name: worldsim.Obj(arg.arg_name, types[arg.arg_type])})

    return worldsimObjects


def pasrsPredicate(dompredicates):
    parsed = []
    for a in dompredicates:
        # a.args is typedArgList
        predicate_args = parseTypedArgList_names(a.args)
        parsed.append(a.name + " " + predicate_args)
    return parsed


def parseTypedArgList(argList):
    parsed = {}
    for arg in argList.args:
        if arg.arg_type in types:
            parsed.update({arg.arg_name: types[arg.arg_type]})
        else:
            parsed.update({arg.arg_name: types["resource"]})
    return parsed


def parseTypedArgList_names(argList):
    parsed = []
    for arg in argList.args:
        n = objects
        parsed.append(str(arg.arg_name))
    return parsed

def parseTypedArgList_ground_names(argList):
    parsed = []
    for arg in argList.args:
        n = objects[arg.arg_name]
        parsed.append(n)
    return parsed

def predicate(name, argnames, argList):
    argtypes = []
    for arg in argList.args:
        if arg.arg_type not in types:
            argtypes.append(types["resource"])
        else:
            argtypes.append(types[arg.arg_type])

    predicates[name] = worldsim.Predicate(name, argnames, argtypes)
    # for t in predicates[name].argtypes:
    #     print(t.__str__())


def parseTypedArgList_types_predicate(argList):
    ptypes = []
    for arg in argList.args:
        if arg.arg_type in types.keys():
            ptypes.append(types[arg.arg_type])
        else:

            ptypes.append(types["resource"])

    return ptypes


def parseTypedArgList_types(argList, action_types):
    ptypes = []
    for arg in argList.args:
        if arg.arg_name in action_types.keys():
            ptypes.append(action_types[arg.arg_name])
        else:
            ptypes.append(types["resource"])

    return ptypes


def test(a, actions_args):
    for eff in a.get_pre(False):
        func = None
        val = None
        if type(eff) is Formula:
            for sub in eff.subformulas:
                print(eff.op)
                if type(sub) is Predicate:  # when it is a negate predicate#
                    name, argnames, argtypes = parsePredicate(sub, actions_args)

                elif type(sub) is FHead:
                    print("________")
                    print(sub.name)
                    if index == 1:
                        func = functions[sub.name]
                    else:
                        val = functions[sub.name]
                    print("__________________")
                else:
                    val = sub.val
                    print(sub.val)

                worldsim.Predicate_function(eff.name, eff.op, func, val)


if __name__ == "__main__":
    thisDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    MIDCA_ROOT = thisDir + "/../"

    ### Domain Specific Variables for JSHOP planner
    ff_DOMAIN_FILE = MIDCA_ROOT + "domains/ffdomain/minecraft/test.pddl"
    ff_STATE_FILE = MIDCA_ROOT + "domains/ffdomain/minecraft/wood.75.pddl"

    load_domain(ff_DOMAIN_FILE, ff_STATE_FILE)
