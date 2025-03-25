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

def vypocti_rychlost(pocet_tiku, interval=1000000):
    interval_na_sekundy = interval / 1000000
    stupne = (pocet_tiku/40) * 360
    return radians(stupne)/interval_na_sekundy

if __name__ == "__main__":
    print("Zacatek programu")
    aktualni_rychlost = 0
    cas_minule = ticks_us()
    while True:
        pocet_tiku_levy()
        pocet_tiku_pravy()
        cas_ted = ticks_us()
        interval = 200000

        # kazdych 200ms vypise rychlost kol v radianech za sekundu
        if ticks_diff(cas_ted, cas_minule) > interval:
            aktualni_rychlost_levy = vypocti_rychlost(tiky_levy, interval)
            aktualni_rychlost_pravy = vypocti_rychlost(tiky_pravy, interval)
            nuluj_tiky()
            cas_minule = ticks_us()
            print(aktualni_rychlost_levy, aktualni_rychlost_pravy)
        sleep(5)
