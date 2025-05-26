from picoed import i2c
from time import sleep
from konstanty import Konstanty

class Motor:
    def __init__(self, strana):
        self.__strana = strana
        if strana == Konstanty.levy:
            self.__dopredu = b"\x05"
            self.__dozadu = b"\x04"
        elif strana == Konstanty.pravy:
            self.__dopredu = b"\x03"
            self.__dozadu = b"\x02"
        else:
            raise AttributeError("spatna strana motoru, musi byt \"levy\" a nebo \"pravy\", zadane jmeno je" + str(strana))

    # pomocna funkce pro DU3
    def __nastav_PWM_kanaly(self, kanal_on, kanal_off, rychlost):
        # je nesmirne dulezite vzdy mit zapnuty jen jeden kanal,
        # tedy tato funkce zarucuje, ze se druhy kanal vypne

        while not i2c.try_lock():
            pass
        try:
            i2c.writeto(0x70, kanal_off + bytes([0]))
            i2c.writeto(0x70, kanal_on + bytes([rychlost]))
        finally:
            i2c.unlock()
        
        return 0

    # DU3
    def jed(self, smer, rychlost):
        '''
        Tato funkce uvede dany motor do pohybu,
        zadanou rychlosti a v pozadovanem smeru.
        Vraci chybove hodnoty:
            0: vse je v poradku
        -1: program neprobehl spravne
        -3: pozadovana rychlost je mimo mozny rozsah
        -4: zadany nepodporovany smer
        '''
        je_vse_ok = -1

        rychlost = int(rychlost)
        if rychlost < 0 or rychlost > 180:
            je_vse_ok = -3
            return

        if smer == "dopredu":
            je_vse_ok = self.__nastav_PWM_kanaly(self.__dopredu, self.__dozadu, rychlost)
        elif smer == "dozadu":
            je_vse_ok = self.__nastav_PWM_kanaly(self.__dozadu, self.__dopredu, rychlost)
        else:
            je_vse_ok = -4

        return je_vse_ok
    
    def zastav(self):
        self.jed("dopredu",0)
        self.jed("dozadu",0)