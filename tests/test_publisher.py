import unittest
from trajectory_publisher import *

class TrajectoryPublisherTestCase(unittest.TestCase):
    def test_can_create(self):
        pub = TrajectoryPublisher()
        self.assertEqual(pub.trajectories, {})

    def test_can_update_trajectory(self):
        pub = TrajectoryPublisher()
        t1 = Trajectory(0., 1., (1, 2, 3))
        pub.update_trajectory("base", t1)
        self.assertEqual(pub.trajectories, {'base': t1})

    def test_can_merge(self):
        pub = TrajectoryPublisher()
        t1 = Trajectory(0., 1., (1, 2, 3))
        t2 = Trajectory(1., 1., (10, 20, 30))
        pub.update_trajectory("base", t1)
        pub.update_trajectory("base", t2)

        traj = pub.trajectories['base']

        self.assertEqual(traj, Trajectory(0., 1., (1, 10, 20, 30)))


