from enum import Enum
from PCA9685 import PCA9685

pwm = PCA9685(0x40)
pwm.setPWMFreq(50)

offsets = [1500, 1500, 1500, 1500,
           1500, 1500, 1500, 1500,
           1500, 1500, 1500, 1500,
           1500, 1500, 1500, 1500]

DELTA = 250

class Position(Enum):
    ON = 1
    OFF = 2
    UNKNOWN = 3

switch_positions = [Position.UNKNOWN, Position.UNKNOWN, Position.UNKNOWN, Position.UNKNOWN,
                    Position.UNKNOWN, Position.UNKNOWN, Position.UNKNOWN, Position.UNKNOWN,
                    Position.UNKNOWN, Position.UNKNOWN, Position.UNKNOWN, Position.UNKNOWN,
                    Position.UNKNOWN, Position.UNKNOWN, Position.UNKNOWN, Position.UNKNOWN]

def calibrate_switch(port: int, offset: int):
    offsets[port] = offset
    set_switch_position(port, position = Position.OFF)

def set_switch_position(port: int, position: Position):
    "Sets a switch at port 0-15 on or off"
    pulse = offsets[port] + (DELTA if position == Position.ON else 0)
    switch_positions[port] = position
    pwm.setServoPulse(port, pulse)

def get_switch_position(port: int) -> Position:
    return switch_positions[port]
