
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

  