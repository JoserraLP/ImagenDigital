import TNormal

class Cara():
    """Class for representing a Cara"""
	
    a=0
    b=0
    c=0
    normal=TNormal()

    def __init__(self, vA, vB, vC, normal=None):
        self.a = vA
        self.b = vB
        self.c = vC
        self.normal = normal

    def getA(self):
        """Getter de A"""
        return self.a

    def setA(self, a):
        """Setter de A"""
        self.a = a

    def getB(self):
        """Getter de B"""
        return self.b
    
    def setB(self, b):
        """Setter de B"""
        self.b = b

    def getC(self):
        """Getter de C"""
        return self.a

    def setC(self, c):
        """Setter de C"""
        self.c = c

    def getNormal(self):
        """Getter de Normal"""
        return self.normal

    def setNormal(self, normal):
        """Setter de Normal"""
        self.normal = normal