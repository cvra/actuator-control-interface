import unittest
from trajectory_publisher import *
try:
    from unittest.mock import patch
except ImportError:
    from mock import patch


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

    def test_wheelbase_trajectory_set(self):
        """
        Checks that we do merge the trajectory.
        """
        dt = 0.5
        t1 = WheelbaseTrajectory(0., dt, (1, 2, 3, 4))
        t2 = WheelbaseTrajectory(1., dt, (10, 20, 30, 40))

        pub = TrajectoryPublisher()
        pub.update_trajectory("base", t1)
        pub.update_trajectory("base", t2)

        expected = WheelbaseTrajectory(0., dt, (1, 2, 10, 20, 30, 40))

        self.assertEqual(pub.trajectories['base'], expected),

    def test_trajectory_set(self):
        dt = 0.5
        pub = TrajectoryPublisher()
        t1 = Trajectory(0., dt, (1, 2, 3, 4))
        t2 = Trajectory(1., dt, (10, 20, 30, 40))
        pub.update_trajectory("base", t1)
        pub.update_trajectory("base", t2)

        expected = Trajectory(0., dt, (1, 2, 10, 20, 30, 40))

        self.assertEqual(pub.trajectories['base'], expected)

    def test_trajectory_set_setpoint_after_a_trajectory(self):
        """
        If we input a setpoint after a trajectory, it should immediately be
        applied.
        """
        dt = 0.5
        pub = TrajectoryPublisher()

        t1 = Trajectory(0., dt, (1, 2, 3, 4))
        t2 = PositionSetpoint(12)
        pub.update_trajectory("base", t1)
        pub.update_trajectory("base", t2)

        self.assertEqual(pub.trajectories['base'], t2)

    @patch('time.time')
    def test_setpoint_then_trajectory(self, now):
        """
        Checks we can append a trajectory after a setpoint.
        """
        dt = 0.5
        pub = TrajectoryPublisher()
        p1 = PositionSetpoint(12)

        p1_new = TrajectoryPoint(12, 0, 0)
        p2_new = TrajectoryPoint(14, 0, 0)

        now.return_value = 1.
        traj = Trajectory(3., dt, (p2_new, ))
        expected = Trajectory(1., dt, (p1_new, ) * 4 + (p2_new, ))

        pub.update_trajectory("base", p1)
        pub.update_trajectory("base", traj)
        self.assertEqual(pub.trajectories['base'], expected)




