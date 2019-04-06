from midca import plans, base



class WaypointPlanner(base.BaseModule):

    """
    The challenge is to survey the Qroute and remove the maximum mines to provide safe passage to the ships.
    
    input : Two dictionaries "remus_location" and "hazard_location" which gives information about the submarine and the mines detected

            remus_location format:
                        remus_location =  {"X": x,
                                           "Y": y,
                                           "speed": speed,
                                           "direction": speed})
                        x and y are the location coordinates
                        speed is the velocity with which the remus is heading towards
                        ignore direction

            hazard_location format:
                        hazard_location =  {"X": mine_x,
                                            "Y": mine_y}
                        x and y are the location coordinates of the mine

    output : The list "way_point" to make the remus go to certain way_points
             way_point format:
                    way_point = [ [2,2],
                                  [3,3]]
    """


    def init(self, world, mem):
        """
        This is executed during the initialization of midca.
        Feel free to create any number of variables to store information
        """
        self.world = world
        self.mem = mem
        self.previous_way_points = []

    def get_remus_location(self):
        """

        :return: the dictionary of remus location
        """
        return self.mem.get(self.mem.REMUS_LOCATION)


    def get_mine_location(self):
        """

        :return: the dictionary of mine location
        """

        return self.mem.get(self.mem.HAZARD_LOCATION)


    def sample_behavior(self):
        """

        :return: a list of way_points
        """
        #way_points = [[-16, -8], [-17, -142],
        #              [92, -144], [89, -7],
        #              [216, -5], [195, -138]
        #              ]
        way_points = [[52,2], [20,-1],
                      [18,-39], [53,-29],
                      [69,-45], [103,-55],
                      [101,-95], [57,-91],
                      [57,-55], [80,-141],
                      [141,-97], [198, -59]]

        return way_points

    def set_way_points(self,way_points):
        """

        :param way_points: the list of way_points
         sets the memory variable "WAY_POINTS"
        """
        if self.previous_way_points == way_points:
                return

        self.mem.set(self.mem.WAY_POINTS, way_points)
        self.previous_way_points = way_points
   
    def run(self, cycle, verbose=2):
        """
        run function is executed in a cyclic fashion
        """

        remus_location = self.get_remus_location()
        hazard_location = self.get_mine_location()

        way_points = self.sample_behavior()

        """
        Your Code should start here
        """

        self.set_way_points(way_points)