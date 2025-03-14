from microbit import i2c, sleep
from sys import exit

# inicializae i2c motoru
def init_motoru():
    i2c.init(freq=400000)
    i2c.write(0x70, b'\x00\x01')
    i2c.write(0x70, b'\xE8\xAA')
    sleep(100)

# zastaveni vsech motoru
def motory_stop():
    i2c.write(0x70, b"\x02" + bytes([0]))
    i2c.write(0x70, b"\x03" + bytes([0]))
    i2c.write(0x70, b"\x04" + bytes([0]))
    i2c.write(0x70, b"\x05" + bytes([0]))

# jizda jednotlivych motoru
def jed(strana, smer, rychlost):
    motor_smer = strana+"_"+smer

    if motor_smer == "leva_dopredu":
        nulovani_pwm = b"\x04"
        prikaz = b"\x05"

    elif motor_smer == "leva_dozadu":
        nulovani_pwm = b"\x05"
        prikaz = b"\x04"

    elif motor_smer == "prava_dopredu":
        nulovani_pwm = b"\x02"
        prikaz = b"\x03"

    elif motor_smer ==  "prava_dozadu":
        nulovani_pwm = b"\x03"
        prikaz = b"\x02"

    else:
        print("chybny prikaz - zastavuji motory")
        motory_stop()
        return

    nulovaci_prikaz = nulovani_pwm + bytes([0])
    i2c.write(0x70, nulovaci_prikaz)
    finalni_prikaz = prikaz + bytes([rychlost])
    i2c.write(0x70, finalni_prikaz)

# hlavni cast programu
if __name__ == "__main__":
    # Write your code here :-)
    i2c.init()
    init_motoru()
    rychlost = 135

    # Pohyb robota dopredu 1s
    jed("leva", "dopredu", rychlost)
    jed("prava", "dopredu", rychlost)
    sleep(1000)

    # Zastaveni na 1s
    motory_stop()
    sleep(1000)

    # Pohyb vzad 1s
    jed("leva", "dozadu", rychlost)
    jed("prava", "dozadu", rychlost)
    sleep(1000)

    # zastaveni
    motory_stop()

    #ukonceni programu
    exit()
