from microbit import i2c, sleep

def init_motoru():
    i2c.write(0x70, b'\x00\x01')
    i2c.write(0x70, b'\xE8\xAA')
    sleep(100)

def jed(strana, smer, rychlost):
    # Strana může být jen “leva” a “prava”
    # “smer” je typu string a může mít hodnoty “dopredu”, "dozadu"
    # Rychlost je celočíselné číslo od 0-255
    # vyuzijte prikladu z hodiny, ktery poslal povel x03 - prave kolo pro jizdu rovne
    # ostatni povely:

    # Levý motor:
    # 0x04 - příkaz pro pohyb vzad
    # 0x05 - příkaz pro pohyb vpřed

    if (strana == "leva"):
       print("leva")
       if smer == "dopredu":
            print("dopredu")
            i2c.write(0x70, b'\x05' + bytes([rychlost]))
       elif smer == "dozadu":
            print("dozadu")
            i2c.write(0x70, b'\x04' + bytes([rychlost]))
       else:
            print("nemam smer")

    elif strana == "prava":
    # Pravý motor:
    # 0x02 - příkaz pro pohyb vzad
    # 0x03 - příkaz pohyb vpřed

       print("prava")
       if smer == "dopredu":
            print("dopredu")
            i2c.write(0x70, b'\x03' + bytes([rychlost]))
       elif smer == "dozadu":
            print("dozadu")
            i2c.write(0x70, b'\x02' + bytes([rychlost]))
       else:
           print("nemam smer")
    else:
        print("nemam stranu")





if __name__ == "__main__":
    # Write your code here :-)
    i2c.init()
    init_motoru()
    # volejte funkci jed, tak abyste ziskali:
    # Pohyb robota dopredu 1s
    jed("leva","dopredu",100)
    jed("prava","dopredu",100)
    sleep(1000)
    # Zastaveni 1s - DULEZITE! Nikdy nemente smer jizdy bez zastaveni
    jed("leva","dopredu",0)
    jed("prava","dopredu",0)
    sleep(1000)

    # Pohyb vzad 1s,
    jed("leva","dozadu",100)
    jed("prava","dozadu",100)
    sleep(1000)
    # Zastaveni 1s - DULEZITE! Nikdy nemente smer jizdy bez zastaveni
    jed("leva","dozadu",0)
    jed("prava","dozadu",0)
    sleep(1000)
    # zastaveni
