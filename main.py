# -*- coding:utf-8 -*- 

from math import acos, sqrt, pi
from decimal import Decimal, getcontext

# decimal.getcontext().prec 来设定小数点精度(默认为28)：
getcontext().prec = 30


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = 'No unique orthogonal component'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'No unique parallel component'
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'Cross function is only defined for 2d and 3d'

    
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

    def __iter__(self):
        self.current = 0
        return self

    def next(self):
        if self.current >= len(self.coordinates):
            raise StopIteration
        else:
            current_value = self.coordinates[self.current]
            self.current += 1
            return current_value

    def __len__(self):
        return len(self.coordinates)

    def __getitem__(self, i):
        return self.coordinates[i]

    def __str__(self):
        # return 'Vector: {}'.format(self.coordinates)
        return 'Vector: {}'.format([round(coord, 3)
                                    for coord in self.coordinates])

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def is_zero(self):
        return set(self.coordinates) == set([Decimal(0)])
    '''
    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance
    '''
    
    def plus(self, v):
        # return Vector([x+y for x,y in zip(self.coordinates, v.coordinates)])
        return Vector(map(sum, zip(self.coordinates, v.coordinates)))

    def minus(self, other):
        # return Vector([x-y for x,y in zip(self.coordinates, v.coordinates)])
        return Vector([coords[0] - coords[1]
                       for coords in zip(self.coordinates, other.coordinates)])

    def times_scalar(self, factor):
        return Vector([Decimal(factor) * coord for coord in self.coordinates])
   
    def magnitude(self):
        # return sqrt(sum([x**2 for x in self.coordinates]))
        return Decimal(sqrt(sum([coord * coord
                                 for coord in self.coordinates])))

    def normalized(self):
        try:
            # return self.times_scalar(1./self.magnitude())
            return self.times_scalar(Decimal('1.0') / self.magnitude())
        except ZeroDivisionError:
            raise Exception(CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def dot(self, v):
        return sum([x*y for x,y in zip(self.coordinates, v.coordinates)])

    def get_angle_rad(self, other):
        dot_prod = round(self.normalized().dot(other.normalized()), 3)
        return acos(dot_prod)

    def get_angle_deg(self, other):
        degrees_per_rad = 180. / pi
        return degrees_per_rad * self.get_angle_rad(other)

    def is_parallel(self, other):
        return (self.is_zero() or other.is_zero() or
                self.get_angle_rad(other) in [0, pi])

    def is_orthogonal(self, other):
        return round(self.dot(other), 3) == 0

    def get_projected_vector(self, other):
        """
        Gets projection of vector v in b
        """
        b_normalized = other.normalized()
        return b_normalized.times_scalar(self.dot(b_normalized))

    def get_orthogonal_vector(self, other):
        return self.minus(self.get_projected_vector(other))

    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e
    
    def component_parallel_to(self, basis):
        try:
            u = basis.normalized()
            weight = self.dot(u)
            return u.times_scalar(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e
    
    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance
        
    def is_parallel_to(self, v):
        return abs(self.is_zero() or v.is_zero() or self.angle_with(v) == 0 or self.angle_with(v) == pi)
            
    def angle_with(self, v, in_degrees=False):
        try:
            n1 = self.normalized()
            n2 = v.normalized()
            d = n1.dot(n2)
            d = min(d, Decimal('1'))
            d = max(d, Decimal('0'))
            angle_in_radians = acos(d)

            if in_degrees:
                degrees_per_radian = 180. / pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e
    def cross(self, v):
        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates

            return Vector([y_1 * z_2 - y_2 * z_1, -(x_1 * z_2 - x_2 * z_1), x_1 * y_2 - x_2 * y_1])
        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif msg == 'too many values to unpack' or msg == 'need more than value to unpack':
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e

    def area_of_triangle_with(self, v):
        return self.area_of_parallelogram_with(v) / Decimal('2.0')

    def area_of_parallelogram_with(self, v):
        return self.cross(v).magnitude()                
    '''
    def cross_product(self, other):
        [x1, y1, z1] = self.coordinates
        [x2, y2, z2] = other.coordinates
        x = (y1 * z2) - (y2 * z1)
        y = -((x1 * z2) - (x2 * z1))
        z = (x1 * y2) - (x2 * y1)
        return Vector([x, y, z])

    def area_parallelogram(self, other):
        return self.cross_product(other).magnitude()

    def area_triangle(self, other):
        return self.cross_product(other).magnitude() / 2
    '''    
    
if __name__ == '__main__':

    # 判断两个向量是否相等
    my_vector = Vector([1,2,3])
    my_vector2 = Vector([1,2,3])
    print my_vector	== my_vector2

    v = Vector([8.218, -9.341])
    w = Vector([-1.129, 2.111])
    addition = v.plus(w)
    print 'addition: {}'.format(addition)
    
    v = Vector([7.119, 8.215])
    w = Vector([-8.223, 0.878])
    subtraction = v.minus(w)
    print 'subtraction: {}'.format(subtraction)

    v = Vector([1.671, -1.012, -0.318])
    multiplication = v.times_scalar(7.41)
    print 'multiplication: {}'.format(multiplication)

    # *****************

    v = Vector([-0.221, 7.437])
    first_magintude = v.magnitude()
    print 'first_magintude: {}'.format(round(first_magintude, 3))

    v = Vector([8.813, -1.331, -6.247])
    second_magintude = v.magnitude()
    print 'second_magintude: {}'.format(round(second_magintude, 3))

    v = Vector([5.581, -2.136])
    first_normalization = v.normalized()
    print 'first_normailization: {}'.format(first_normalization)

    v = Vector([1.996, 3.108, -4.554])
    second_normalization = v.normalized()
    print 'second_normailization: {}'.format(second_normalization)

    # *****************
    # 求 v, w 点积
    v = Vector([7.887, 4.138])
    w = Vector([-8.802, 6.776])
    dot = v.dot(w)
    print 'first_dot: {}'.format(round(dot, 3))

    # 求 v, w 点积
    v = Vector([-5.955, -4.904, -1.874])
    w = Vector([-4.496, -8.755, 7.103])
    dot = v.dot(w)
    print 'second_dot: {}'.format(round(dot, 3))

    # *****************
    # 求 v, w 夹角, 单位rad
    v = Vector([3.183, -7.627])
    w = Vector([-2.668, 5.319])
    angle_rads = v.get_angle_rad(w)
    print 'first_angle_rads: {}'.format(angle_rads)

    # 求 v, w 夹角, 单位度
    v = Vector([7.35, 0.221, 5.188])
    w = Vector([2.751, 8.259, 3.985])
    angle_degrees = v.get_angle_deg(w)
    print 'first_angle_rads: {}'.format(angle_degrees)

    # *****************
    # 判断向量平行还是正交
    v = Vector([-7.579, -7.88])
    w = Vector([22.737, 23.64])
    is_parallel = v.is_parallel(w)
    is_orthogonal = v.is_orthogonal(w)

    print '1 parallel: {}, orthogonal: {}'.format(is_parallel, is_orthogonal)

    v = Vector([-2.029, 9.97, 4.172])
    w = Vector([-9.231, -6.639, -7.245])
    is_parallel = v.is_parallel(w)
    is_orthogonal = v.is_orthogonal(w)

    print '2 parallel: {}, orthogonal: {}'.format(is_parallel, is_orthogonal)

    v = Vector([-2.328, -7.284, -1.214])
    w = Vector([-1.821, 1.072, -2.94])
    is_parallel = v.is_parallel(w)
    is_orthogonal = v.is_orthogonal(w)
    print '3 parallel: {}, orthogonal: {}'.format(is_parallel, is_orthogonal)

    v = Vector([2.118, 4.827])
    w = Vector([0, 0])
    is_parallel = v.is_parallel(w)
    is_orthogonal = v.is_orthogonal(w)

    print '4 parallel: {}, orthogonal: {}'.format(is_parallel, is_orthogonal)

    # *****************

    v = Vector([3.039, 1.879])
    w = Vector([0.825, 2.036])
    projected_vector = v.get_projected_vector(w)

    print 'projected vector is: {}'.format(projected_vector)

    v = Vector([-9.88, -3.264, -8.159])
    w = Vector([-2.155, -9.353, -9.473])
    orthogonal_vector = v.get_orthogonal_vector(w)

    print 'orthogonal vector is: {}'.format(orthogonal_vector)

    v = Vector([3.009, -6.172, 3.692, -2.51])
    w = Vector([6.404, -9.144, 2.759, 8.718])
    projected_vector = v.get_projected_vector(w)
    orthogonal_vector = v.get_orthogonal_vector(w)

    print 'second projected vector is: {}'.format(projected_vector)

    print 'second orthogonal vector is: {}'.format(orthogonal_vector)


    # -----------------------------------------------------
    print '#1'
    v = Vector([3.039, 1.879])
    w = Vector([0.825, 2.036])
    print v.component_parallel_to(w)

    print '\n#2'
    v = Vector([-9.88, -3.264, -8.159])
    w = Vector([-2.155, -9.353, -9.473])
    print v.component_orthogonal_to(w)

    print '\n#3'
    v = Vector([3.009, -6.172, 3.692, -2.51])
    w = Vector([6.404, -9.144, 2.759, 8.718])
    vpar = v.component_parallel_to(w)
    vort = v.component_orthogonal_to(w)
    print 'parallel component:', vpar
    print 'orthogonal component:', vort
    
    # -----------------------------------------------------
    v1 = Vector([8.462, 7.893, -8.187])
    w1 = Vector([6.984, -5.975, 4.778])

    v2 = Vector([-8.987, -9.838, 5.031])
    w2 = Vector([-4.268, -1.861, -8.866])

    v3 = Vector([1.5, 9.547, 3.691])
    w3 = Vector([-6.007, 0.124, 5.772])

    first_cross_product = v1.cross(w1)
    print 'cross product is: {}'.format(first_cross_product)

    area_parallelogram = v2.area_of_parallelogram_with(w2) 
    print 'area parallelogram is: {}'.format(round(area_parallelogram, 3))

    area_triangle = v3.area_of_triangle_with(w3)
    print 'area triangle is: {}'.format(round(area_triangle, 3))
   
