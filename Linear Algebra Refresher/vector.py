import math
from decimal import Decimal, getcontext

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')


    def __str__(self):
        return 'Vector: {{{}}}'.format(', '.join('{0:.3f}'.format(x) for x in self.coordinates))


    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus(self, v):
        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        new_coordinates = [c*x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        return Decimal(math.sqrt(sum([x**2 for x in self.coordinates])))

    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal('1.0')/magnitude)
        except ZeroDivisionError:
            raise Exception('Cannot normalize then zero vector')
            
    def dot(self, v):
        new_coordicates = [x*y for x,y in zip(self.coordinates, v.coordinates)]
        return sum(new_coordicates)

    def angle(self, v, in_degrees=False):
        u1 = self.normalized()
        u2 = v.normalized()
        angle_in_radians = math.acos(u1.dot(u2))
        if in_degrees:
            return math.degrees(angle_in_radians)
        else:
            return angle_in_radians

    @staticmethod
    def is_close(a, b, rel_tol=1e-10):
        return abs(a-b) <= rel_tol

    def is_zero(self):
        return Vector.is_close(self.magnitude(), 0)
    
    def is_parallel(self, v):
        if (self.is_zero() or
            v.is_zero()):
            return True
        result = True
        for v1, v2 in zip(self.normalized().coordinates, v.normalized().coordinates):
            result = result and Vector.is_close(abs(v1), abs(v2))
        return result
    
    def is_orthogonal(self, v):
        return Vector.is_close(self.dot(v), 0)
    
    def parallel_project(self, b):
        unit_b = b.normalized()
        return unit_b.times_scalar(self.dot(unit_b))
    
    def orthogonal_project(self, b):
        parallel_project = self.parallel_project(b)
        return self.minus(parallel_project)
    
    def cross(self, v):
        x1, y1, z1 = self.coordinates
        x2, y2, z2 = v.coordinates
        x = y1*z2 - y2*z1
        y = 0 - (x1*z2 - x2*z1)
        z = x1*y2 - x2*y1
        return Vector([x,y,z])
    
    def area_parallelogram(self, v):
        return self.cross(v).magnitude()
    
    def area_triangle(self, v):
        return self.area_parallelogram(v) / 2
    