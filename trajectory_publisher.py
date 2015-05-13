from collections import namedtuple

WheelbaseTrajectoryPoint = namedtuple('WheelbaseTrajectoryPoint',
                                      ['x', 'y', 'vx', 'vy', 'ax', 'ay'])
WheelbaseTrajectory = namedtuple('WheelbaseTrajectory',
                                 ['start', 'dt', 'points'])
TrajectoryPoint = namedtuple('TrajectoryPoint',
                             ['position', 'speed', 'torque'])
Trajectory = namedtuple('Trajectory', ['start', 'dt', 'points'])
Setpoint = namedtuple('Setpoint', ['value'])


class PositionSetpoint(Setpoint):
    pass


class SpeedSetpoint(Setpoint):
    pass


class TorqueSetpoint(Setpoint):
    pass


class TrajectoryPublisher():
    def __init__(self):
        self.trajectories = dict()

    def update_trajectory(self, name, newtraj):
        if name not in self.trajectories:
            self.trajectories[name] = newtraj

        elif isinstance(self.trajectories[name], WheelbaseTrajectory):
            if not isinstance(newtraj, WheelbaseTrajectory):
                raise ValueError("Wheelbase can only updated with Wheelbase")

        elif isinstance(newtraj, Setpoint):
            self.trajectories[name] = newtraj
