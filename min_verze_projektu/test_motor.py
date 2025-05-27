from time import sleep
from picoed import button_a
from motor import Motor
from konstanty import Konstanty


if __name__ == "__main__":
    motor_levy = Motor(Konstanty.LEVY)
    motor_levy.inicializuj_se()
    motor_levy.zastav()
    motor_levy.jed(Konstanty.DOPREDU, 150)
    sleep(1)
    motor_levy.zastav()
    sleep(1)
    motor_levy.jed(Konstanty.DOZADU, 150) 
    sleep(1)
    motor_levy.zastav()
    


