class Calculator:
    add = 0
    substract = 0
    multiply = 0
    divide = 0

    def __init__(self, number1, number2):
        self.number1 = number1
        self.number2 = number2

    def added(self):
        self.add = self.number1+self.number2
    
    def substracted(self):
        self.substract = self.number1-self.number2

    def multiplied(self):
        self.multiply = self.number1*self.number2

    def divided(self):
        self.divide = self.number1/self.number2