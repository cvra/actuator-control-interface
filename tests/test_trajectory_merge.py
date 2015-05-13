import unittest
from trajectory_publisher import *


class TrajectoryMergingTestCase(unittest.TestCase):
    def test_can_merge_trajectory(self):
        dt = 0.1
        first = Trajectory(1., dt, (1, 2, 3))
        second = Trajectory(1. + dt, dt, (10, 20, 30))

        res = trajectory_merge(first, second)
        self.assertEqual(res, Trajectory(1., dt, (1, 10, 20, 30)))

    def test_can_merge_trajectory_before(self):
        dt = 0.1
        first = Trajectory(1., dt, (1, 2, 3))
        second = Trajectory(1. - dt, dt, (10, 20, 30))
        res = trajectory_merge(first, second)
        self.assertEqual(res, Trajectory(1. - dt, dt, (10, 20, 30)))
