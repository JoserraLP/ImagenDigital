class TNormal():
    """Clase para representar la normal"""

    x = 0.0
    y = 0.0
    z = 0.0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def getX(self):
        """Getter de Normal X"""
        return self.x

    def setX(self, x):
        """Setter de Normal X"""
        self.x = x

    def getY(self):
        """Getter de Y"""
        return self.y
    
    def setY(self, y):
        """Setter de Normal Y"""
        self.y = y

    def getZ(self):
        """Getter de Normal Z"""
        return self.z

    def setZ(self, z):
        """Setter de Normal Z"""
        self.z = z