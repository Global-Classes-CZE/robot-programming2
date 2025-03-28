from board import P14, P15
from digitalio import DigitalInOut
from time import sleep, time

levy_enkoder = DigitalInOut(P14)
pravy_enkoder = DigitalInOut(P15)

perioda_sec = 0.5   # Tuto periodu jsem si vybral na zaklade doporuceni lektorky v hodine. Za tento cas nasbirame dostatecny pocet tiku s nasim 40 stavovym enkoderem. Zaroven vsak relativne vyloucime chybu zprumerovani vlivem kolisani rychlosti.

predchozi_stav_tiku_levy = levy_enkoder.value
predchozi_stav_tiku_pravy = pravy_enkoder.value
soucet_tiku_levy = 0
soucet_tiku_pravy = 0

def pocet_tiku_levy():
    global predchozi_stav_tiku_levy, soucet_tiku_levy
    surova_data_levy = levy_enkoder.value
    if surova_data_levy != predchozi_stav_tiku_levy:
        soucet_tiku_levy += 1
        predchozi_stav_tiku_levy = surova_data_levy
    return soucet_tiku_levy

def pocet_tiku_pravy():
    global predchozi_stav_tiku_pravy, soucet_tiku_pravy
    surova_data_pravy = pravy_enkoder.value
    if surova_data_pravy != predchozi_stav_tiku_pravy:
        soucet_tiku_pravy += 1
        predchozi_stav_tiku_pravy = surova_data_pravy
    return soucet_tiku_pravy

def vypocti_rychlost(pocet_tiku):
    rad_za_sec = ((360/40) * (pocet_tiku / perioda_sec)) * (3.14/180)  # zde patri ukol DU5
    return rad_za_sec #vratte rychlost v radianech za sekundu

def aktualni_rychlost():
    global soucet_tiku_levy, soucet_tiku_pravy    
    cas_ted = time()
    while time() - cas_ted < perioda_sec:
        pocet_tiku_levy()
        pocet_tiku_pravy()
        sleep(0.005)
    soucet_za_periodu_levy = soucet_tiku_levy
    soucet_za_periodu_pravy = soucet_tiku_pravy
    soucet_tiku_levy = 0
    soucet_tiku_pravy = 0

    aktualni_rychlost_levy = vypocti_rychlost(soucet_za_periodu_levy)
    aktualni_rychlost_pravy = vypocti_rychlost(soucet_za_periodu_pravy)
    return aktualni_rychlost_levy, aktualni_rychlost_pravy   

if __name__ == "__main__":
    
    while True:
        print(aktualni_rychlost())
        sleep(5)
