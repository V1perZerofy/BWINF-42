def read_construction_file(filename):
    lightcount = 0
    with open(filename, 'r') as f:
        n, m = map(int, f.readline().strip().split())
        construction = [list(f.readline().strip().split()) for _ in range(m)]
        
        for i in construction[0]:
            if i.startswith('Q'):
                lightcount += 1
    return n, m, construction, lightcount

def interpretConstruction(n, m, construction, startingLight, lightcount):
    lightrow = ['O'] * n
    for i in range(len(construction[0])):
        if construction[0][i].startswith('Q'):
            idx = int(construction[0][i][-1]) - 1
            if 0 <= idx < lightcount:
                lightrow[i] = 'l' if startingLight[idx] == '1' else 'O'
        if construction[0][i].startswith('X'):
            lightrow[i] = 'O'
    startrow = lightrow.copy()
    for i in construction[1:-1]:
        for j in range(len(i)):
            if j < len(i) - 1:
                if i[j] == 'R' and i[j+1] == 'r':
                    if lightrow[j] == 'O':
                        lightrow[j] = 'l'
                        lightrow[j+1] = 'l'
                    else:
                        lightrow[j] = 'O'
                        lightrow[j+1] = 'O'
                if i[j] == 'r' and i[j+1] == 'R':
                    if lightrow[j+1] == 'O':
                        lightrow[j] = 'l'
                        lightrow[j+1] = 'l'
                    else:
                        lightrow[j] = 'O'
                        lightrow[j+1] = 'O'
            if i[j] == 'W' and i[j+1] == 'W':
                if lightrow[j] == 'O' and lightrow[j+1] == 'O':
                    lightrow[j] = 'l'
                    lightrow[j+1] = 'l'
                elif lightrow[j] == 'l' and lightrow[j+1] == 'l':
                    lightrow[j] = 'O'
                    lightrow[j+1] = 'O'
                else:
                    lightrow[j] = 'l'
                    lightrow[j+1] = 'l'
            if i[j] == 'X':
                lightrow[j] = 'O'
        #print(lightrow)
    final_leds = ['L' if lightrow[led_item] == 'l' and construction[-1][led_item].startswith("L") else 'X' if construction[-1][led_item].startswith("L") else '' for led_item in range(len(lightrow))]
    return final_leds

def test_all_flashlight_combinations(n, m, construction, lightcount):
    print("Testing all flashlight combinations: ")
    print("Start" + " -> " + "End")
    for i in range(2**lightcount):
        flashlights = bin(i)[2:].zfill(lightcount)
        final_leds = interpretConstruction(n, m, construction, flashlights, lightcount)
        print(flashlights + " -> " +  "".join(final_leds))

n, m, construction, lightcount = read_construction_file("bwinf.de_fileadmin_user_upload_nandu1.txt")
test_all_flashlight_combinations(n, m, construction, lightcount)
