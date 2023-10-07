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
    #return lightrow
    for i in construction[1:-1]:
        for j in range(len(i)):
            if i[j] == 'W':
                if lightrow[j] == 'l':


def test_all_flashlight_combinations(n, m, construction, lightcount):
    for i in range(2**lightcount):
        flashlights = bin(i)[2:].zfill(lightcount)
        final_leds = interpretConstruction(n, m, construction, flashlights, lightcount)
        print("".join(final_leds), flashlights)

n, m, construction, lightcount = read_construction_file("bwinf.de_fileadmin_user_upload_nandu1.txt")
test_all_flashlight_combinations(n, m, construction, lightcount)
