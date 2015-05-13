import unittest
from trajectory_publisher import *


class WheelbaseTrajectoryTestCase(unittest.TestCase):
    def test_can_create_trajectory(self):
        p = WheelbaseTrajectoryPoint(1., 2.,
                                     3., 4.,
                                     5., 6.)

        traj = WheelbaseTrajectory(1., 1e-3, (p, ))

        self.assertEqual(traj.start, 1.)
        self.assertEqual(traj.dt, 1e-3)
        self.assertEqual(traj.points, (p, ))


class TrajectoryTestCase(unittest.TestCase):
    def test_can_create_trajectory(self):
        p = TrajectoryPoint(position=1.,
                            speed=2.,
                            torque=10.)

        Trajectory(start=1, dt=1e-3,
                   points=(p,))


class SetpointTestCase(unittest.TestCase):
    def test_can_create(self):
        PositionSetpoint(12)
        SpeedSetpoint(12)
        TorqueSetpoint(12)

