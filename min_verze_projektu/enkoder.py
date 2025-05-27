class Enkoder:
    def __init__(self, strana, perioda_rychlosti=0.5):
        self.strana = strana
        self.perioda_rychlosti = perioda_rychlosti*1000000  # na us

        self.tiky = 0
        self.posledni_hodnota = -1
        self.tiky_na_otocku = 40
        self.inicializovano = False
        self.cas_posledni_rychlosti = ticks_us()
        self.radiany_za_sekundu = 0

    def inicializuj(self):
        self.posledni_hodnota = self.aktualni_hodnota()
        self.inicializovano = True

    def aktualni_hodnota(self):
        if self.strana == K.PR_ENKODER:
            return pin15.read_digital()
        elif self.strana == K.LV_ENKODER:
            return pin14.read_digital()
        else:
            return -2

    def aktualizuj_se(self):
        if self.posledni_hodnota == -1:
            return -1

        aktualni_enkoder = self.aktualni_hodnota()
        if aktualni_enkoder >= 0:
            if self.posledni_hodnota != aktualni_enkoder:
                self.posledni_hodnota = aktualni_enkoder
                self.tiky += 1
        else:
            return aktualni_enkoder
        return 0

    def us_na_s(self, cas):
        return cas/1000000

    def vypocti_rychlost(self):
        cas_ted = ticks_us()
        interval_us = ticks_diff(cas_ted, self.cas_posledni_rychlosti)
        if interval_us >= self.perioda_rychlosti:
            interval_s = self.us_na_s(interval_us)
            otacky = self.tiky/self.tiky_na_otocku
            radiany = otacky * 2 * K.PI
            self.radiany_za_sekundu = radiany / interval_s
            self.tiky = 0
            self.cas_posledni_rychlosti = cas_ted

        return self.radiany_za_sekundu

