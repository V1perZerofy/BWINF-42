def read_construction_file(filename):
    with open(filename, 'r') as f:
        # Erste Zeile für Breite und Höhe einlesen
        n, m = map(int, f.readline().strip().split())
        
        # Restliche Zeilen für die Konstruktion einlesen
        construction = [list(f.readline().strip().split()) for i in range(m)]
        
    return n, m, construction

def interpret_construction(n, m, construction, flashlights):
    # Initialisiere die LEDs auf der untersten Reihe
    leds = ['O'] * n  # O für ausgeschaltet
            
    for row in reversed(construction[1:-1]):
        for i in range(0, n):
            block_type = row[i]
            # Interpretiere die Regeln für jeden Baustein-Typ
            if block_type == 'W':
                if flashlights[i] == 'I':  # Beide Sensoren sind bestrahlt
                    leds[i] = 'O'
                else:  # Keiner oder nur ein Sensor ist bestrahlt
                    leds[i] = 'I'  # I für eingeschaltet
            elif block_type == 'B':
                if flashlights[i] == 'I':  # Nur der obere Sensor ist bestrahlt
                    leds[i] = 'I'
                else:  # Nur der untere oder kein Sensor ist bestrahlt
                    leds[i] = 'I'
            elif block_type == 'r' or block_type == 'R':
                if flashlights[i] == 'I':  # Der Sensor ist bestrahlt
                    leds[i] = 'O'
                else:  # Der Sensor ist nicht bestrahlt
                    leds[i] = 'I'
                    
    # Letzte Reihe ist für LEDs
    final_leds = [led if led_item == 'L' else 'X' for led, led_item in zip(leds, construction[-1])]
    return final_leds

#testenaller start lampen möglichkeiten
def test_all_flashlight_combinations(n, m, construction):
    # Teste alle Kombinationen von Lampen
    for i in range(2**n):
        flashlights = list(bin(i)[2:].zfill(n))
        final_leds = interpret_construction(n, m, construction, flashlights)
        print("".join(final_leds), flashlights)

n, m, construction = read_construction_file("bwinf.de_fileadmin_user_upload_nandu1.txt")
test_all_flashlight_combinations(n, m, construction)