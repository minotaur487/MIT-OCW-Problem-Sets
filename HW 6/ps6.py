# Problem Set 6: Simulating robots
# Name:
# Collaborators:
# Time:

import math
import random

import ps6_visualize
import pylab


# === Provided classes

class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """

    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: float representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)


# === Problems 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    cleanTiles = []  # Using a dict to make sure I don't get duplicate tiles

    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        x = pos.getX()
        y = pos.getY()
        if y >= self.height:
            y -= 1
        elif y <= 0:
            y += 1
        if x >= self.width:
            x -= 1
        elif x <= 0:
            x += 1
        self.cleanTiles.append((math.floor(x), math.floor(y)))
        self.cleanTiles = list(set(self.cleanTiles))

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        if (math.floor(m), math.floor(n)) in self.cleanTiles:
            return True
        return False

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return len(self.cleanTiles)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return Position(random.randrange(self.width), random.randrange(self.height))

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return 0 <= pos.getX() <= self.width and 0 <= pos.getY() <= self.height


class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """

    # int(random.random()*360)

    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.r_direction = random.randrange(0, 360)
        self.r_position = self.room.getRandomPosition()
        self.room.cleanTileAtPosition(self.r_position)

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.r_position

    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.r_direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.r_position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.r_direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the raise passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError


# === Problem 2
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current direction; when
    it hits a wall, it chooses a new direction randomly.
    """
    # def positioning(self, x, y, speed, angle):
    #
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # has room and speed in attributes of robot
        speed = 0.0
        speed_timer = 0.0
        robot_position = None
        while speed_timer < self.speed:
            # print('speed incr of UPC', speed)
            y = self.getRobotPosition().getY()
            x = self.getRobotPosition().getX()
            if self.room.isTileCleaned(int(x), int(y)) is False:
                self.room.cleanTileAtPosition(self.r_position)
            robot_position = Position(x, y)
            robot_position = robot_position.getNewPosition(self.r_direction, speed)
            # print('y', robot_position.getY())
            # print('x', robot_position.getX())
            speed += 0.01
            speed_timer += 0.01
            cy = robot_position.getY()
            cx = robot_position.getX()
            if cy <= 0:
                self.setRobotPosition(Position(robot_position.getX(),0))
                self.r_direction = random.randrange(360)
                speed = 0.01
            elif cy >= self.room.height:
                self.setRobotPosition(Position(robot_position.getX(), self.room.height))
                self.r_direction = random.randrange(360)
                speed = 0.01
            if cx <= 0:
                self.setRobotPosition(Position(0, robot_position.getY()))
                self.r_direction = random.randrange(360)
                speed = 0.01
            elif cx >= self.room.width:
                self.setRobotPosition(Position(self.room.width, robot_position.getY()))
                self.r_direction = random.randrange(360)
                speed = 0.01
        # print(type(robot_position))
        self.setRobotPosition(robot_position)


# === Problem 3

def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. Robot or
                RandomWalkRobot)
    """

    visualize = False
    total_time_steps = 0.0
    for trial in range(num_trials):
        if visualize:
            anim = ps6_visualize.RobotVisualization(num_robots, width, height)
        room = RectangularRoom(width, height)
        robotCollection = []
        for i in range(num_robots):
            robotCollection.append(robot_type(room, speed))
        if visualize:
            anim.update(room, robotCollection)
        while (room.getNumCleanedTiles() / float(room.getNumTiles())) < min_coverage:
            for robot in robotCollection:
                robot.updatePositionAndClean()
            total_time_steps += 1
            if visualize:
                anim.update(room, robotCollection)
        if visualize:
            anim.done()
        print(trial)
    return total_time_steps / num_trials

class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random after each time-step.
    """
    def updatePositionAndClean(self):
        cur_pos = self.getRobotPosition()
        cur_dir = self.getRobotDirection()
        self.setRobotDirection(random.randrange(360))
        new_pos = cur_pos.getNewPosition(cur_dir, self.speed)
        if self.room.isPositionInRoom(new_pos):
            self.setRobotPosition(new_pos)
            self.room.cleanTileAtPosition(new_pos)
        # speed = 0.0
        # speed_timer = 0.0
        # robot_position = None
        # while speed_timer < self.speed:
        #     # print('speed incr of UPC', speed)
        #     y = self.getRobotPosition().getY()
        #     x = self.getRobotPosition().getX()
        #     if self.room.isTileCleaned(int(x), int(y)) is False:
        #         self.room.cleanTileAtPosition(self.r_position)
        #     robot_position = Position(x, y)
        #     robot_position = robot_position.getNewPosition(self.r_direction, speed)
        #     # print('y', robot_position.getY())
        #     # print('x', robot_position.getX())
        #     speed += 0.01
        #     speed_timer += 0.01
        #     cy = robot_position.getY()
        #     cx = robot_position.getX()
        #     if cy <= 0:
        #         self.setRobotPosition(Position(robot_position.getX(), 0))
        #         self.r_direction = random.randrange(0, 360)
        #         speed = 0.01
        #     elif cy >= self.room.height:
        #         self.setRobotPosition(Position(robot_position.getX(), self.room.height))
        #         self.r_direction = random.randrange(0, 360)
        #         speed = 0.01
        #     if cx <= 0:
        #         self.setRobotPosition(Position(0, robot_position.getY()))
        #         self.r_direction = random.randrange(0, 360)
        #         speed = 0.01
        #     elif cx >= self.room.width:
        #         self.setRobotPosition(Position(self.room.width, robot_position.getY()))
        #         self.r_direction = random.randrange(0, 360)
        #         speed = 0.01
        # # print(type(robot_position))
        # self.setRobotDirection(random.randrange(0, 360))
        # self.setRobotPosition(robot_position)

# === Problem 4
#
# 1) How long does it take to clean 80% of a 20�20 room with each of 1-10 robots?
#
# 2) How long does it take two robots to clean 80% of rooms with dimensions 
#	 20�20, 25�16, 40�10, 50�8, 80�5, and 100�4?

def showPlot1():
    """
    Produces a plot showing dependence of cleaning time on number of robots.
    """
    xAxis = []
    yAxis = []
    for num_r in range(1, 11):
        xAxis.append(num_r)
        yAxis.append(runSimulation(num_r, 1.0, 20, 20, .8, 25, StandardRobot))
    pylab.title('Plot 1')
    pylab.xlabel('Number of Robots')
    # pylab.semilogy()
    pylab.ylabel('Mean Time')
    pylab.plot(xAxis, yAxis)
    pylab.show()

# showPlot1()

def showPlot2(title, x_label, y_label):
    """
    Produces a plot showing dependence of cleaning time on room shape.
    """
    # aspect_ratios = []
    # times1 = []
    # times2 = []
    # for width in [40, 20, 25, 50, 80, 100]:
    #     height = int(400 / width)
    #     print("Plotting cleaning time for a room of width:", width, "by height:", height)
    #     aspect_ratios.append(float(width) / height)
    #     times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
    #     # print('d')
    #     # times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    # pylab.plot(aspect_ratios, times1)
    # print(times1)
    # # pylab.plot(aspect_ratios, times2)
    # # print(times2)
    #
    # pylab.title(title)
    # pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    # pylab.xlabel(x_label)
    # pylab.ylabel(y_label)
    # pylab.show()
    num_r = 2
    room_size = [(20, 20), (25, 16), (40, 10), (50, 8), (80, 5), (100, 4)]
    yAxis = []
    # yAxis2 = []
    xAxis = []
    for size in room_size:
        yAxis.append(runSimulation(num_r, 1.0, size[0], size[1], 0.8, 100, StandardRobot))
        xAxis.append(size[0]/size[1])
        # yAxis2.append(runSimulation(2, 1.0, size[0], size[1], 0.8, 200, RandomWalkRobot))
    # pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.ylabel('Mean Time')
    pylab.xlabel('Ratio of Width to Height')
    pylab.title('Plot 2')
    print(yAxis)
    # pylab.plot(xAxis, yAxis2)
    pylab.plot(xAxis, yAxis)
    pylab.show()

# === Problem 5


# print('result', runSimulation(1, 1.0, 10, 10, 0.9, 100, StandardRobot))

# === Problem 6

# For the parameters tested below (cleaning 80% of a 20x20 square room),
# RandomWalkRobots take approximately twice as long to clean the same room as
# StandardRobots do.
def showPlot3():
    """
    Produces a plot comparing the two robot strategies.
    """
    min_cov = 0.9
    num_bots = 1
    trials = 100
    room_sizes = [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (10, 10)]
    speed = 1.0
    r_yAxis = []
    s_yAxis = []
    xAxis = [x[0]*x[1] for x in room_sizes]
    for x in room_sizes:
        r_yAxis.append(runSimulation(num_bots, speed, x[0], x[1], min_cov, trials, RandomWalkRobot))
        s_yAxis.append(runSimulation(num_bots, speed, x[0], x[1], min_cov, trials, StandardRobot))

    # Random Walk
    # Standard Walk

    pylab.title('Random Walk vs. Standard Walk')
    pylab.xlabel('Area of Room')
    pylab.ylabel('Mean Time')
    pylab.plot(xAxis, s_yAxis, 'b^', label='standard')
    pylab.plot(xAxis, r_yAxis, 'g--', label='random')
    pylab.legend()
    pylab.show()

# showPlot3()
showPlot2('Time to clean 80% of a 400-tile room for various room shapes',
              'Aspect Ratio',
              'Time / steps')