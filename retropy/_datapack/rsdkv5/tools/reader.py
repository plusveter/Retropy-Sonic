U8  = 2**(8*1) 
U16 = 2**(8*2)
U24 = 2**(8*3)
U32 = 2**(8*4)
U40 = 2**(8*5)
U48 = 2**(8*6)
U56 = 2**(8*7)
U64 = 2**(8*8)

class Reader:
    def __init__(self):
        self.pos = 0
        
    def read_selectbytes(self, data:bytes, lenght:int) -> bytes:
        self.pos += lenght
        return data[(self.pos-lenght):self.pos]

    def read_string_selectbytes(self, data:bytes, lenght:int) -> bytes:
        return str(self.read_selectbytes(data, lenght).decode())
    
    # _1bytes
    def read_Uint_1bytes(self, data:bytes) -> bytes:
        self.pos += 1
        return int(data[(self.pos-1)])

    def read_int_1bytes(self, data:bytes) -> bytes:
        i = self.read_Uint_1bytes(self, data)-U8
        if i > (U8/2): return i - U8
        return i

    # _2bytes
    def read_Uint_2bytes(self, data:bytes) -> bytes:
        number_8b = self.read_Uint_1bytes(data)
        number_16b = self.read_Uint_1bytes(data)*U8
        return number_8b + number_16b
    
    def read_int_2bytes(self, data:bytes) -> bytes:
        i =  self.read_Uint_2bytes(data)
        if i > (U16//2): return i - U16
        
        return i
    
    #_3bytes
    def read_Uint_3bytes(self, data:bytes) -> bytes:
        number_8b = self.read_Uint_1bytes(data)
        number_16b = self.read_Uint_1bytes(data)*U8
        number_24b = self.read_Uint_1bytes(data)*U16
        return number_8b + number_16b + number_24b

    def read_int_3bytes(self, data:bytes) -> bytes:
        i =  self.read_Uint_3bytes(data)
        if i > (U24/2): return i - U24
        return i
    
    #_4bytes
    def read_Uint_4bytes(self, data:bytes) -> bytes:
        number_8b = self.read_Uint_1bytes(data)
        number_16b = self.read_Uint_1bytes(data)*U8
        number_24b = self.read_Uint_1bytes(data)*U16
        number_32b = self.read_Uint_1bytes(data)*U24
        return number_8b + number_16b + number_24b + number_32b
    
    def read_int_4bytes(self, data:bytes) -> bytes:
        i =  self.read_Uint_4bytes(data)
        if i > (U32/2): return i - U32
        return i

    #_5bytes
    def read_Uint_5bytes(self, data:bytes) -> bytes:
        number_8b = self.read_Uint_1bytes(data)
        number_16b = self.read_Uint_1bytes(data)*U8
        number_24b = self.read_Uint_1bytes(data)*U16
        number_32b = self.read_Uint_1bytes(data)*U24
        number_40b = self.read_Uint_1bytes(data)*U32
        return number_8b + number_16b + number_24b + number_32b + number_40b

    def read_int_5bytes(self, data:bytes) -> bytes:
        i =  self.read_Uint_5bytes(data)
        if i > (U40/2): return i - U40
        return i
    
    #_6bytes
    def read_Uint_6bytes(self, data:bytes) -> bytes:
        number_8b = self.read_Uint_1bytes(data)
        number_16b = self.read_Uint_1bytes(data)*U8
        number_24b = self.read_Uint_1bytes(data)*U16
        number_32b = self.read_Uint_1bytes(data)*U24
        number_40b = self.read_Uint_1bytes(data)*U32
        number_48b = self.read_Uint_1bytes(data)*U40
        return number_8b + number_16b + number_24b + number_32b + number_40b + number_48b
    
    def read_int_6bytes(self, data:bytes) -> bytes:
        i =  self.read_Uint_6bytes(data)
        if i > (U48/2): return i - U48
        return i
    
    #_7bytes
    def read_Uint_7bytes(self, data:bytes) -> bytes:
        number_8b = self.read_Uint_1bytes(data)
        number_16b = self.read_Uint_1bytes(data)*U8
        number_24b = self.read_Uint_1bytes(data)*U16
        number_32b = self.read_Uint_1bytes(data)*U24
        number_40b = self.read_Uint_1bytes(data)*U32
        number_48b = self.read_Uint_1bytes(data)*U40
        number_56b = self.read_Uint_1bytes(data)*U48
        return number_8b + number_16b + number_24b + number_32b + number_40b + number_48b + number_56b

    def read_int_7bytes(self, data:bytes) -> bytes:
        i =  self.read_Uint_7bytes(data)
        if i > (U56/2): return i - U56
        return i

    #_8bytes
    def read_Uint_8bytes(self, data:bytes) -> bytes:
        number_8b = self.read_Uint_1bytes(data)
        number_16b = self.read_Uint_1bytes(data)*U8
        number_24b = self.read_Uint_1bytes(data)*U16
        number_32b = self.read_Uint_1bytes(data)*U24
        number_40b = self.read_Uint_1bytes(data)*U32
        number_48b = self.read_Uint_1bytes(data)*U40
        number_56b = self.read_Uint_1bytes(data)*U48
        number_64b = self.read_Uint_1bytes(data)*U56
        return number_8b + number_16b + number_24b + number_32b + number_40b + number_48b + number_56b + number_64b 

    def read_int_8bytes(self, data:bytes) -> bytes:
        i =  self.read_Uint_8bytes(data)
        if i > (U64/2): return i - U64
        return i