from microbit import sleep, pin14, pin15

predchozi_stav_tiku_levy = pin14.read_digital()
predchozi_stav_tiku_pravy = pin15.read_digital()
soucet_tiku_levy = 0
soucet_tiku_pravy = 0

def pocet_tiku_levy():
    global predchozi_stav_tiku_levy, soucet_tiku_levy
    surova_data_levy = pin14.read_digital()
    if surova_data_levy != predchozi_stav_tiku_levy:
        soucet_tiku_levy += 1
        predchozi_stav_tiku_levy = surova_data_levy
    return soucet_tiku_levy

def pocet_tiku_pravy():
    global predchozi_stav_tiku_pravy, soucet_tiku_pravy
    surova_data_pravy = pin15.read_digital()
    if surova_data_pravy != predchozi_stav_tiku_pravy:
        soucet_tiku_pravy += 1
        predchozi_stav_tiku_pravy = surova_data_pravy
    return soucet_tiku_pravy

if __name__ == "__main__":

    while True:
        print(pocet_tiku_levy(), pocet_tiku_pravy())
        sleep(5)