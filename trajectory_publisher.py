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


def trajectory_merge(first, second):
    if first.dt != second.dt:
        raise ValueError("Can only merge trajectories with same samplerate.")

    dt = first.dt

    # Small helper function to convert second to a discreet number of samples
    seconds_to_samples = lambda t: int(t / dt)

    start_index = seconds_to_samples(second.start - first.start)

    # Repeat last point of first trajectory until the start of the second
    padding_len = second.start - (first.start + dt * len(first.points))
    padding = first.points[-1:] * seconds_to_samples(padding_len)

    points = first.points[:start_index] + padding + second.points

    start = min(first.start, second.start)

    return Trajectory(start, first.dt, points)

