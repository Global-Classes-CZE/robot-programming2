from picoed import button_a, button_b, i2c
from time import sleep, monotonic_ns
from board import P8, P12
from digitalio import DigitalInOut, Direction
from ultrazvuk import Ultrazvuk
from math import fabs


pul_rozchod_kol = 0.075 # vzdalenost stredu kola od stredu robota

def init_motoru():
    while not i2c.try_lock():
        pass
    try:
        i2c.writeto(0x70, b'\x00\x01')
        i2c.writeto(0x70, b'\xE8\xAA')
        sleep(0.1)
    finally:
        i2c.unlock()

def jed(dopredna, uhlova):
    v_l = dopredna - pul_rozchod_kol * uhlova
    v_r = dopredna + pul_rozchod_kol * uhlova

    if v_l == 0 and v_r == 0:
        jed_pwm("leva", "dopredu", 0)
        jed_pwm("prava", "dopredu", 0)
    else:
        if v_l >= 0:
            l_smer = "dopredu"
        else:
            l_smer = "dozadu"
        if v_r >= 0:
            r_smer = "dopredu"
        else:
            r_smer = "dozadu"

        jed_pwm("leva", l_smer, int(fabs(v_l)))
        jed_pwm("prava", r_smer, int(fabs(v_r)))

    return 0

def jed_pwm(strana, smer, rychlost):
    if (rychlost >= 0 and rychlost <= 255):
        if (strana == "leva" and smer == "dopredu"):
            nastav_kanaly(4, 5, rychlost)
            return 0
        elif (strana == "leva" and smer == "dozadu"):
            nastav_kanaly(5, 4, rychlost)
            return 0
        elif (strana == "prava" and smer == "dopredu"):
            nastav_kanaly(2, 3, rychlost)
            return 0
        elif (strana == "prava" and smer == "dozadu"):
            nastav_kanaly(3, 2, rychlost) 
            return 0
        else:
            return -1
    else:
        return -2

def nastav_kanaly(kanal_off, kanal_on, rychlost):
    while not i2c.try_lock():
        pass
    try:
        i2c.writeto(0x70, bytes([kanal_off, 0]))
        i2c.writeto(0x70, bytes([kanal_on, rychlost]))
    finally:
        i2c.unlock()
    return 0

def zastav():
    jed(0, 0)

def sign(num):
    return -1 if num < 0 else 1

if __name__ == "__main__":
    init_motoru()
    zastav()
    while not button_b.was_pressed():
        pass
    ultrazvuk = Ultrazvuk(DigitalInOut(P8), DigitalInOut(P12))

    reference = 0.2 # na jakou vzdalenost cheme zastavit [m]
    P = -300
    max_PWM = 150 #teoreticky 255, ale ja se bojim :)
    min_PWM = 80 # idealne zjisteno kalibraci, nebo vypozorovano, kdy se robot odlepi
    mrtva_zona = 0.05 #napr 5cm - kdy regulace uz rekne "uz tu jsem" a prestane regulovat

    predchozi_akcni_zasah = 0 #potrebuji, abych osetrila, ze motory se nikdy nerozjedou skokove do protismeru
    
    while not button_a.was_pressed():
        merena_vzdalenost = ultrazvuk.proved_mereni_blokujici(timeout=0.01)
        if merena_vzdalenost < 0:
            print("error")
            continue
        else:
            error = reference - merena_vzdalenost
            akcni_zasah = P * error
            if fabs(akcni_zasah) > max_PWM:
                akcni_zasah = sign(akcni_zasah) * max_PWM
            if fabs(akcni_zasah) < min_PWM:
                if fabs(error) > mrtva_zona:
                    akcni_zasah = sign(akcni_zasah) * min_PWM
                else:
                    akcni_zasah = 0
            

            # osetreni, ze nikdy motory neposleme do protismeru hned
            # normalne bych tohle v regulaci nemela,
            # zde to mame, protoze nase motory jsou dost blbe
            if sign(predchozi_akcni_zasah) != sign(akcni_zasah):
                zastav()
                
            jed(fabs(akcni_zasah), 0)

            predchozi_akcni_zasah = akcni_zasah

        sleep(0.05)
    
    zastav()