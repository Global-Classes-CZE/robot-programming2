from picoed import i2c
from time import sleep
from motor import Motor
from konstanty import Konstanty

class Robot:
    def __init__(self):
        self.__inicializovan = False
        self.__levy_motor = Motor(Konstanty.levy)
        self.__pravy_motor = Motor(Konstanty.pravy)
    
    # z lekce 3
    def inicializuj_se(self):
        while not i2c.try_lock():
            pass
        try:
            i2c.writeto(0x70, b'\x00\x01')
            i2c.writeto(0x70, b'\xE8\xAA')
            sleep(0.1)
            self.__inicializovan = True
        finally:
            i2c.unlock()
    
    def jed_pres_pwm(self, smer_pravy, pwm_pravy, smer_levy, pwm_levy):
        if not self.__inicializovan:
            return -1
        else:
            self.__pravy_motor.jed(smer_pravy, pwm_pravy)
            self.__levy_motor.jed(smer_levy, pwm_levy)
    
    def zastav(self):
        self.__levy_motor.zastav()
        self.__pravy_motor.zastav()