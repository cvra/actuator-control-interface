from trajectory_publisher import *
import time
import argparse
from decimal import Decimal

SPEED = 5e-2  # m / s
DT = Decimal(1) / Decimal(100)

parser = argparse.ArgumentParser()

parser.add_argument('host')

args = parser.parse_args()

points = [WheelbaseTrajectoryPoint(float(i), 42.,
                                   0.2, 0.,
                                   0., 0.) for i in [x * float(DT) * SPEED for x in range(0, 400)]]

print("\n".join(map(str, points)))

pub = SimpleRPCActuatorPublisher((args.host, 20000))

if input("go ? ") == 'y':
    traj = WheelbaseTrajectory(start=time.time()+1., dt=DT, points=tuple(points))

    pub.update_actuator('base', traj)

    while True:
        pub.publish(time.time())
        time.sleep(0.1)


