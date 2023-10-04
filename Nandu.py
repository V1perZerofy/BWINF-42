#white Block is an xor gate returns to true Boolean values
class whiteBlock():
    def __init__(self, inputU, inputD):
        self.name = "whiteBlock"
        self.inputU = inputU
        self.inputD = inputD

    
    def function(self):
        if self.inputU and self.inputD:
            return False, False
        elif self.inputU and not self.inputD:
            return True, True
        elif not self.inputU and self.inputD:
            return True, True
        elif not self.inputU and not self.inputD:
            return True, True
        

#red Block only takes one input
#return two true Boolean values when input is false
#return two false Boolean values when input is true
class redBlock():
    def __init__(self, input):
        self.name = "redBlock"
        self.input = input

    def function(self):
        if self.input:
            return False, False
        else:
            return True, True
        
#blue Block takes two inputs
#returns input values

class blueBlock():
    def __init__(self, inputU, inputD):
        self.name = "blueBlock"
        self.inputU = inputU
        self.inputD = inputD

    def function(self):
        return self.inputU, self.inputD