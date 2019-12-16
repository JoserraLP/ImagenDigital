class StateMachine():
    """ `StateMachine`

        Maquina de estados para representar y gestionar los cuatro estados que surgen
        teniendo las dos barreras de entrada.

        Estos cuatro estados son:
            - F --> FUERA
            - D --> DENTRO
            - S --> SALIENDO
            - E --> ENTRANDO
    """

    __author__      =   "Jose Ramon Lozano Pinilla, Javier Nogales Fernandez"

    def __init__(self, bar_sup=0, bar_inf=0, cont=0):
        """ `__init__`
            
            Inicializa la clase `StateMachine`

            Parametros
            ----------
            - bar_sup  :  Barrera superior
            - bar_inf  :  Barrera inferior
            - cont     :  Contador de elementos
        """
        self.is_bar_sup_passed = True
        self.is_bar_inf_passed = True
        self.bar_sup = bar_sup
        self.bar_inf = bar_inf
        self.contador = cont
        self.states = {
            'F': (False, False), #Fuera
            'D': (True, True), #Dentro
            'S': (False, True), #Saliendo
            'E': (True, False) #Entrando
        }

    def updateBarriers(self, bar_sup, bar_inf):
        """ `updateBarriers`
            Actualiza las barreras con los valores actuales

            Parametros
            ----------
            - bar_sup  :  Nueva barrera superior
            - bar_inf  :  Nueva barreara inferior

        """
        self.bar_sup = bar_sup
        self.bar_inf = bar_inf

    def checkBarrier(self, centroidY):
        """ `checkBarrier`
            
            Gestiona el contador dependiendo del estado en el que se encuentre y el estado anterior.

            Parametros
            ----------
            - centroidY  :  Ordenada del centroide

            Return
            ------
            - contador  :  Contador de elementos dentro del aula

        """
        if (centroidY < self.bar_sup): # Si estamos por encima de la barrera superior
            if (self.is_bar_sup_passed, self.is_bar_inf_passed) == self.states['E']: # Si el estado anterior es ENTRANDO
                self.contador += 1 # Aumentamos el contador
            self.is_bar_sup_passed = True 
            self.is_bar_inf_passed = True
        elif (centroidY > self.bar_sup and centroidY < self.bar_inf): # Si estamos en medio de las dos barreras
            if (self.is_bar_sup_passed, self.is_bar_inf_passed) == self.states['D']: # Si el estado anterior es DENTRO
                self.is_bar_sup_passed = False
                self.is_bar_inf_passed = True
            elif (self.is_bar_sup_passed, self.is_bar_inf_passed) == self.states['F']: #Si el estado anterior es FUERA
                self.is_bar_sup_passed = True
                self.is_bar_inf_passed = False
        elif (centroidY > self.bar_sup and centroidY > self.bar_inf): #Si estamos debajo de las dos barreras
            if (self.is_bar_sup_passed, self.is_bar_inf_passed) == self.states['S']: #Si el estado anterior es SALIENDO
                self.contador -= 1 # Decrementamos el contador
            self.is_bar_sup_passed = False
            self.is_bar_inf_passed = False
        return self.contador
