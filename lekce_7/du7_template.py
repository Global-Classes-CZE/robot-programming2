from picoed import i2c
from time import sleep

POLOMER_ROBOTA = 0.075

def init_motoru():
    while not i2c.try_lock():
        pass
    try:
        i2c.writeto(0x70, b'\x00\x01')
        i2c.writeto(0x70, b'\xE8\xAA')
        sleep(0.1)
    finally:
        i2c.unlock()

def jed(dopredna, uhlova):
    v_l = dopredna - (uhlova * POLOMER_ROBOTA)
    v_r = dopredna + (uhlova * POLOMER_ROBOTA)

    if v_l == 0 and v_r == 0:
        jed_pwm("leva", "dopredu", 0)
        jed_pwm("prava", "dopredu", 0)
    else:
        smer_l = "dopredu" if v_l >= 0 else "dozadu"
        smer_r = "dopredu" if v_r >= 0 else "dozadu"

        jed_pwm("leva", smer_l, min(abs(int(v_l)), 255))
        jed_pwm("prava", smer_r, min(abs(int(v_r)), 255))

    return 0

def jed_pwm(strana, smer, rychlost):
    if (rychlost >= 0 and rychlost <= 255):
        if (strana == "leva" and smer == "dopredu"):
            nastav_kanaly(4, 5, rychlost)
            return 0
        elif (strana == "leva" and smer == "dozadu"):
            nastav_kanaly(5, 4, rychlost)
            return 0
        elif (strana == "prava" and smer == "dopredu"):
            nastav_kanaly(2, 3, rychlost)
            return 0
        elif (strana == "prava" and smer == "dozadu"):
            nastav_kanaly(3, 2, rychlost)
            return 0
        else:
            return -1
    else:
        return -2

def nastav_kanaly(kanal_off, kanal_on, rychlost):
    while not i2c.try_lock():
        pass
    try:
        i2c.writeto(0x70, bytes([kanal_off, 0]))
        i2c.writeto(0x70, bytes([kanal_on, rychlost]))
    finally:
        i2c.unlock()
    return 0

def stuj():
    jed(0, 0)
    sleep(1)

if __name__ == "__main__":
    # Write your code here :-)
    init_motoru()

    # jed dopredu
    jed(135, 0)
    sleep(2)
    stuj()
    # otoc se vlevo
    jed(0, 1350)
    sleep(2)
    stuj()
    # otoc se vpravo
    jed(0, -1350)
    sleep(2)
    stuj()
    # jed dozadu
    jed(-135, 0)
    sleep(2)
    stuj()
