import unittest
from cvra_actuatorpub.trajectory_publisher import *


class WheelbaseTrajectoryTestCase(unittest.TestCase):
    def test_can_create_trajectory(self):
        p = WheelbaseTrajectoryPoint(1., 2.,
                                     3., 4.,
                                     5.)

        traj = WheelbaseTrajectory(1., 1e-3, (p, ))

        self.assertEqual(traj.start, 1.)
        self.assertEqual(traj.dt, 1e-3)
        self.assertEqual(traj.points, (p, ))


class TrajectoryTestCase(unittest.TestCase):
    def test_can_create_trajectory(self):
        p = TrajectoryPoint(position=1.,
                            speed=2.,
                            torque=10.,
                            acceleration=42.
                            )

        Trajectory(start=1, dt=1e-3,
                   points=(p,))

    def check_trajectories_created_from_setpoints(self, setpoint, trajpoint):
        t = Trajectory.from_setpoint(point=setpoint, duration=2.,
                                     dt=1., start=0.)

        expected_t = Trajectory(start=0., dt=1., points=(trajpoint, trajpoint))

        self.assertEqual(t.points, expected_t.points)
        self.assertEqual(t.dt, expected_t.dt)
        self.assertEqual(t.start, expected_t.start)

    def test_can_create_from_position_setpoint(self):
        """
        Check that we can create a trajectory from a position setpoint.
        """
        p = PositionSetpoint(12)
        pp = TrajectoryPoint(12, 0, 0, 0)
        self.check_trajectories_created_from_setpoints(p, pp)

    def test_can_create_from_speed_setpoint(self):
        p = SpeedSetpoint(12)
        pp = TrajectoryPoint(0, 12, 0, 0)
        self.check_trajectories_created_from_setpoints(p, pp)

    def test_can_create_from_torque_setpoint(self):
        p = TorqueSetpoint(12)
        pp = TrajectoryPoint(0, 0, 0, 12)
        self.check_trajectories_created_from_setpoints(p, pp)


class SetpointTestCase(unittest.TestCase):
    def test_can_create(self):
        PositionSetpoint(12)
        SpeedSetpoint(12)
        TorqueSetpoint(12)
        VoltageSetpoint(12)

