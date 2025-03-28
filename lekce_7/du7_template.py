from picoed import i2c
from time import sleep

pul_rozchod_kol = 0.075 # vzdalenost stredu kola od stredu robota

def init_motoru():
    i2c.write(0x70, bytes([0, 0x01]))
    i2c.write(0x70, bytes([8, 0xAA]))
    sleep(0.01)

def jed(dopredna, uhlova):
    v_l = dopredna - pul_rozchod_kol * uhlova
    v_r = dopredna + pul_rozchod_kol * uhlova

    print(f"v_l: {v_l}, v_r: {v_r}")

    if v_l == 0 and v_r == 0:
        jed_pwm("leva", "dopredu", 0)
        jed_pwm("prava", "dopredu", 0)
    else:
        if v_l >= 0:
            l_smer = "dopredu"
        else:
            l_smer = "dozadu"
        if v_r >= 0:
            r_smer = "dopredu"
        else:
            r_smer = "dozadu"

        jed_pwm("leva", l_smer, int(v_l)) 
        jed_pwm("prava", r_smer, int(v_r)) 

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
        i2c.write(0x70, bytes([kanal_off, 0]))
        i2c.write(0x70, bytes([kanal_on, rychlost]))
    finally:
        i2c.unlock()
    return 0

if __name__ == "__main__":
    # Write your code here :-)
    init_motoru()
    jed(135, 0)
    sleep(1)
    jed(0, 0)
    sleep(1)
    jed(0, 1350)
    sleep(1)
    jed(0, 0)
