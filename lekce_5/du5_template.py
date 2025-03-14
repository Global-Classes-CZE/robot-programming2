from microbit import sleep, pin14, pin15
from utime import ticks_diff, ticks_us
from math import radians

tiky_levy = 0
predesla_hodnota_levy = 0
tiky_pravy = 0
predesla_hodnota_pravy = 0

def pocet_tiku_levy():
    global tiky_levy, predesla_hodnota_levy
    surova_data_leva = pin14.read_digital()
    if surova_data_leva != predesla_hodnota_levy:
        tiky_levy += 1
        predesla_hodnota_levy = surova_data_leva
    return tiky_levy

def pocet_tiku_pravy():
    global tiky_pravy, predesla_hodnota_pravy
    surova_data_prava = pin15.read_digital()
    if surova_data_prava != predesla_hodnota_pravy:
        tiky_pravy += 1
        predesla_hodnota_pravy = surova_data_prava
    return tiky_pravy

def nuluj_tiky():
    global tiky_levy, tiky_pravy
    tiky_levy = 0
    tiky_pravy = 0

def vypocti_rychlost(pocet_tiku):
    stupne = (pocet_tiku/40) * 360
    return radians(stupne)

if __name__ == "__main__":
    print("Zacatek programu")
    aktualni_rychlost = 0
    cas_minule = ticks_us()
    while True:
        pocet_tiku_levy()
        pocet_tiku_pravy()
        cas_ted = ticks_us()

        # kazdou vterinu vypise rychlost kol v radianech za sekundu
        # kdybychom meli jinou periodu vypisu, tak musime danou rychlost vynasobit pomernym faktorem 1s/perioda_vypisu
        if ticks_diff(cas_ted, cas_minule) > 1000000:
            aktualni_rychlost_levy = vypocti_rychlost(tiky_levy)
            aktualni_rychlost_pravy = vypocti_rychlost(tiky_pravy)
            nuluj_tiky()
            cas_minule = ticks_us()
            print(aktualni_rychlost_levy, aktualni_rychlost_pravy)
        sleep(5)
