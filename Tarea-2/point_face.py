
from typing import Tuple


class Point2D:
    """Vector two dimensional

    Attributes:
        x (float): X axis
        y (float): Y axis
    """

    def __init__(self, x: float = 0, y: float = 0):
        """Creates a Point2D (two-dimensional vector)

        Args:
            x (float): X axis
            y (float): Y axis
        """

        self.x = x
        self.y = y

    @classmethod
    def from_tuple(cls, tuple: Tuple[float, float]):
        """Creates a Point2D from a tuple"""

        if tuple is None:
            return cls()

        return cls(tuple[0], tuple[1])


class Point3D:
    """Vector three dimensional

    Attributes:
        x (float): X axis
        y (float): Y axis
        z (float): Z axis
    """

    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        """Creates a Point3D (three-dimensional vector)

        Args:
            x (float): X axis
            y (float): Y axis
            z (float): Z axis
        """

        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_tuple(cls, tuple: Tuple[float, float, float]):
        """Creates a Point3D from a tuple"""

        if tuple is None:
            return cls()

        return cls(tuple[0], tuple[1], tuple[2])


class Rotation:
    """Rotation in Euler angles

    Attributes:
        alpha (float): Rotation around the Z axis
        beta (float): Rotation around the X axis
        gamma (float): Rotation around the Y axis
    """

    def __init__(self, alpha: float = 0, beta: float = 0, gamma: float = 0):
        """Creates a Rotation

        Args:
            alpha (float): Rotation around the Z axis
            beta (float): Rotation around the X axis
            gamma (float): Rotation around the Y axis
        """

        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    @classmethod
    def from_tuple(cls, tuple: Tuple[float, float, float]):
        """Creates a Rotation from a tuple"""

        if tuple is None:
            return cls()

        return cls(tuple[0], tuple[1], tuple[2])


class Face:
    """Face of a 3D model, a triangle made up of 3 points

    Attributes:
        a (int): The index in the vertices list for the vertex A
        b (int): The index in the vertices list for the vertex B
        c (int): The index in the vertices list for the vertex C
        normal (Point3D): The Normal vector of the Face
    """

    def __init__(self, a: int, b: int, c: int, normal: Point3D):
        """Creates a Face

        Args:
            a (int): Reference to vertex A in the vertices list
            b (int): Reference to vertex B in the vertices list
            c (int): Reference to vertex C in the vertices list
            normal (Point3D): The Normal vector of the Face
        """

        self.a = a
        self.b = b
        self.c = c
        self.normal = normal

    @classmethod
    def from_tuple(cls, tuple: Tuple[int, int, int, Point3D]):
        """Creates a Face from a tuple"""

        if tuple is None:
            return cls()

        return cls(tuple[0], tuple[1], tuple[2], tuple[3])


class Transform:
    """Transform holds position, scaling and rotation for an object in the World

    Attributes:
        position (Point3D): Position in the 3D World
        scaling (Point3D): Scaling of the Object
        rotation (Rotation): Rotation of the Object
    """

    def __init__(self, position: Point3D = Point3D(), scaling: Point3D = Point3D(), rotation: Rotation = Rotation()):
        """Creates a Transform data

        Args:
            position (Point3D): Position in the 3D World
            scaling (Point3D): Scaling of the Object
            rotation (Rotation): Rotation of the Object
        """

        self.position = position
        self.scaling = scaling
        self.rotation = rotation
