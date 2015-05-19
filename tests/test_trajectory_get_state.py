import unittest
from cvra_actuatorpub.trajectory_publisher import *

class TrajectoryGetStateTestCase(unittest.TestCase):
    def test_trajectory_get_state(self):
        t = Trajectory(0., 0.5, (1, 2, 3))
        self.assertEqual(trajectory_get_state(t, 1.), 3)
        self.assertEqual(trajectory_get_state(t, 0.), 1)
        self.assertEqual(trajectory_get_state(t, 0.8), 3)
        self.assertEqual(trajectory_get_state(t, 0.6), 2)

    def test_trajectory_get_state_after(self):
        t = Trajectory(0., 0.5, (1, 2, 3))
        self.assertEqual(trajectory_get_state(t, 10.), 3)


