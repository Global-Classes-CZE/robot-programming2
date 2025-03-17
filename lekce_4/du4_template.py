from microbit import sleep, pin14, pin15

class Pocitadlo_tiku():
    
    def __init__(self):
        self._pocet_levy = 0
        self._pocet_pravy = 0
        self._posledni_leva = 0
        self._posledni_prava = 0
        
    def pocet(self, strana, data):
        if strana == "leva":
            if self._posledni_leva != data:
                self._posledni_leva = data
                self._pocet_levy += 1
                
            return self._pocet_levy
            
        if strana == "prava":
            if self._posledni_prava != data:
                self._posledni_prava = data
                self._pocet_pravy += 1
                
            return self._pocet_pravy

def pocet_tiku_levy():
    return pocitadlo.pocet("leva", pin14.read_digital())

def pocet_tiku_pravy():
    return pocitadlo.pocet("prava", pin15.read_digital())

if __name__ == "__main__":

    pocitadlo = Pocitadlo_tiku()

    while True:
        print(pocet_tiku_levy(), pocet_tiku_pravy())
        sleep(5)
