from microbit import sleep, pin14, pin15
from utime import ticks_us, ticks_diff

tiky_leva = 0                           # globalna premenne pocitadla L/P
prev_data_leva = pin14.read_digital()   # globalna premenna stavu predosleho merania L/P

tiky_prava = 0
prev_data_prava = pin15.read_digital()

def pocet_tiku_levy():

    surova_data_leva = pin14.read_digital()

    global tiky_leva
    global prev_data_leva

    if surova_data_leva != prev_data_leva:
        tiky_leva += 1

    prev_data_leva = surova_data_leva

def pocet_tiku_pravy():

    surova_data_prava = pin15.read_digital()    #precitam enkoder a zapisem stav

    global tiky_prava                           #deklaracia globalnych premennych
    global prev_data_prava

    if surova_data_prava != prev_data_prava:    #porovnavam aktualny stav a predosly
        tiky_prava += 1                         #ked sa po sebe iduce stavy lisia, inkremantujem pocitadlo

    prev_data_prava = surova_data_prava         #pre dalsie porovnanie si odlozim do predoslej hodnoty cerstvo nameranu hodnotu enkodera

if __name__ == "__main__":

    cas_minule = ticks_us()                     #setnem si aktualny cas

    while True:

        cas_ted = ticks_us()

        pocet_tiku_levy()                       # volam funkcie na meranie enkoderov, porovnanie stavov a zapis do pocitadla
        pocet_tiku_pravy()

        if ticks_diff(cas_ted, cas_minule) > 500000:                    # porovnavam casy, aby som vypisal hodnoty enkoderov iba raz za 500ms do terminalu
            print("Leva:",tiky_leva,"Prava:", tiky_prava)               # vypisem stavy pocitadiel L/P
            cas_minule = cas_ted

