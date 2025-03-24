from microbit import sleep, pin14, pin15, i2c
from utime import ticks_us, ticks_diff

tiky_leva = 0                           # globalna premenna pocitadla L/P
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

def vypocti_rychlost(perioda):

    global tiky_prava

    rychlost_prava = (tiky_prava/40 * 6.283)/(perioda/1000)

    return rychlost_prava

if __name__ == "__main__":

    #test motora
    #i2c.init()
    #i2c.write(0x70, b'\x00\x01')
    #i2c.write(0x70, b'\xE8\xAA')
    #sleep(100)
    #i2c.write(0x70, b'\x03' + bytes([0]))

    aktualni_rychlost = 0
    cas_minule_print = ticks_us()              # setnem si aktualny cas
    perioda = 250                              # perioda merania nastavena na 250ms: nazbieram okolo 25 tickov, co je nad oporucanim 10-20.
                                               # prislo mi to ako lepsie rozlisenie nez 500, pri zachovani presnosti
                                               # stale je to celociselny podiel 1 sekundy, co je fajn pri tesrovani a preratavani
    while True:
        cas_ted = ticks_us()

        pocet_tiku_levy()                       # volam funkcie na meranie enkoderov, porovnanie stavov a zapis do pocitadla
        pocet_tiku_pravy()

        if ticks_diff(cas_ted, cas_minule_print) > perioda*1000:      # porovnavam casy, aby som vypisal hodnoty enkoderov iba raz za 500ms do terminalu

            print("Leva:",tiky_leva,"Prava:", tiky_prava)             # vypisem stavy pocitadiel L/P
            print("Rychlost:",vypocti_rychlost(perioda),"[rad/s]")
            tiky_prava = 0
            cas_minule_print = cas_ted

        sleep(5)

