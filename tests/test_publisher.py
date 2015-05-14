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

    def test_can_get_trajectory_point(self):
        pub = TrajectoryPublisher()
        pub.update_trajectory("base", Trajectory(0., 1., (1, 2, 3)))

        state = pub.get_state("base", 1.4)
        self.assertEqual(state, 2)

    def test_can_get_sepoint(self):
        pub = TrajectoryPublisher()

        pub.update_trajectory("base", PositionSetpoint(10))
        state = pub.get_state("base", 1.4)
        self.assertEqual(state, PositionSetpoint(10))

