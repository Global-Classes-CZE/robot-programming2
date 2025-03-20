from microbit import sleep, pin14t, ticks_us, ticks_diff
import math  # Pro konstantu π

# Konstanta pro přepočet na úhel v radiánech
TWO_PI = 2 * math.pi  # Přesná hodnota 2π
# Celkový počet změn na senzoru
CELKOVY_POCET_TIKU = 40

# Perioda měření v mikrosekundách (180 ms = 180 000 us)
# Perioda je zvolena, tak že počítá s průměrnými rychlostmi které odpovídají 50 až 70 tik/s,
# což odopovídá průměrné rychlosti motoru, které budeme používat
PERIODA_US = 180000

def pocet_tiku_levy(predchozi_stav_levy, aktualni_stav_levy):
    """ Sleduje změny na enkodéru a přičítá tik při změně stavu. """
    pocet_tiku = 0
    if aktualni_stav_levy != predchozi_stav_levy:  # Pokud došlo ke změně
        pocet_tiku += 1
    return pocet_tiku# Vrací nový počet tiků a aktualizovaný stav



def pocet_tiku_pravy():
    surova_data_prava = pin15.read_digital()
    #zde napiste vas kod
    #scitejte tiky pro pravy enkoder od zacatku behu progamu
    return #vratte soucet

def vypocti_rychlost(pocet_tiku, perioda_us):
    # Přepočet tiků na počet otáček
    pocet_otacek = pocet_tiku / CELKOVY_POCET_TIKU
    # Přepočet na úhel v radiánech
    uhel_radiany = pocet_otacek * TWO_PI
    # Výpočet úhlové rychlosti (ω = rad/s)
    rychlost_rad_s = uhel_radiany / (perioda_us / 1000000)  # Převod us na s
    return round(rychlost_rad_s, 2)  # Zaokrouhlení na 2 desetinná místa
    
if __name__ == "__main__":
    aktualni_rychlost_leva = 0
    leve_tiky = 0
    predchozi_stav_levy = pin14.read_digital()
    cas_start = ticks_us()
    while True:
        # Neustálé čtení tiků (sběr dat)
        aktualni_stav_levy = pin14.read_digital()
        leve_tiky += pocet_tiku_levy(predchozi_stav_levy, aktualni_stav_levy)
        sleep(10)
        predchozi_stav_levy = aktualni_stav_levy
        # Zjistit aktuální čas
        cas_ted = ticks_us()
        # Pokud uplynula měřicí perioda, spočítat rychlost
        if ticks_diff(cas_ted, cas_start) >= PERIODA_US:
            # Výpočet rychlosti
            aktualni_rychlost_leva = vypocti_rychlost(leve_tiky, PERIODA_US)
            # Výpis hodnot
            print(f"Tiky levý: {leve_tiky} | Rychlost levý (rad/s): {aktualni_rychlost_leva}")
            # Resetování počtu tiků pro novou periodu
            leve_tiky = 0
            # Aktualizace času začátku nové periody
            cas_start = ticks_us()

        # Malá pauza pro omezení frekvence čtení
        sleep(5)

