import unittest
from cvra_actuatorpub.trajectory_publisher import *


class TrajectoryChunkTestCase(unittest.TestCase):
    dt = 0.5
    traj = Trajectory(0., dt, tuple(range(100)))

    def test_can_create_chunk_iterator(self):
        """
        Tests if we can create an iterator from chunks.
        """
        chunks = trajectory_to_chunks(self.traj, 10)

        traj = next(chunks)

        self.assertEqual(traj,
                         Trajectory(0., self.dt, tuple(i for i in range(10))))

    def test_the_chunk_is_complete(self):
        """
        Tests if the chunks contain the whole trajectory.
        """
        chunks = trajectory_to_chunks(self.traj, 10)
        points = sum((c.points for c in chunks), tuple())
        self.assertEqual(points, self.traj.points)

    def test_chunk_dates(self):
        """
        Tests if the dates of the chunk are correct.
        """
        traj = Trajectory(10., 0.5, tuple(range(100)))
        chunks = trajectory_to_chunks(traj, 10)

        expected = list(map(float, range(10, 60, 5)))
        dates = [c.start for c in chunks]

        self.assertEqual(dates, expected)

    def test_chunk_dt(self):
        """
        Test that chunks have the same sample rate as the original trajectory.
        """
        for chunk in trajectory_to_chunks(self.traj, 10):
            self.assertEqual(chunk.dt, self.dt)

    def test_chunk_other_type(self):
        """
        Tests that we can instantiate Wheelbase chunks too.
        """
        traj = WheelbaseTrajectory(0., self.dt, tuple(range(100)))
        for chunk in trajectory_to_chunks(traj, 10):
            self.assertIsInstance(chunk, WheelbaseTrajectory)
