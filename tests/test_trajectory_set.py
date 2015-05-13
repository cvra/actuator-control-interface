import unittest
from trajectory_publisher import *


class TrajectoryTestingTestCase(unittest.TestCase):
    def test_trajectory_publisher_is_empty(self):
        pub = TrajectoryPublisher()
        self.assertEqual({}, pub.trajectories)

    def test_trajectory_update_empy(self):
        pub = TrajectoryPublisher()
        t = SpeedSetpoint(12.)

        pub.update_trajectory("foo", t)
        self.assertEqual(pub.trajectories['foo'], t)

    def test_trajectory_update_setpoint(self):
        pub = TrajectoryPublisher()
        start, stop = PositionSetpoint(12.), PositionSetpoint(14.)
        pub.update_trajectory('foo', start)
        pub.update_trajectory('foo', stop)
        self.assertEqual(pub.trajectories['foo'], stop)

    def test_trajectory_wheelbase_cannot_be_changed(self):
        """
        Changed that wheelbase trajectories cannot be switched to something else.
        """
        pub = TrajectoryPublisher()
        start = WheelbaseTrajectory(1., 1., tuple())
        pub.update_trajectory("foo", start)

        with self.assertRaises(ValueError):
            pub.update_trajectory("foo", TorqueSetpoint(10.))
