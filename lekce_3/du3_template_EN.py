from microbit import i2c, sleep

def init_motor():
    i2c.write(0x70, b'\x00\x01')
    i2c.write(0x70, b'\xE8\xAA')
    sleep(100)

def go(side, direction, speed):
   """Engine control, validation of input parameters."""
   if side not in ["right", "left"]:
       raise ValueError("Error: Invalid side. Use 'right' or left'.")
       
   if direction not in ["forward", "backward"]:
        raise ValueError("Error: Invalid direction. Use 'forward' or backward'.")

   if speed >= 0 and speed <= 255:
        motor_map = {
            ("right", "forward"): b'\x03',
            ("right", "backward"): b'\x02',
            ("left", "forward"): b'\x05',
            ("left", "backward"): b'\x04'
        }
        i2c.write(0x70, motor_map[(side, direction)] + bytes([speed]))
   else:
        print("Error: Speed must be between 0 and 255.")
def stop_dir(direction):
    """Stop the last direction of the robot"""
    if direction not in ["forward", "backward"]:
        raise ValueError("Error: Invalid side. Use 'right' or left'.")
    motor_map = {
        "forward": [b'\x03', b'\x05'],
        "backward": [b'\x02', b'\x04']
    }
     # Sends 0V to channels to stop the motor
    for channel in motor_map[direction]:
        i2c.write(0x70, channel + bytes([0]))

def stop_all_motors():
    """Stop all engines."""
    motor_map = {
        "right": [b'\x03', b'\x02'],
        "left": [b'\x05', b'\x04']
    }

    for side in motor_map:  # Loop trough both sides
        for channel in motor_map[side]:  # Stops all channels for the given motor
            i2c.write(0x70, channel + bytes([0]))

if __name__ == "__main__":
    i2c.init() #I2C initialization
    init_motor() #Engine IO initialization
    #Robot goes forward for 1 s
    go("right", "forward", 150)
    go("left", "forward", 150)
    sleep(1000)
    #Robot goes backward for 1s
    stop_dir("forward")
    go("right", "backward", 150)
    go("left", "backward", 150)
    sleep(1000)
    #Robot stops
    stop_all_motors()
