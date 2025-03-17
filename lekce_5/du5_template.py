from microbit import sleep, pin14, pin15
from utime import ticks_diff, ticks_us


class Pocitadlo_tiku:
    def __init__(self):
        self._pocet_levy = 0
        self._pocet_pravy = 0
        self._posledni_leva = 0
        self._posledni_prava = 0

    def pocet(self, strana, data):
        if strana == "leva":
            if self._posledni_leva != data:
                self._posledni_leva = data
                self._pocet_levy += 1
            return self._pocet_levy
        if strana == "prava":
            if self._posledni_prava != data:
                self._posledni_prava = data
                self._pocet_pravy += 1
            return self._pocet_pravy


def pocet_tiku_levy():
    return pocitadlo.pocet("leva", pin14.read_digital())


def pocet_tiku_pravy():
    return pocitadlo.pocet("prava", pin15.read_digital())


def vypocti_rychlost(pocet_tiku, interval):
    otacky = pocet_tiku / 40
    uhel = otacky * 6.28
    rychlost = uhel / interval
    return rychlost  # vratte rychlost v radianech za sekundu
    
def aktualni_rychlost(interval):
    cas_zacatek = ticks_us()
    tiky_leve_kolo = pocet_tiku_levy()
    # tiky_prave_kolo = pocet_tiku_pravy()
    
    while int(ticks_diff(ticks_us(), cas_zacatek)/1000) < interval:
        pocet_tiku_levy()
        pocet_tiku_pravy()
        sleep(5)
    
    return vypocti_rychlost(pocet_tiku_levy() - tiky_leve_kolo, interval)


if __name__ == "__main__":

    pocitadlo = Pocitadlo_tiku()
    # aktualni_rychlost = 0
    perioda_cyklu_ms = 5
    interval_mereni = 166

    while True:
        print(aktualni_rychlost(interval_mereni))
        sleep(5)
