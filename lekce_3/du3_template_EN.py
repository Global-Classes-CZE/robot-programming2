from microbit import i2c, sleep

class InvalidSideException(Exception):
    """Raised when an invalid side is specified."""
    pass

class InvalidDirectionException(Exception):
    """Raised when an invalid direction is specified."""
    pass

class InvalidSpeedException(Exception):
    """Raised when an invalid speed is specified."""
    pass

class Engine:
    VALID_SIDES = ("left", "right")
    VALID_DIRECTIONS = ("forward", "backward")

    # Commands for movement per side and direction
    MOVE_COMMANDS = {
        "left": {
            "forward": b'\x03',
            "backward": b'\x02'
        },
        "right": {
            "forward": b'\x05',
            "backward": b'\x04'
        }
    }

    def __init__(self, side):
        if side not in self.VALID_SIDES:
            raise InvalidSideException("Side must be 'left' or 'right'")
        self.side = side

    def init_engines():
        """Initialize engines controller. This method should be called before any engine movement."""
        i2c.write(0x70, b'\x00\x01')
        i2c.write(0x70, b'\xE8\xAA')
        sleep(100)

    def go(self, direction, speed):
        """
        Control the engine movement.
        :param direction: 'forward' or 'backward'
        :param speed: integer value between 0 and 255
        """
        if direction not in self.VALID_DIRECTIONS:
            raise InvalidDirectionException("Direction must be 'forward' or 'backward'")
        if not (0 <= speed <= 255):
            raise InvalidSpeedException("Speed must be between 0 and 255")

        command = self.MOVE_COMMANDS[self.side][direction]
        i2c.write(0x70, command + bytes([speed]))

    def emergency_stop(self):
        """Stop all engines immediately."""
        sleep(100)
        self.go("forward", 0)
        sleep(100)
        self.go("backward", 0)

if __name__ == "__main__":
    i2c.init()

    try:
        print("Initializing engines...")
        Engine.init_engines()
        left_engine = Engine("left")
        right_engine = Engine("right")

        print("Engines moving forward...")
        left_engine.go("forward", 135)
        right_engine.go("forward", 135)

        print("Stop both engines.")
        sleep(1000)
        left_engine.go("forward", 0)
        right_engine.go("forward", 0)

        print("Engines moving backward...")
        sleep(1000)
        left_engine.go("backward", 135)
        right_engine.go("backward", 135)

        print("Stop both engines.")
        sleep(1000)
        left_engine.go("backward", 0)
        right_engine.go("backward", 0)

        sleep(1000)
        print("Done.")

    except Exception as e:
        print(e)
        print("Exiting...")
        left_engine.emergency_stop()
        right_engine.emergency_stop()
