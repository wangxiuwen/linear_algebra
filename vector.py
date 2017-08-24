# -*- coding:utf-8 -*- 

from math import acos, sqrt, pi
from decimal import Decimal, getcontext

# decimal.getcontext().prec 来设定小数点精度(默认为28)：
getcontext().prec = 30


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
    
    # 打印向量
    def __str__(self):
        # return 'Vector: {}'.format(self.coordinates)
        return 'Vector: {}'.format([round(coord, 3) for coord in self.coordinates])
    
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
    
    # 判断相等
    def __eq__(self, v):
        return self.coordinates == v.coordinates
    
    # 判断是否为0向量
    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance
    
    # 计算长度
    def magnitude(self):
        # return sqrt(sum([x**2 for x in self.coordinates]))
        return Decimal(sqrt(sum([coord * coord
                             for coord in self.coordinates])))

    def plus(self, v):
        # return Vector([x+y for x,y in zip(self.coordinates, v.coordinates)])
        return Vector(map(sum, zip(self.coordinates, v.coordinates)))

    def minus(self, v):
        return Vector([x-y for x,y in zip(self.coordinates, v.coordinates)])
        #return Vector([coords[0] - coords[1] for coords in zip(self.coordinates, v.coordinates)])

    # 乘以标量
    def times_scalar(self, factor):
        return Vector([Decimal(factor) * coord for coord in self.coordinates])
   
    # 标准化
    def normalized(self):
        try:
            # return self.times_scalar(1./self.magnitude())
            return self.times_scalar(Decimal('1.0') / self.magnitude())
        except ZeroDivisionError:
            raise Exception(CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    # 点积
    def dot(self, v):
        return sum([x*y for x,y in zip(self.coordinates, v.coordinates)])

    # 向量投影 
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
    
    # 正交分量
    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)
        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e
    
    # 判断正交
    def is_orthogonal_to(self, v, tolerance=1e-10):
        # return round(self.dot(other), 3) == 0
        return abs(self.dot(v)) < tolerance
    
    # 判断平行  
    def is_parallel_to(self, v, tolerance=1e-6):
        print self, v
        return abs(self.is_zero() or v.is_zero() or 
                self.angle_with(v) == 0 or self.angle_with(v) == pi)
        
    # 计算向量夹角
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
    
    # 计算叉积
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
    
    # 计算平行四边形面积
    def area_of_parallelogram_with(self, v):
        return self.cross(v).magnitude()
    
    #计算三角形面积
    def area_of_triangle_with(self, v):
        return self.area_of_parallelogram_with(v) / Decimal('2.0')

if __name__ == '__main__':

    print '判断两个向量是否相等:'
    v = Vector([1,2,3])
    w = Vector([1,2,3])
    print v	== w
    print '\r\n'

    print '向量相加:'
    v = Vector([8.218, -9.341])
    w = Vector([-1.129, 2.111])
    addition = v.plus(w)
    print 'addition: {}'.format(addition)
    print '\r\n'
    
    print '向量相减:'
    v = Vector([7.119, 8.215])
    w = Vector([-8.223, 0.878])
    subtraction = v.minus(w)
    print 'subtraction: {}'.format(subtraction)
    print '\r\n'

    print '与标量相乘:'
    v = Vector([1.671, -1.012, -0.318])
    multiplication = v.times_scalar(7.41)
    print 'multiplication: {}'.format(multiplication)
    print '\r\n'

    print '计算长度:'
    v = Vector([-0.221, 7.437])
    w = Vector([8.813, -1.331, -6.247])
    
    first_magintude = v.magnitude()
    print 'first_magintude: {}'.format(round(first_magintude, 3))
    

    second_magintude = w.magnitude()
    print 'second_magintude: {}'.format(round(second_magintude, 3))
    print '\r\n'

    print '向量标准化:'
    v = Vector([5.581, -2.136])
    w = Vector([1.996, 3.108, -4.554])
    
    first_normalization = v.normalized()
    print 'first_normailization: {}'.format(first_normalization)

    second_normalization = w.normalized()
    print 'second_normailization: {}'.format(second_normalization)
    print '\r\n'
    
    print '求 v, w 点积:'
    v1 = Vector([7.887, 4.138])
    w1 = Vector([-8.802, 6.776])
    
    v2 = Vector([-5.955, -4.904, -1.874])
    w2 = Vector([-4.496, -8.755, 7.103])
    
    dot = v1.dot(w1)
    print 'first_dot: {}'.format(round(dot, 3))

    dot = v2.dot(w2)
    print 'second_dot: {}'.format(round(dot, 3))
    print '\r\n'
    
    print '求 v, w 夹角, 单位rad:'
    v = Vector([3.183, -7.627])
    w = Vector([-2.668, 5.319])
    angle_rads = v.angle_with(w,True)
    print 'first_angle_rads: {}'.format(angle_rads)
    print '\r\n'
    
    print '求 v, w 夹角, 单位度:'
    v = Vector([7.35, 0.221, 5.188])
    w = Vector([2.751, 8.259, 3.985])
    angle_degrees = v.angle_with(w, True)
    print 'first_angle_rads: {}'.format(angle_degrees)
    print '\r\n'
    
    print '判断向量平行还是正交:'
    v1 = Vector([-7.579, -7.88])
    w1 = Vector([22.737, 23.64])
    
    v2 = Vector([-2.029, 9.97, 4.172])
    w2 = Vector([-9.231, -6.639, -7.245])
    
    v3 = Vector([-2.328, -7.284, -1.214])
    w3 = Vector([-1.821, 1.072, -2.94])
    
    v4 = Vector([2.118, 4.827])
    w4 = Vector([0, 0])
    
    is_parallel = v1.is_parallel_to(w1)
    is_orthogonal = v1.is_orthogonal_to(w1)
    print '1 parallel: {}, orthogonal: {}'.format(is_parallel, is_orthogonal)

    is_parallel = v2.is_parallel_to(w2)
    is_orthogonal = v2.is_orthogonal_to(w2)
    print '2 parallel: {}, orthogonal: {}'.format(is_parallel, is_orthogonal)

    is_parallel = v3.is_parallel_to(w3)
    is_orthogonal = v3.is_orthogonal_to(w3)
    print '3 parallel: {}, orthogonal: {}'.format(is_parallel, is_orthogonal)

    is_parallel = v4.is_parallel_to(w4)
    is_orthogonal = v4.is_orthogonal_to(w4)
    print '4 parallel: {}, orthogonal: {}'.format(is_parallel, is_orthogonal)
    print '\r\n'
    
    print '计算投影:'
    v = Vector([3.039, 1.879])
    w = Vector([0.825, 2.036])
    print 'component_parallel_to: {}'.format(v.component_parallel_to(w))

    v = Vector([-9.88, -3.264, -8.159])
    w = Vector([-2.155, -9.353, -9.473])
    print 'component_orthogonal_to: {}'.format(v.component_orthogonal_to(w))
 
    v = Vector([3.009, -6.172, 3.692, -2.51])
    w = Vector([6.404, -9.144, 2.759, 8.718])
    vpar = v.component_parallel_to(w)
    vort = v.component_orthogonal_to(w)
    print 'parallel component:', vpar
    print 'orthogonal component:', vort
    print '\r\n'
    
    print '计算叉积:'
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
   
