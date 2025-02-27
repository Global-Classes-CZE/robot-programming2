from microbit import display

class Obrazovka:
    def vypis(text):
        display.scroll(text)  # Výpis na micro:bit
        print(text)  # Výpis do terminálu

