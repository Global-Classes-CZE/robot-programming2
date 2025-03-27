from picoed import i2c
from time import sleep

def init_motoru():
    i2c.write(0x70, bytes([0, 0x01]))
    i2c.write(0x70, bytes([8, 0xAA]))
    sleep(0.01)

def jed(dopredna, uhlova):

    d = 0.0725 # polovina vzdálenosti mezi koly robota
    v_l = dopredna - d * uhlova
    v_r = dopredna + d * uhlova

    # rychlosti v_l a v_r se ještě musí převést na PWM signál
    if v_l > 0:
        jed_pwm("leva", "dopredu",v_l)
    elif v_l < 0:
        jed_pwm("leva", "dozadu", v_l)  
    else:
        jed_pwm("leva", "dopredu", 0)

    if v_r > 0:
        jed_pwm("prava", "dopredu", v_r)
    elif v_r < 0:
        jed_pwm("prava", "dozadu", v_r)
    else:
        jed_pwm("prava", "dopredu", 0)

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
    # volejte funkci jed, tak abyste ziskali:
    # Pohyb robota dopredu 1s
    # Zastaveni 1s - DULEZITE! Nikdy nemente smer jizdy bez zastaveni
    # Otáčení robota na místě doleva
    # zastaveni
