from machine import I2C, Pin

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)  
ADDRESS = 0x48

def read_temp():
  
    try:
        raw = i2c.readfrom_mem(ADDRESS, 0x00, 2)
        value = (raw[0] << 8) | raw[1]
        temp_raw = value >> 7
        if temp_raw & (1 << 8):
            temp_raw -= 1 << 9
        return (temp_raw * 0.5) -1
    except Exception as e:
        print("Fehler beim Lesen der Temperatur:", e)
        return None
