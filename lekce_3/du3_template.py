from microbit import i2c, sleep

from microbit import i2c,sleep

def init_motoru():
    i2c.write(0x70, b'\x00\x01')
    i2c.write(0x70, b'\xE8\xAA')
    i2c.init()
    sleep(100)

def jed(strana, smer, rychlost):
    if strana == 'prava':
        if smer == 'dopredu':
            pravy_motor = b'\x03'
        if smer == 'dozadu':
            pravy_motor = b'\x02'
            
        i2c.write(0x70, pravy_motor + bytes([rychlost]))
            
    if strana == 'lava':
        if smer == 'dopredu':
            lavy_motor = b'\x05'
        if smer == 'dozadu':
            lavy_motor = b'\x04'
    
        i2c.write(0x70, lavy_motor + bytes([rychlost]))

if __name__ == "__main__":
    
    init_motoru()
    
    jed('prava','dopredu',135)
    jed('lava','dopredu',135)
    
    sleep(1000)
    
    jed('prava','dopredu',0)
    jed('lava','dopredu',0)
    
    sleep(1000)
    
    jed('prava','dozadu',135)
    jed('lava','dozadu',135)
    
    sleep(1000)
    
    jed('prava','dozadu',0)
    jed('lava','dozadu',0)
    
    sleep(1000)