from picoed import i2c, button_a, button_b, display
from time import sleep, monotonic_ns
from cas import Cas
from senzory import Senzory
from robot import Robot

dopredna_pwm = 100
uhlova_max_pwm = 80
uhlova_min_pwm = 0

def vypis_senzory_cary(levy, centralni, pravy):
    print(levy, centralni, pravy)
    if levy:
        display.pixel(display.width-1,0, 255)
    else:
        display.pixel(display.width-1,0,0)

    if centralni:
        display.pixel(int(display.width/2),0, 255)
    else:
        display.pixel(int(display.width/2),0,0)
    
    if pravy:
        display.pixel(0,0, 255)
    else:
        display.pixel(0,0,0)

def stav_vycti_senzory(senzory):
    data_string = senzory.vycti_senzory()
    return data_string

def detekuj_krizovatku(senzory, data_string):
    data = senzory.vycti_senzory()
    kolik_senzoru_meri_caru = senzory.vrat_levy() + senzory.vrat_centralni() + senzory.vrat_pravy()
    return kolik_senzoru_meri_caru >=2

def stav_reaguj_na_caru(robot, senzory, data_string):
    if detekuj_krizovatku(senzory, data_string):
        return False
    
    if senzory.vrat_levy():
        robot.jed_pres_pwm("dopredu", uhlova_max_pwm, "dopredu", uhlova_min_pwm)        
        return True
    
    if senzory.vrat_pravy():
        robot.jed_pres_pwm("dopredu", uhlova_min_pwm, "dopredu", uhlova_max_pwm) 
        return True 
    
    if senzory.vrat_centralni():
        robot.jed_pres_pwm("dopredu", dopredna_pwm, "dopredu", dopredna_pwm) 
        return True 
    
    return True


if __name__ == "__main__":

    senzory = Senzory()
    robot = Robot()

    robot.inicializuj_se()
    
    aktualni_stav = "start"

    st_reaguj_na_caru = "reaguj na caru"
    st_vycti_senzory = "vycti senzory"
    st_stop = "st_stop"
    st_cekej = "st_cekej"
    st_popojed = "st_popojed"
    st_jedu = "st_jedu"
    st_pootoc = "st_pootoc"
    st_tocim = "st_tocim"
    st_zatoc_na_caru = "st_zatoc_na_caru"
    st_konec = "st_konec"

    cas_zastaveni = 0.5 #sekundy
    cas_popojeti = 0.3 #sekundy
    cas_pootoceni = 0.5 #sekundy
    prikazy = ["vlevo", "vpravo", "vpravo", "vpravo", "rovne"]
    aktualni_prikaz = 0

    while not button_a.was_pressed():
        print(aktualni_stav)
        data = stav_vycti_senzory(senzory)
        vypis_senzory_cary(senzory.vrat_levy(), senzory.vrat_centralni(), senzory.vrat_pravy())
        sleep(0.1)
        pass

    aktualni_stav = st_vycti_senzory

    while not button_b.was_pressed():
        if aktualni_stav == st_vycti_senzory:
            data = stav_vycti_senzory(senzory)
            vypis_senzory_cary(senzory.vrat_levy(), senzory.vrat_centralni(), senzory.vrat_pravy())
            aktualni_stav = st_reaguj_na_caru
            print(aktualni_stav)
        
        if aktualni_stav == st_reaguj_na_caru:
            pokracuj_jizda_po_care = stav_reaguj_na_caru(robot, senzory, data)
            if pokracuj_jizda_po_care:
                aktualni_stav = st_vycti_senzory
            else:
                aktualni_stav = st_stop
            print(aktualni_stav)
        
        if aktualni_stav == st_stop:
            robot.zastav()
            cas_zacatku_zastaveni = monotonic_ns()
            aktualni_stav = st_cekej
            print(aktualni_stav)
        
        if aktualni_stav == st_cekej:
            if Cas.ubehl_cas(monotonic_ns(), cas_zacatku_zastaveni, cas_zastaveni):
                robot.zastav()
                aktualni_stav = st_popojed
                print(aktualni_stav)
        
        if aktualni_stav == st_popojed:
            # DU 8  - naprogramujte zde
            robot.jed_pres_pwm("dopredu", dopredna_pwm, "dopredu", dopredna_pwm)
            cas_zacatku_jizdy = monotonic_ns()
            aktualni_stav = st_jedu
            print(aktualni_stav)
        
        if aktualni_stav == st_jedu:
            if Cas.ubehl_cas(monotonic_ns(), cas_zacatku_jizdy, cas_popojeti):
                robot.zastav()
                aktualni_stav = st_pootoc
                print(aktualni_stav)
        
        if aktualni_stav == st_pootoc:
            if len(prikazy) == aktualni_prikaz:
                #dosly prikazy
                aktualni_stav = st_konec
                print(aktualni_stav)
                continue
            if prikazy[aktualni_prikaz] == "rovne":
                aktualni_stav = st_vycti_senzory
                aktualni_prikaz += 1
                print(aktualni_stav)
            elif prikazy[aktualni_prikaz] == "vlevo":
                robot.jed_pres_pwm("dopredu", uhlova_max_pwm, "dozadu", uhlova_max_pwm)
                cas_zacatku_jizdy = monotonic_ns()
                aktualni_stav = st_tocim
                print(aktualni_stav)
            elif prikazy[aktualni_prikaz] == "vpravo":
                robot.jed_pres_pwm("dozadu", uhlova_max_pwm, "dopredu", uhlova_max_pwm)
                cas_zacatku_jizdy = monotonic_ns()
                aktualni_stav = st_tocim
                print(aktualni_stav)
            else:
                #neplatny prikaz
                aktualni_stav = st_konec
                print(aktualni_stav)
                continue
        
        if aktualni_stav == st_tocim:
            if Cas.ubehl_cas(monotonic_ns(), cas_zacatku_jizdy, cas_pootoceni):
                aktualni_stav = st_zatoc_na_caru
        
        if aktualni_stav == st_zatoc_na_caru:
            data = senzory.vycti_senzory()
            if prikazy[aktualni_prikaz] == "vlevo":
                if senzory.vrat_levy():
                    aktualni_prikaz += 1
                    robot.zastav()
                    aktualni_stav = st_vycti_senzory
            elif prikazy[aktualni_prikaz] == "vpravo":
                if senzory.vrat_pravy():
                    aktualni_prikaz += 1
                    robot.zastav()
                    aktualni_stav = st_vycti_senzory
        
        if aktualni_stav == st_konec:
            robot.zastav()
            print("Konec stavoveho automatu")
            break
        sleep(0.1)
    
    robot.zastav()

    

   



