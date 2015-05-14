import unittest
from trajectory_publisher import *

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
        pub.publish()

