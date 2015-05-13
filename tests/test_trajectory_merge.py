import unittest
from trajectory_publisher import *


class TrajectoryMergingTestCase(unittest.TestCase):
    def test_can_merge_trajectory(self):
        """
        Simple check that we can merge a second trajectory overlapping with the
        first (most common case.
        """
        dt = 0.1
        first = Trajectory(1., dt, (1, 2, 3))
        second = Trajectory(1. + dt, dt, (10, 20, 30))

        res = trajectory_merge(first, second)
        self.assertEqual(res, Trajectory(1., dt, (1, 10, 20, 30)))

    def test_can_merge_trajectory_before(self):
        """
        This test checks that having a second trajectory starting before the
        start of the first one works as expected.
        """
        dt = 0.1
        first = Trajectory(1., dt, (1, 2, 3))
        second = Trajectory(1. - dt, dt, (10, 20, 30))
        res = trajectory_merge(first, second)
        self.assertEqual(res, Trajectory(1. - dt, dt, (10, 20, 30)))

    def test_wrong_dt_trajectories(self):
        """
        Checks that we raise the correct error when merging two trajectories
        whose dt don't match.
        """
        first = Trajectory(0., 1., tuple())
        second = Trajectory(0., 2., tuple())

        with self.assertRaises(ValueError):
            trajectory_merge(first, second)

    def test_after_end(self):
        """
        Checks that we correctly repeat the last point of the first trajectory
        as padding until the start of the second one if needed.
        """
        first = Trajectory(0., 0.5, (1, 2, 3))
        second = Trajectory(3., 0.5,  (10, 20, 30))

        res = trajectory_merge(first, second)

        self.assertEqual(res.start, 0.)
        self.assertEqual(res.dt, 0.5)
        padding = (3, 3, 3)
        self.assertEqual(res.points, first.points + padding + second.points)
