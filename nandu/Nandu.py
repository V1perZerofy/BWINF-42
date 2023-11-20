import time

def read_construction_file(filename): #read the construction file and return the number of rows, number of columns, the construction, and the number of lights
    lightcount = 0 #number of lights
    with open(filename, 'r') as f: #open the file
        n, m = map(int, f.readline().strip().split()) #read the first line and get the number of rows and columns
        construction = [list(f.readline().strip().split()) for _ in range(m)] #read the construction
        
        for i in construction[0]: #for each item in the first row of the construction
            if i.startswith('Q'): #if the item starts with Q
                lightcount += 1 #increment the number of lights
    return n, m, construction, lightcount #return the number of rows, number of columns, the construction, and the number of lights

def interpretConstruction(n, m, construction, startingLight, lightcount): #interpret the construction and return the final state of the LEDs
    lightrow = ['O'] * n #create a list of length n with all items set to O
    for i in range(len(construction[0])): #for each item in the first row of the construction
        if construction[0][i].startswith('Q'): #if the item starts with Q
            idx = int(construction[0][i][-1]) - 1 #get the index of the light
            if 0 <= idx < lightcount: #if the index is valid  
                lightrow[i] = 'l' if startingLight[idx] == '1' else 'O' #set the item at the index to l if the light is on or O if the light is off
        if construction[0][i].startswith('X'): #if the item starts with X
            lightrow[i] = 'O' #set the item to O
    startrow = lightrow.copy() #create a copy of the lightrow
    for i in construction[1:-1]: #for each row in the construction except the first and last
        j = 0 #set j to 0
        while j in range(len(i)): #while j is in range of the length of the row
            if j < len(i) - 1: #if j is less than the length of the row minus 1
                if i[j] == 'R' and i[j+1] == 'r': #if the item at j is R and the item at j+1 is r logic for Red Left Input
                    if lightrow[j] == 'l':
                        lightrow[j] = 'O'
                        lightrow[j+1] = 'O'
                    else:
                        lightrow[j] = 'l'
                        lightrow[j+1] = 'l'
                if i[j] == 'r' and i[j+1] == 'R': #if the item at j is r and the item at j+1 is R logic for Red Right Input
                    if lightrow[j+1] == 'l':
                        lightrow[j] = 'O'
                        lightrow[j+1] = 'O'
                    else:
                        lightrow[j] = 'l'
                        lightrow[j+1] = 'l'
            if i[j] == 'W' and i[j+1] == 'W': #if the item at j is W and the item at j+1 is W logic for White
                if lightrow[j] == 'O' and lightrow[j+1] == 'O':
                    lightrow[j] = 'l'
                    lightrow[j+1] = 'l'
                elif lightrow[j] == 'l' and lightrow[j+1] == 'l':
                    lightrow[j] = 'O'
                    lightrow[j+1] = 'O'
                else: #logic for Blue
                    lightrow[j] = 'l'
                    lightrow[j+1] = 'l'
                j += 1
            if i[j] == 'X': #if the item at j is X
                lightrow[j] = 'O'
            j += 1
        #print(lightrow)
    final_leds = ['1' if lightrow[led_item] == 'l' and construction[-1][led_item].startswith("L") else '0' if construction[-1][led_item].startswith("L") else '' for led_item in range(len(lightrow))] #create a list of length n with all items set to L if the light is on or X if the light is off
    return final_leds

def test_all_flashlight_combinations(n, m, construction, lightcount): #test all flashlight combinations
    print("Testing all flashlight combinations: ") #print the message
    print("Start" + " -> " + "End") #print direction
    for i in range(2**lightcount): #for each flashlight combination
        flashlights = bin(i)[2:].zfill(lightcount) #get the binary representation of the number and pad it with 0s to the length of the number of lights
        final_leds = interpretConstruction(n, m, construction, flashlights, lightcount) #interpret the construction
        print(flashlights + " -> " +  "".join(final_leds)) #print the flashlight combination and the final state of the LEDs

start = time.time() #start the timer
n, m, construction, lightcount = read_construction_file("nandu/Input/nandu5.txt") #read the construction file and get the number of rows, number of columns, the construction, and the number of lights
test_all_flashlight_combinations(n, m, construction, lightcount) #test all flashlight combinations
end = time.time() #end the timer
print('{:5.3f}s'.format(end-start), end='  ')