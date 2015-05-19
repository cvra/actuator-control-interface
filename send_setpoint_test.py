from cvra_rpc.service_call import call
import argparse
from trajectory_publisher import *
import time


HOST = '192.168.3.20'


def create_actuator(name):
    return call((HOST, 20001), 'actuator_create_driver', [name])



parser = argparse.ArgumentParser()
parser.add_argument('host')
parser.add_argument('value', type=float)
parser.add_argument('--actuator', '-a',  default='foobar2000',
                    help="Actuator to set (default foobar2000)")

parser.add_argument('--negative', '-n', action='store_true')
parser.add_argument('--create', '-c', action='store_true')
parser.add_argument('--position', '-p', action='store_true')
parser.add_argument('--speed', '-s', action='store_true')
parser.add_argument('--torque', '-t', action='store_true')

args = parser.parse_args()

if args.create:
    print(create_actuator(args.actuator))

pub = SimpleRPCActuatorPublisher((args.host, 20000))

sign = 1
if args.negative:
    sign = -1

if args.position:
    pub.update_actuator(args.actuator, PositionSetpoint(sign*args.value))
elif args.speed:
    pub.update_actuator(args.actuator, SpeedSetpoint(sign*args.value))
elif args.torque:
    pub.update_actuator(args.actuator, TorqueSetpoint(sign*args.value))

print(pub.get_state(args.actuator, time.time()))

pub.publish(time.time())

