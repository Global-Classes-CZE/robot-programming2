from microbit import display

class Obrazovka:
    def vypis(text):
        print(text)
        display.scroll(text)

    vypis("Ahoj !")

        
