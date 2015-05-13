# Trajectory publisher

This module receives trajectories or setpoint for the various actuators in the robot.
It then send them to the master board at a fixed rate.
It also handles end of trajectory cases correctly by switching to position control mode.

## Setpoint types
Each setpoint type is represented by a named tuple.
The various setpoints are immutable to make them easier to copy / share.

* `WheelbaseTrajectory` is the type used to represent a robot movement which will then be fed to the trajectory tracker.
    It must be handled differently because it will not switch to position control after the end of the movement.
    Trajectories will also be converted to trajectory tracker format (speed in polar coordinates) before sending them to the master board.
    It contains several fields :
    - Start date in UNIX format
    - Sampling interval
    - Tuple of `WheelbaseTrajectoryPoint`s, each containing `x`, `y` (position), `vx`, `vy` (speed) and `ax`, `ay` (acceleration).
* `Setpoint`: This is just the type used when one wants a fixed setpoint.
    Fields:
    - Value of the setpoint
    This is a base class. User should rather use `PositionSetpoint`, `SpeedSetpoint, `TorqueSetpoint`.

* `Trajectory` is used to perform trajectories with an actuator (e.g. Debra's arms).
    Fields:
    - Tuple of `TrajectoryPoint`s, each containing `position`, `speed`, `torque`.
        If one field is not used it must be left zero.
    - Start date in UNIX format
    - Sampling interval
