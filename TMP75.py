from machine import I2C, Pin

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)  
ADDRESS = 0x48

def read_temp():
    try:
        raw = i2c.readfrom_mem(ADDRESS, 0x00, 2)

        temp_raw = (raw[0] << 4) | (raw[1] >> 4)
        
        if temp_raw & 0x800: 
            temp_raw -= 4096
            
        temperature = temp_raw * 0.0625
        return round(temperature, 2)
        
    except Exception as e:
        print("Temperatur-Lesefehler:", e)
        return None
