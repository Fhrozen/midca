#!/usr/bin/env python 
from MIDCA import base, rosrun
from MIDCA.modules import simulator, perceive, note, guide, evaluate, intend, planning, act
from MIDCA.modules._plan.asynch import asynch, operators_sr, methods_sr
from MIDCA.logging import Logger
import inspect, os
from std_msgs.msg import String
from MIDCA.examples._gazebo_baxter import Calibrate
from geometry_msgs.msg import Point, PointStamped


def ros_style_midca():
	myMidca = base.MIDCA(None, verbose = 2)
	for phase in ["Perceive", "Interpret", "Eval", "Intend", "Plan", "Act"]:
		myMidca.append_phase(phase)

	myMidca.append_module("Perceive", perceive.ROSObserver())
	myMidca.append_module("Interpret", guide.InstructionReceiver_sr())
	myMidca.append_module("Eval", evaluate.EvalPointingFromFeedback())
	myMidca.append_module("Intend", intend.SimpleIntend())
	myMidca.append_module("Plan", planning.AsynchPyhopPlanner(methods_sr.declare_methods, 
	operators_sr.declare_ops
	
	))
	myMidca.append_module("Act", act.AsynchronousAct())
	return myMidca
	
thisDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

MIDCA_ROOT = thisDir + "/../"

myMidca = ros_style_midca()

#myMidca.logger.logOutput()
#myMidca.mem.enableLogging(myMidca.logger)

# calibration


rosMidca = rosrun.RosMidca(myMidca, incomingMsgHandlers = [
	#rosrun.CalibrationHandler("calibrate_done", myMidca),
	rosrun.threeObjectsLocationHandler("obj_pos", myMidca),
	rosrun.UtteranceHandler("cmds_received", myMidca),
	rosrun.FeedbackHandler(rosrun.FEEDBACK_TOPIC, myMidca)],
	outgoingMsgHandlers = [rosrun.OutgoingMsgHandler(asynch.LOC_TOPIC, String), 
						rosrun.OutgoingMsgHandler(asynch.GRAB_TOPIC, String),
						rosrun.OutgoingMsgHandler(asynch.RELEASE_TOPIC, String),
						rosrun.OutgoingMsgHandler(asynch.RAISE_TOPIC, String)])

rosMidca.ros_connect()


H = Calibrate.calibrate()
#Z = -0.15113003072395247
#Z = -0.16113003072395247
Z=-0.147
myMidca.mem.set(myMidca.mem.CALIBRATION_MATRIX, H)
myMidca.mem.set(myMidca.mem.CALIBRATION_Z, Z)
#myMidca.mem.set(myMidca.mem.STACK_Z, 0.018148563732166244)
myMidca.mem.set(myMidca.mem.STACK_Z, -0.108833784354784)
myMidca.mem.set(myMidca.mem.STACK_3Z, 0.01517833784354784)
myMidca.mem.set(myMidca.mem.UNSTACK_Z, -0.11434523370125365)
myMidca.mem.set(myMidca.mem.UNSTACK_3Z, -0.05434523370125365)

p = Point(x = 0.5682, y =  0.1829 , z = 0.2256)
#p = 
myMidca.mem.set(myMidca.mem.RAISING_POINT, p)
#0.6754473650020971, 0.3487005600746112
#q = Point(x = 0.6754473650020971, y =   0.3487005600746112, z = -0.14113003072395247)
#q = Point(x = 0.7596311811530513, y =   0.09691300804254104, z = -0.14113003072395247)
#lab_q =Point(0.7450848313136519, 0.11634406023548731, -0.15821251824917773)
q = Point(0.69, 0.01967133208903987, -0.145)
myMidca.mem.set(myMidca.mem.PUTTING_POINT, q)


raw_input('Enter ...')
rosMidca.run_midca()
