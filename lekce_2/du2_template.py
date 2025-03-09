from microbit import display

class Obrazovka:
    def vypis(text):
        print(text) #Vypíše text na konzoli
        display.scroll(text) #Vypíše text na display
