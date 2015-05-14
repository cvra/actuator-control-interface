import unittest
from trajectory_publisher import *


class TrajectoryGarbageCollectorTestCase(unittest.TestCase):
    dt = 0.5

    def test_simple_gc(self):
        traj = Trajectory(0., self.dt, (1, ) * 10)
        traj = trajectory_gc(traj, 2.)
        expected = Trajectory(2., self.dt, (1, ) * 6)
        self.assertEqual(traj.dt, expected.dt)
        self.assertEqual(traj.start, expected.start)
        self.assertEqual(traj.points, expected.points)

    def test_no_gc(self):
        traj = Trajectory(0., self.dt, (1, ) * 10)
        traj2 = trajectory_gc(traj, -1)

        self.assertEqual(traj, traj2)

    def test_gc_wheelbase_trajectory(self):
        traj = WheelbaseTrajectory(0., dt=0.5, points=(1, 2, 3, 4))
        traj = trajectory_gc(traj, 1.)
        self.assertIsInstance(traj, WheelbaseTrajectory)
        self.assertEqual(traj, WheelbaseTrajectory(1., 0.5, (3, 4)))


