from microbit import i2c, sleep

def init_motoru():
    i2c.write(0x70, b'\x00\x01')
    i2c.write(0x70, b'\xE8\xAA')
    sleep(100)

def jed(strana, smer, rychlost):

    error = False

    if strana == 'prava' and smer == 'vzad':
        povel = b'\x02'
    elif strana == 'prava' and smer == 'vpred':
        povel = b'\x03'
    elif strana == 'leva' and smer == 'vzad':
        povel = b'\x04'
    elif strana == 'leva' and smer == 'vpred':
        povel = b'\x05'
    else:
        error = True
        print("Input Error!")

    if error != True:
        i2c.write(0x70, povel + bytes([rychlost]))

def zastav(cas):
    i2c.write(0x70, b'\x02' + bytes([0]))
    i2c.write(0x70, b'\x03' + bytes([0]))
    i2c.write(0x70, b'\x04' + bytes([0]))
    i2c.write(0x70, b'\x05' + bytes([0]))
    sleep(cas)

if __name__ == "__main__":
    # Write your code here :-)
    i2c.init()
    init_motoru()

    jed('leva', 'vpred', 125)
    jed('prava', 'vpred', 125)
    sleep(1000)

    zastav(1000)

    jed('leva', 'vzad', 125)
    jed('prava', 'vzad', 125)
    sleep(1000)

    zastav(1000)
