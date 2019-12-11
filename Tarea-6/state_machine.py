class StateMachine():

    def __init__(self, bar_sup=0, bar_inf=0):
        self.is_bar_sup_passed = True
        self.is_bar_inf_passed = True
        self.bar_sup = bar_sup
        self.bar_inf = bar_inf
        self.contador = 1
        self.states = {
            'F': (False, False), #Fuera
            'D': (True, True), #Dentro
            'S': (False, True), #Saliendo
            'E': (True, False) #Entrando
        }

    def updateBarriers(self, bar_sup, bar_inf):
        self.bar_sup = bar_sup
        self.bar_inf = bar_inf

    def checkBarrier(self, centroidY):
        if (centroidY < self.bar_sup):
            if (self.is_bar_sup_passed, self.is_bar_inf_passed) == self.states['E']:
                self.contador += 1
            self.is_bar_sup_passed = True
            self.is_bar_inf_passed = True
        elif (centroidY > self.bar_sup and centroidY < self.bar_inf):
            if (self.is_bar_sup_passed, self.is_bar_inf_passed) == self.states['D']:
                self.is_bar_sup_passed = False
                self.is_bar_inf_passed = True
            elif (self.is_bar_sup_passed, self.is_bar_inf_passed) == self.states['F']:
                self.is_bar_sup_passed = True
                self.is_bar_inf_passed = False
        elif (centroidY > self.bar_sup and centroidY > self.bar_inf):
            if (self.is_bar_sup_passed, self.is_bar_inf_passed) == self.states['S']:
                self.contador -= 1
            self.is_bar_sup_passed = False
            self.is_bar_inf_passed = False
        return self.contador
