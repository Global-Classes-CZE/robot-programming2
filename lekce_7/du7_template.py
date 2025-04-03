from picoed import i2c
from time import sleep

def init_motoru():
    while not i2c.try_lock():
        pass
    try:
        i2c.writeto(0x70, bytes([0, 0x01]))
        i2c.writeto(0x70, bytes([8, 0xAA]))
        sleep(0.01)
    finally:
        i2c.unlock()
 
def jed(dopredna, uhlova):
    prumer_kol = 65 # milimetry
    polomer_vozu = 75 # milimetry
    v_l = dopredna - polomer_vozu * uhlova # milimetry / sekunda
    v_r = dopredna + polomer_vozu * uhlova # milimetry / sekunda
    if v_l >=0 :
        smer_l = "dopredu"
        rychlost_l = v_l / prumer_kol # radiany / sekunda
    else:
        smer_l = "dozadu"
        rychlost_l = - v_l / prumer_kol # radiany / sekunda

    if v_r >=0 :
        smer_r = "dopredu"
        rychlost_r = v_r / prumer_kol # radiany / sekunda
    else:
        smer_r = "dozadu"
        rychlost_r = - v_r / prumer_kol # radiany / sekunda
    print ("dopredna: ",dopredna, " uhlova: ",uhlova, "vyvola")
    print ("jed_rad_sec( leva, " ,smer_l,", ", rychlost_l,")")
    print ("jed_rad_sec( prava, " ,smer_r,", ", rychlost_r,")")
    jed_rad_sec("prava", smer_r,rychlost_r)
    jed_rad_sec("leva", smer_l,rychlost_l)
    return 0

def jed_rad_sec(strana, smer, rychlost): #prepocet z radianu na pwm neni hotove
    if rychlost < 1:
        pwm_rychlost = 0
    else:
        pwm_rychlost = 127
    jed_pwm(strana, smer, pwm_rychlost)
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

if __name__ == "__main__":
    # Write your code here :-)
    init_motoru()
    # volejte funkci jed, tak abyste ziskali:
    # Pohyb robota dopredu 1s
    jed(200,0)
    sleep(1)
    # Zastaveni 1s - DULEZITE! Nikdy nemente smer jizdy bez zastaveni
    jed(0,0)
    sleep(1)
    # Otáčení robota na místě doleva
    jed(0,150)
    sleep(1)
    # zastaveni
    jed(0,0)


