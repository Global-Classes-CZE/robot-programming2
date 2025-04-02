from picoed import i2c
from time import sleep

def init_motor():
    i2c.write(0x70, bytes([0, 0x01]))
    i2c.write(0x70, bytes([8, 0xAA]))
    sleep(0.01)

def go(forward, angular):
     # Polovina rozteče kol v metrech (7,5 cm)
    d = 0.075

    # Výpočet podle kinematiky diferenciálního pohonu
    v_l = forward - d * angular
    v_r = forward + d * angular

    def speed_to_pwm(speed):
        # Převod rychlosti na PWM v rozsahu 0–255
        return min(max(int(abs(speed)), 0), 255)

    pwm_l = speed_to_pwm(v_l)
    pwm_r = speed_to_pwm(v_r)

    # Výpisy pro ladění
    print(f"[go] v = {forward}, ω = {angular}")
    print(f"[go] v_l = {v_l:.2f}, v_r = {v_r:.2f}")
    print(f"[go] pwm_l = {pwm_l}, pwm_r = {pwm_r}")
    print(f"[go] left: {'forward' if v_l >= 0 else 'backward'}, right: {'forward' if v_r >= 0 else 'backward'}")

    if forward == 0 and angular == 0:
        print("[go] Stop")
        go_pwm("left", "forward", 0)
        go_pwm("right", "forward", 0)
        return

    if v_l >= 0:
        go_pwm("left", "forward", pwm_l)
    else:
        go_pwm("left", "backward", pwm_l)

    if v_r >= 0:
        go_pwm("right", "forward", pwm_r)
    else:
        go_pwm("right", "backward", pwm_r)

    return 0

def go_pwm(side, direction, speed):
    # side může být jen “left” a “right”
    # “direction” je typu string a může mít hodnoty “forward”, "backward"
    if (speed >= 0 and speed <= 255):
        if (side == "left" and direction == "forward"):
            set_canals(4, 5, speed)
            return 0
        elif (side == "left" and direction == "backward"):
            set_canals(5, 4, speed)
            return 0
        elif (side == "right" and direction == "forward"):
            set_canals(2, 3, speed)
            return 0
        elif (side == "right" and direction == "backward"):
            set_canals(3, 2, speed) 
            return 0
        else:
            return -1
    else:
        return -2

def set_canals(canal_off, canal_on, pwm):
    while not i2c.try_lock():
        pass
    try:
        i2c.write(0x70, bytes([canal_off, 0]))
        i2c.write(0x70, bytes([canal_on, pwm]))
    finally:
        i2c.unlock()
    return 0

if __name__ == "__main__":
    init_motor() 
    go(135, 1350)       # Dopředný pohyb
    sleep(1)
    go(0, 0)         # Zastavení
    sleep(1)
    go(135, 1350)      # Otáčení na místě doleva
    sleep(1)
    go(0, 0)         # Zastavení
