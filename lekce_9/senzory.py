from picoed import i2c

class Senzory:
    def __init__(self):
        self.__data_bit_string = ""
    
    def __byte_na_bity(self, buffer):
        data_int = int.from_bytes(buffer, "big")
        self.__data_bit_string = bin(data_int)

    def vycti_senzory(self):
        while not i2c.try_lock():
            pass

        # pokud se program dostane sem, tak se i2c podarilo zamknout
        try:
            buffer = bytearray(1)
            i2c.readfrom_into(0x38, buffer, start = 0, end = 1)
            self.__byte_na_bity(buffer)  
        finally:
            i2c.unlock()

        return self.__data_bit_string
    
    def vrat_levy(self):
        return bool(int(self.__data_bit_string[7]))

    def vrat_centralni(self):
        return bool(int(self.__data_bit_string[6]))

    def vrat_pravy(self):
        return bool(int(self.__data_bit_string[5]))