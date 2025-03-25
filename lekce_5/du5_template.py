from microbit import sleep, pin14, pin15


celkovy_pocet_lava = 0
celkovy_pocet_prava = 0

predosly_stav_lava = 0
predosly_stav_prava = 0

counter = 0

aktualna_uhlova_rychlost = 0



def pocet_tiku_levy():
    global celkovy_pocet_lava, predosly_stav_lava
    surova_data_leva = pin14.read_digital()
    zmena = 0 if predosly_stav_lava == surova_data_leva else 1
    predosly_stav_lava = surova_data_leva
    celkovy_pocet_lava += zmena
    return celkovy_pocet_lava

def pocet_tiku_pravy():
    global celkovy_pocet_prava, predosly_stav_prava
    surova_data_prava = pin15.read_digital()
    zmena = 0 if predosly_stav_prava == surova_data_prava else 1
    predosly_stav_prava = surova_data_prava
    celkovy_pocet_prava += zmena
    return celkovy_pocet_prava
    
def vypocitaj_uhlovu_rychlost(pocet_tiku):
    global aktualna_uhlova_rychlost
    # zde patri ukol DU5
    aktualne_otacky = pocet_tiku/40
    aktualny_uhol = aktualne_otacky*6.28
    aktualna_uhlova_rychlost = aktualny_uhol*4
    
if __name__ == "__main__":

    while True:
        counter +=1
        pocet_tiku_levy()
        
        if counter == 50:
            vypocitaj_uhlovu_rychlost(pocet_tiku_levy())
            print (pocet_tiku_levy(), aktualna_uhlova_rychlost)
            counter=0
            celkovy_pocet_lava = 0
            aktualne_otacky = 0
        sleep(5)
