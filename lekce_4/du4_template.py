from microbit import sleep, pin14, pin15

posledni_stav_levy = 0
posledni_stav_pravy = 0
tik_count_levy = 0
tik_count_pravy = 0

def pocet_tiku_levy():
    global posledni_stav_levy
    global tik_count_levy
    surova_data_leva = pin14.read_digital()
    if surova_data_leva != posledni_stav_levy:
        tik_count_levy += 1
    posledni_stav_levy = surova_data_leva
    return tik_count_levy

def pocet_tiku_pravy():
    global posledni_stav_pravy
    global tik_count_pravy
    surova_data_prava = pin15.read_digital()
    if surova_data_prava != posledni_stav_pravy:
        tik_count_pravy += 1
    posledni_stav_pravy =  surova_data_prava
    return tik_count_pravy

if __name__ == "__main__":


    while True:
        print(pocet_tiku_levy(), pocet_tiku_pravy())
        sleep(5)
