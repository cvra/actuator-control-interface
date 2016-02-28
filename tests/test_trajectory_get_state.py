import unittest
from decimal import Decimal
from cvra_actuatorpub.trajectory_publisher import *

class TrajectoryGetStateTestCase(unittest.TestCase):
    def test_trajectory_get_state(self):
        t = Trajectory(0., 0.5, (1, 2, 3))
        self.assertEqual(t.get_state(1.), 3)
        self.assertEqual(t.get_state(0.), 1)
        self.assertEqual(t.get_state(0.8), 3)
        self.assertEqual(t.get_state(0.6), 2)

    def test_trajectory_get_state_after(self):
        t = Trajectory(0., 0.5, (1, 2, 3))
        self.assertEqual(t.get_state(10.), 3)

    def test_traject_get_state_dt_is_decimal(self):
        t = Trajectory(0., Decimal('0.5'), (1, 2, 3))
        self.assertEqual(t.get_state(10.), 3)



