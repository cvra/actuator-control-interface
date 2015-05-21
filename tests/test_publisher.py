import unittest
import math
from decimal import Decimal

try:
    from unittest.mock import patch, ANY
except ImportError:
    from mock import patch, ANY

from cvra_actuatorpub.trajectory_publisher import *

class ActuatorPublisherTestCase(unittest.TestCase):
    def test_can_create(self):
        pub = ActuatorPublisher()
        self.assertEqual(pub.trajectories, {})

    def test_can_update_actuator(self):
        pub = ActuatorPublisher()
        t1 = Trajectory(0., 1., (1, 2, 3))
        pub.update_actuator("base", t1)
        self.assertEqual(pub.trajectories, {'base': t1})

    def test_can_merge(self):
        pub = ActuatorPublisher()
        t1 = Trajectory(0., 1., (1, 2, 3))
        t2 = Trajectory(1., 1., (10, 20, 30))
        pub.update_actuator("base", t1)
        pub.update_actuator("base", t2)

        traj = pub.trajectories['base']

        self.assertEqual(traj, Trajectory(0., 1., (1, 10, 20, 30)))

    def test_can_get_trajectory_point(self):
        pub = ActuatorPublisher()
        pub.update_actuator("base", Trajectory(0., 1., (1, 2, 3)))

        state = pub.get_state("base", 1.4)
        self.assertEqual(state, 2)

    def test_can_get_sepoint(self):
        pub = ActuatorPublisher()

        pub.update_actuator("base", PositionSetpoint(10))
        state = pub.get_state("base", 1.4)
        self.assertEqual(state, PositionSetpoint(10))

    def test_can_gc(self):
        pub = ActuatorPublisher()
        traj = Trajectory(4., 1., (1, 2, 3, 4))
        pub.update_actuator("base", traj)
        pub.gc(6.)
        self.assertEqual(pub.trajectories['base'].points, (3, 4))

    def test_dont_gc_setpoint(self):
        pub = ActuatorPublisher()
        p = PositionSetpoint(10)
        pub.update_actuator("base", p)
        pub.gc(6.)
        self.assertEqual(pub.trajectories['base'], p)

    def test_publish_exists(self):
        pub = ActuatorPublisher()
        pub.publish(date=10.)


class SimpleRPCPublisherTestCase(unittest.TestCase):
    dt = Decimal(1) / Decimal(100)
    def setUp(self):
        self.pub = SimpleRPCActuatorPublisher(('localhost', 20000))

    def test_create(self):
        self.assertEqual(self.pub.trajectories, {})
        self.assertEqual(self.pub.target, ('localhost', 20000))

    def test_publish_positionpoint(self):
        self.pub.update_actuator('foo', PositionSetpoint(10.))

        with patch('cvra_rpc.message.send') as send:
            self.pub.publish(date=10.)
            send.assert_any_call(self.pub.target, 'actuator_position', ['foo', 10.])

    def test_publish_speed(self):
        self.pub.update_actuator('foo', SpeedSetpoint(10.))
        with patch('cvra_rpc.message.send') as send:
            self.pub.publish(date=10.)
            send.assert_any_call(self.pub.target, 'actuator_velocity', ['foo', 10.])

    def test_publish_voltage(self):
        self.pub.update_actuator('foo', VoltageSetpoint(10.))
        with patch('cvra_rpc.message.send') as send:
            self.pub.publish(date=10.)
            send.assert_any_call(self.pub.target, 'actuator_voltage', ['foo', 10.])

    def test_publish_torque(self):
        self.pub.update_actuator('foo', TorqueSetpoint(10.))
        with patch('cvra_rpc.message.send') as send:
            self.pub.publish(date=10.)
            send.assert_any_call(self.pub.target, 'actuator_torque', ['foo', 10.])

    def test_publish_chunk(self):
        traj = Trajectory(10., dt=self.dt,
                          points=tuple(TrajectoryPoint(float(i), 10.,
                                                       acceleration=20.,
                                                       torque=30.)
                                       for i in range(100)))

        self.pub.update_actuator('foo', traj)

        expected_points = [[float(i), 10., 20., 30.] for i in range(20, 30)]

        with patch('cvra_rpc.message.send') as send:
            self.pub.publish(date=10.2)
            self.assertTrue(send.called)
            target, name, args = tuple(send.call_args[0])
            self.assertEqual(target, self.pub.target)
            self.assertEqual(name, 'actuator_trajectory')

            _, start_s, start_us, dt_us, points = tuple(args)
            self.assertEqual(10, start_s)
            self.assertAlmostEqual(0.2, start_us / 1e6, 3)
            self.assertEqual(10*1000, dt_us)
            self.assertEqual(points, expected_points)

    def test_publish_wheelbase(self):
        traj = WheelbaseTrajectory(0.2, dt=self.dt, points=tuple([
            # This settings make omega = 2
                                   WheelbaseTrajectoryPoint(0., 0., # pos
                                                            2., # spd
                                                            math.pi / 2, # theta
                                                            2.) # omega
                                   ]))

        self.pub.update_actuator('base', traj)

        with patch('cvra_rpc.message.send') as send:
            self.pub.publish(date=0.)
            send.assert_any_call(self.pub.target, 'wheelbase_trajectory', ANY)

            _, _, args = send.call_args[0]

            s, us, dt, points = args

            x, y, v, theta, omega = tuple(points[0])

            self.assertEqual(0, s)
            self.assertAlmostEqual(us / 1e6, 0.2)
            self.assertEqual(dt, 10000)

            self.assertAlmostEqual(x, 0.)
            self.assertAlmostEqual(y, 0.)
            self.assertAlmostEqual(v, 2.)
            self.assertAlmostEqual(theta, math.pi / 2)
            self.assertAlmostEqual(theta, math.pi / 2)
            self.assertAlmostEqual(omega, 2.)

    def test_publish_wheelbase_past_trajectory_end(self):
        """
        Checks that nothing happens when we publish past the end of the
        trajectory.
        """
        traj = WheelbaseTrajectory(0.2, dt=self.dt, points=(1, 2, 3))
        self.pub.update_actuator('base', traj)
        with patch('cvra_rpc.message.send') as send:
            self.pub.publish(date=1000.)
            self.assertFalse(send.called)

    def test_publish_trajectory_past_end(self):
        """
        Checks that we can publish past the end of the trajectory.
        """
        points = [TrajectoryPoint(float(i), 0., 0., 0.) for i in range(10)]
        traj = Trajectory(0.2, self.dt, points=tuple(points))
        self.pub.update_actuator('foo', traj)

        with patch('cvra_rpc.message.send') as send:
            self.pub.publish(date=1000.)
            send.assert_any_call(self.pub.target, 'actuator_position', ['foo', 9.])


