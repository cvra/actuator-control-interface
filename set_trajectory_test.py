from cvra_rpc.service_call import call
import argparse
from cvra_actuatorpub.trajectory_publisher import *
import time


HOST = '192.168.3.20'


def create_actuator(name):
    return call((HOST, 20001), 'actuator_create_driver', [name])



parser = argparse.ArgumentParser()
parser.add_argument('host')
# parser.add_argument('value', type=float)
parser.add_argument('--actuator', '-a',  default='foobar2000',
                    help="Actuator to set (default foobar2000)")

# parser.add_argument('--negative', '-n', action='store_true')
parser.add_argument('--create', '-c', action='store_true')
# parser.add_argument('--position', '-p', action='store_true')
# parser.add_argument('--speed', '-s', action='store_true')
# parser.add_argument('--torque', '-t', action='store_true')

args = parser.parse_args()

if args.create:
    print(create_actuator(args.actuator))

pub = SimpleRPCActuatorPublisher((args.host, 20000))

# print(pub.get_state(args.actuator, time.time()))

# pub.publish(time.time())

DT = 0.01
ACC = 1
VEL = 1
# [p.position, p.speed, p.acceleration, p.torque]

points = []

t = 0
pos = 0
vel = 0

while vel < VEL:
    pos += vel * DT + 1/2 * ACC * DT**2
    vel += ACC * DT
    t += DT
    points.append(TrajectoryPoint(pos, vel, ACC, 0))

while vel > 0:
    pos += vel * DT - 1/2 * ACC * DT**2
    vel += - ACC * DT
    t += DT
    points.append(TrajectoryPoint(pos, vel, -ACC, 0))

points.append(TrajectoryPoint(pos, 0, 0, 0))


print("\n".join(map(str, points)))

# map(print, points)

if input("go ? ") == 'y':
    traj = Trajectory(start=time.time()+1., dt=DT, points=tuple(points))

    pub.update_actuator(args.actuator, traj)

    while True:
        pub.publish(time.time())
        print(pub.get_state(args.actuator, time.time()))
        time.sleep(0.1)
