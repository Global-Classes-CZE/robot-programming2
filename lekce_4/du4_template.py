from microbit import sleep, pin14, pin15
from utime import ticks_us, ticks_diff

class MericTiku:
    def __init__(self):
        self.pocet_tiku = 0
        self.predesla_hodnota = 0

    def zapis_hodnotu(self, nova_hodnota):
        if nova_hodnota != self.predesla_hodnota:
            self.pocet_tiku += 1
            self.predesla_hodnota = nova_hodnota

if __name__ == "__main__":

    meric_tiku_leva = MericTiku()
    meric_tiku_prava = MericTiku()

    cas_minule = ticks_us()
    while True:
        meric_tiku_leva.zapis_hodnotu(pin14.read_digital())
        meric_tiku_prava.zapis_hodnotu(pin15.read_digital())
        sleep(100)
        cas_nyni = ticks_us()
        # every 1 second print the number of ticks
        if ticks_diff(cas_nyni, cas_minule) >= 1000000:
            print('Leva: ', meric_tiku_leva.pocet_tiku, 'Prava: ', meric_tiku_prava.pocet_tiku)
            cas_minule = cas_nyni
