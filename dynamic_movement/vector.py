
class Vector:
    """
    A simple Vector class with a few simple operators.

    Operators:
        Addition: +
        Subtraction: -
        Multiplication/Dot Product: *
        Division: /

    Properties:
        x: Only defined if the Vector is at least 1 dimensional
        y: Only defined if the Vector is at least 2 dimensional
        z  Only defined if the Vector is at least 3 dimensional

    :author: Ben Morrison
    """
    def __init__(self, *values):
        if isinstance(values, tuple):
            values = list(values)
        self.values = tuple(values)

    def __len__(self):
        return len(self.values)

    def __add__(self, other):
        """
        :param other: If other is a Vector, it returns the dot sum. Otherwise it returns values[n] + other.
        :return: Vector
        """
        if isinstance(other, Vector):
            return Vector(*[a + b for a, b in zip(self.values, other.values)])
        else:
            return Vector(*[other + i for i in self.values])

    def __sub__(self, other):
        """
        :param other: If other is a Vector, it returns the dot difference. Otherwise it returns values[n] - other.
        :return: Vector
        """
        if isinstance(other, Vector):
            return Vector(*[a - b for a, b in zip(self.values, other.values)])
        else:
            return Vector(*[other - i for i in self.values])

    def __mul__(self, other):
        """
        :param other: If other is a Vector, it returns the dot product. Otherwise it returns values[n] * other.
        :return: Vector
        """
        if isinstance(other, Vector):
            return sum([a * b for a, b in zip(self.values, other.values)])
        else:
            return Vector(*[other * i for i in self.values])

    def __divmod__(self, other):
        """
        :param other: If other is a Vector, it returns the dot quotient/remainder. Otherwise it returns values[n] /% other.
        :return: Vector
        """
        if isinstance(other, Vector) and len(other) == len(self):
            return Vector(*[a / b for a, b in zip(self.values, other.values)])
        return Vector(*[i / other for i in self.values]), Vector(*[i % other for i in self.values])

    def __truediv__(self, other):
        """
        Simple scalar division
        :param other: The scalar the Vector is being divided by.
        :return: Vector
        """
        return Vector(*[i / other for i in self.values])

    def __getitem__(self, item):
        return self.values[item]

    def __str__(self):
        return f"vec<{', '.join([f'{val:10.3f}' if isinstance(val, float) else f'{val:10}' for val in self.values])}>"

    def get_x(self):
        return self.values[0]

    def get_y(self):
        return self.values[1]

    def get_z(self):
        return self.values[2]

    def magnitude(self):
        return sum([value * value for value in self.values]) ** (1/2)

    def normalize(self):
        return self / self.magnitude()

    def lerp(self, other, percentage):
        assert isinstance(other, Vector)
        assert 0 <= percentage <= 1
        return other * percentage + self * (1 - percentage)

    x = property(get_x)
    y = property(get_y)
    z = property(get_z)
