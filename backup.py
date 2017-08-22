
    def is_parallel(self, other):
        return (self.is_zero() or other.is_zero() or self.get_angle_rad(other) in [0, pi])
        
    def is_zero(self):
        return set(self.coordinates) == set([Decimal(0)])
        
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps
   
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

    def get_angle_rad(self, other):
        dot_prod = round(self.normalized().dot(other.normalized()), 3)
        return acos(dot_prod)

    def get_angle_deg(self, other):
        degrees_per_rad = 180. / pi
        return degrees_per_rad * self.get_angle_rad(other)
        
    def cross_product(self, other):
        [x1, y1, z1] = self.coordinates
        [x2, y2, z2] = other.coordinates
        x = (y1 * z2) - (y2 * z1)
        y = -((x1 * z2) - (x2 * z1))
        z = (x1 * y2) - (x2 * y1)
        return Vector([x, y, z])

  #-----------
  



   

    def intersection(self, line2):

        a, b = self.normal_vector.coordinates
        c, d = line2.normal_vector.coordinates
        k1 = self.constant_term
        k2 = line2.constant_term
        denom = ((a * d) - (b * c))

        if MyDecimal(denom).is_near_zero():
            if self == line2:
                return self
            else:
                return None

        one_over_denom = Decimal('1') / ((a * d) - (b * c))
        x_num = (d * k1 - b * k2)
        y_num = (-c * k1 + a * k2)

        return Vector([x_num, y_num]).times_scalar(one_over_denom)

 
# first system
# 4.046x + 2.836y = 1.21
# 10.115x + 7.09y = 3.025

line1 = Line(Vector([4.046, 2.836]), 1.21)
line2 = Line(Vector([10.115, 7.09]), 3.025)

print 'first system instersects in: {}'.format(line1.intersection(line2))


# second system
# 7.204x + 3.182y = 8.68
# 8.172x + 4.114y = 9.883

line3 = Line(Vector([7.204, 3.182]), 8.68)
line4 = Line(Vector([8.172, 4.114]), 9.883)

print 'second system instersects in: {}'.format(line3.intersection(line4))

# third system
# 1.182x + 5.562y = 6.744
# 1.773x + 8.343y = 9.525

line5 = Line(Vector([1.182, 5.562]), 6.744)
line6 = Line(Vector([1.773, 8.343]), 9.525)

print 'third system instersects in: {}'.format(line5.intersection(line6))