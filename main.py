from ShtServer import TemperatureStation

def main():
    """Hauptfunktion"""
    station = TemperatureStation()
    station.start()

if __name__ == "__main__":
    main()