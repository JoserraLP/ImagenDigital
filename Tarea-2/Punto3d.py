
class Punto3D():
    """Clase para representar un punto 3D"""
	x = 0
	y = 0
	z = 0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def getX(self):
        """Getter de X"""
		return self.x

    def setX(self, x):
        """Setter de X"""
		self.x = x

    def getY(self):
        """Getter de Y"""
		return self.y

    def setY(self, y):
        """Setter de Y"""
		self.y = y

    def getZ(self):
        """Getter de Z"""
		return self.z

    def setZ(self, z):
        """Setter de Z"""
		self.z = z