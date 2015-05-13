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

