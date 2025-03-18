from microbit import sleep, pin14, pin15
from utime import ticks_us, ticks_diff


def pocet_tiku_levy(tiky_leva, stav_leva):

    sum_leva = tiky_leva
    prev_data_leva = stav_leva

    surova_data_leva = pin14.read_digital()

    if surova_data_leva != prev_data_leva:
        sum_leva += 1

    prev_data_leva = surova_data_leva

    return sum_leva, prev_data_leva

def pocet_tiku_pravy(tiky_prava, stav_prava):   #poslal som si lokalne premenne z __main__

    sum_prava = tiky_prava                      #lokalnu premennu v pocitadle sum_prava zosynchronizujem s tiky_prava; lebo tato lokalna premenna sa vynuluje vzdy, ked sa zavola funkcia ak to neurobim
    prev_data_prava = stav_prava                #rovnako zosycnhronizujem predosly stav enkodera

    surova_data_prava = pin15.read_digital()    #precitam enkoder znova a zapisem stav

    if surova_data_prava != prev_data_prava:    #ked su zname aspon 2 stavy, porovnavam
        sum_prava += 1                          #ked sa po sebe iduce stavy lisia, inkremantujem pocitadlo

    prev_data_prava = surova_data_prava         #pre dalsie porovnanie si odlozim predoslu hodnotu enkodera

    return sum_prava, prev_data_prava           #z funkcie vratim lokalne pocitadlo a predosly stav, ktore sa zapisu do lokalnych premennych v maine

if __name__ == "__main__":

    cas_minule = ticks_us()                     #setnem si aktualny cas

    tiky_prava = 0                              #vynulujem pocitadlo
    stav_prava = pin15.read_digital()           #setnem pociatocny stav praveho enkodera

    tiky_leva = 0
    stav_leva = pin14.read_digital()

    while True:

        tiky_prava, stav_prava = pocet_tiku_pravy(tiky_prava, stav_prava) #idem inkrementovat stav lokalnej premennej tiky_prava a ulozim si aj aktualny stav posledneho citania hodnoty enkodera; hodnoty posielam do funkcie
        tiky_leva, stav_leva = pocet_tiku_levy(tiky_leva, stav_leva)

        cas_ted = ticks_us()

        if ticks_diff(cas_ted, cas_minule) > 500000:                      # porovnavam casy, aby som vypisal hodnoty enkoderov iba raz za 500ms do terminalu
            print("Leva:",tiky_leva,"Prava:", tiky_prava)
            cas_minule = cas_ted

