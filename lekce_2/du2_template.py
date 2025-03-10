from microbit import display

class Obrazovka:
    def vypis(text):
        display.scroll(text)
        print(text)