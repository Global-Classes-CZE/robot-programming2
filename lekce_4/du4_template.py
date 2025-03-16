from microbit import sleep, pin14, pin15

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

if __name__ == "__main__":

    while True:
        print(pocet_tiku_levy(), pocet_tiku_pravy())
        sleep(5)
