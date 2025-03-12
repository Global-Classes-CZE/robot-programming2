from board import P14, P15
from digitalio import DigitalInOut
from time import sleep

if __name__ == "__main__":

    levy_enkoder = DigitalInOut(P14)
    pravy_enkoder = DigitalInOut(P15)

    while True:
        surova_data_leva = int(levy_enkoder.value)
        surova_data_prava = int(pravy_enkoder.value)
        print(surova_data_leva, surova_data_prava)
        sleep(0.1)
        