from microbit import sleep, pin14, pin15
from utime import ticks_us, ticks_diff
# deklarace globalnich promennych
pocet_tiku_leva = 0
pocet_tiku_prava = 0
posledni_stav_leva = pin14.read_digital()
posledni_stav_prava = pin15.read_digital()


def pocet_tiku_levy():
# funkce pocitani tiku leva strana

    surova_data_leva = pin14.read_digital()
    global pocet_tiku_leva
    global posledni_stav_leva
    if posledni_stav_leva != surova_data_leva:
        pocet_tiku_leva += 1
        posledni_stav_leva = surova_data_leva

    return pocet_tiku_leva


def pocet_tiku_pravy():
# funkce pocitani tiku prava strana

    surova_data_prava = pin15.read_digital()
    global pocet_tiku_prava
    global posledni_stav_prava

    if posledni_stav_prava != surova_data_prava:
        pocet_tiku_prava += 1
        posledni_stav_prava = surova_data_prava

    return pocet_tiku_prava

def vypocti_rychlost(pocet_tiku, delka_periody):
    aktualni_pocet_otacek = pocet_tiku/40
    aktualni_uhel = aktualni_pocet_otacek*6.28
    rychlost_v_radianech = (aktualni_uhel/delka_periody)*1000000
    return rychlost_v_radianech

if __name__ == "__main__":

    aktualni_rychlost = 0
    cas_minule = ticks_us()
    pocet_tiku_predchozi = 0

    while True:
        cas_ted = ticks_us()
        perioda = ticks_diff(cas_ted, cas_minule)
        aktualni_soucet_tiky = pocet_tiku_levy()
        if perioda  > 200000:
           #print(perioda, cas_ted)
           pocet_tiku = aktualni_soucet_tiky - pocet_tiku_predchozi
           pocet_tiku_predchozi = aktualni_soucet_tiky
           cas_minule = cas_ted
           aktualni_rychlost = vypocti_rychlost(pocet_tiku, perioda)
           print("uhlova rychlost", aktualni_rychlost)
        sleep(5)
