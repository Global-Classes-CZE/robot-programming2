from microbit import i2c, sleep

def init_motoru():
    i2c.write(0x70, b'\x00\x01')
    i2c.write(0x70, b'\xE8\xAA')
    sleep(100)

def jed(strana, smer, rychlost):
    if rychlost >= 0 and rychlost <= 250:
        if strana == "leva" and smer == "dopredu":
            x = b'\x05'
        elif strana == "leva" and smer == "dozadu":
            x = b'\x04'
        elif strana == "prava" and smer == "dopredu":
            x = b'\x03'
        elif strana == "prava" and smer == "dozadu":
            x = b'\x02'
        else:
            print("Spatne parametry")
        i2c.write(0x70, x + bytes([rychlost]))
    else:
        print("Spatne zadana rychlost")

if __name__ == "__main__":
    i2c.init()
    init_motoru()
    jed("leva", "dozadu", 0)
    jed("prava", "dozadu", 0)
    sleep(1000)
    jed("leva", "dopredu", 135)
    jed("prava", "dopredu", 135)
    sleep(1000)
    jed("leva", "dopredu", 0)
    jed("prava", "dopredu", 0)
    sleep(1000)
    jed("leva", "dozadu", 135)
    jed("prava", "dozadu", 135)
    sleep(1000)
    jed("leva", "dozadu", 0)
    jed("prava", "dozadu", 0)   
