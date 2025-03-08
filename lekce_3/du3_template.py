from microbit import i2c, sleep

def init_motoru():
    i2c.write(0x70, b'\x00\x01')
    i2c.write(0x70, b'\xE8\xAA')
    sleep(100)

def jed(strana, smer, rychlost):
    if (rychlost >= 0 and rychlost <= 255):
        if (strana == "leva" and smer == "dopredu"):
            i2c.write(0x70, b'\x05' + bytes([rychlost]))
        if (strana == "leva" and smer == "dozadu"):
            i2c.write(0x70, b'\x04' + bytes([rychlost]))
        if (strana == "prava" and smer == "dopredu"):
            i2c.write(0x70, b'\x03' + bytes([rychlost]))
        if (strana == "prava" and smer == "dozadu"):
            i2c.write(0x70, b'\x02' + bytes([rychlost]))

if __name__ == "__main__":
    i2c.init()
    init_motoru()
    jed("leva","dopredu",125)
    jed("prava","dopredu",125)
    sleep (1000)
    jed("leva","dopredu",0)
    jed("prava","dopredu",0)
    sleep (1000)
    jed("leva","dozadu",135)
    jed("prava","dozadu",135)
    sleep (1000)
    jed("leva","dozadu",0)
    jed("prava","dozadu",0)
