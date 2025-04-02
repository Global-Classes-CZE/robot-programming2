from microbit import sleep, pin14, pin15
from utime import ticks_us, ticks_diff

posledni_l = pin14.read_digital()
posledni_p = pin14.read_digital()
pocet_l = 0
pocet_p = 0

def pocet_tiku_levy():
    global posledni_l
    global pocet_l
    surova_data_leva = pin14.read_digital()
    if surova_data_leva != posledni_l:
        pocet_l +=1
    posledni_l = surova_data_leva
    return pocet_l #vratte soucet

def pocet_tiku_pravy():
    global posledni_p
    global pocet_p
    surova_data_prava = pin15.read_digital()
    if surova_data_prava != posledni_p:
        pocet_p +=1
    posledni_p = surova_data_prava
    return pocet_p #vratte soucet

def vypocti_rychlost(pocet_tiku, ubehly_cas, tpr):

    vypoctena_rychlost = 2 * 3.1415 * pocet_tiku / tpr / ubehly_cas

    return vypoctena_rychlost

if __name__ == "__main__":

    aktualni_rychlost_leva = 0
    aktualni_rychlost_prava = 0
    minuly_cas = ticks_us() #aktualni cas
    perioda = 0.33 #cas v sekundach
    otacka_tick = 40 #kolik je tiku za otacku

    while True:
        pritomny_cas = ticks_us()
        if ticks_diff(pritomny_cas, minuly_cas) > perioda*1000000:
            aktualni_rychlost_leva = vypocti_rychlost(tic_Per_levy,perioda,otacka_tick)
            aktualni_rychlost_prava = vypocti_rychlost(tic_Per_pravy,perioda,otacka_tick)
            print('leve kolo: ',aktualni_rychlost_leva,' rad/sec prave kolo: ',aktualni_rychlost_prava,' rad/sec')
            pocet_l = 0
            pocet_p = 0
            minuly_cas = pritomny_cas
        #volejte zde funkci aktualni_rychlost = vypocti_rychlost s vhodnou peridou - viz slidy min 166ms;
        #volejte zde funkci aktualni_rychlost = vypocti_rychlost s vhodnou peridou - viz slidy min 166ms;
        #budete potrebovat vyuzit praci s casem pres tick_us, ticks_diff (mozna prikazy jsou jinak na pico:edu, pokud nenajdete, zeptejte se na discordu)
        #staci udelat pro jedno kolo

        #print(aktualni_rychlost)
        tic_Per_pravy = pocet_tiku_pravy()
        tic_Per_levy = pocet_tiku_levy()
        sleep(5)
