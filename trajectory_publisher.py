from collections import namedtuple
from threading import Lock
import time

WheelbaseTrajectoryPoint = namedtuple('WheelbaseTrajectoryPoint',
                                      ['x', 'y', 'vx', 'vy', 'ax', 'ay'])
WheelbaseTrajectory = namedtuple('WheelbaseTrajectory',
                                 ['start', 'dt', 'points'])
TrajectoryPoint = namedtuple('TrajectoryPoint',
                             ['position', 'speed', 'torque'])

class Trajectory(namedtuple('Trajectory', ['start', 'dt', 'points'])):
    @classmethod
    def from_setpoint(cls, point, start, dt, duration):
        if isinstance(point, PositionSetpoint):
            point = TrajectoryPoint(point.value, 0, 0)
        elif isinstance(point, SpeedSetpoint):
            point = TrajectoryPoint(0, point.value, 0)
        elif isinstance(point, TorqueSetpoint):
            point = TrajectoryPoint(0, 0, point.value)

        length = int(duration / dt)

        return cls(start=start, dt=dt, points=(point, ) * length)


Setpoint = namedtuple('Setpoint', ['value'])

class PositionSetpoint(Setpoint):
    pass


class SpeedSetpoint(Setpoint):
    pass


class TorqueSetpoint(Setpoint):
    pass


def update_trajectory(trajectories, name, newtraj):
    """
    Update the trajectories dictionnary with the given new traj.
    """
    if name not in trajectories:
        trajectories[name] = newtraj
        return

    oldtraj = trajectories[name]

    if isinstance(oldtraj, WheelbaseTrajectory):
        # If the old setpoint is a trajectory for the wheelbase, we can
        # only merge it if the new trajectory is made for the wheelbase.
        if not isinstance(newtraj, WheelbaseTrajectory):
            raise ValueError("Wheelbase can only updated with Wheelbase")

        trajectories[name] = trajectory_merge(oldtraj, newtraj)

    elif isinstance(newtraj, Setpoint):
        # If the new trajectory is a setpoint, apply it immediately.
        # The motor board will generate a ramp
        trajectories[name] = newtraj

    elif isinstance(oldtraj, Trajectory):
        # If the old was a trajectory, simply merge it
        trajectories[name] = trajectory_merge(oldtraj, newtraj)

    elif isinstance(oldtraj, Setpoint):
        # Finally, if the old was a setpoint, convert it into a trajectory,
        # then merge it
        start = time.time()
        oldtraj = Trajectory.from_setpoint(oldtraj, start, newtraj.dt,
                                           newtraj.start - start)
        trajectories[name] = trajectory_merge(oldtraj, newtraj)


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


def trajectory_gc(trajectory, date):
    """
    Frees up memory by deleting the part of trajectory after the given date.
    """

    skipped_points = int((date - trajectory.start) / trajectory.dt)
    skipped_points = max(0, skipped_points)
    date = max(date, trajectory.start)

    return Trajectory(date, trajectory.dt, trajectory.points[skipped_points:])


def trajectory_to_chunks(traj, chunk_length):
    TrajType = type(traj)
    for i in range(0, len(traj.points), chunk_length):
        yield TrajType(traj.start + traj.dt * i,
                       traj.dt,
                       traj.points[i:i+chunk_length])


class TrajectoryPublisher:
    def __init__(self):
        self.trajectories = {}
        self.lock = Lock()

    def update_trajectory(self, name, newtraj):
        with self.lock:
            update_trajectory(self.trajectories, name, newtraj)
