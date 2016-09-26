from decimal import Decimal, getcontext
from copy import deepcopy

from koku_vector import Vector
from koku_plane import Plane

getcontext().prec = 30


class LinearSystem(object):

    ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG = 'All planes in the system should live in the same dimension'
    NO_SOLUTIONS_MSG = 'No solutions'
    INF_SOLUTIONS_MSG = 'Infinitely many solutions'

    def __init__(self, planes):
        ### Takes list of planes
        ### Checks if all planes are in the same dimension
        ### adds planes and dimension to class
        try:
            d = planes[0].dimension
            for p in planes:
                assert p.dimension == d

            self.planes = planes
            self.dimension = d
        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)
    def swap_rows(self, row0, row1):
        temp_plane = None
        temp_plane = self.planes[row0]
        self.planes[row0] = self.planes[row1]
        self.planes[row1] = temp_plane
    def multiply_coefficient_and_row(self, coefficient, row):
        pass # add your code
    def add_multiple_times_row_to_row(self, coefficient, row_to_add, row_to_be_added_to):
        pass # add your code here
    def indices_of_first_nonzero_terms_in_each_row(self):
        ### Finds the first nonzero terms in each row
        ### Therefore identifies the variable used to divide rows by
        ### Iterates through list of planes
        ### Finds the first nonzezo index in normal of plane (coefficient)
        ### If no nonzero, index is -1, and continues iteration at next plane
        ### Returns list of indices
        num_equations = len(self)
        num_variables = self.dimension
        indices = [-1] * num_equations

        for i,p in enumerate(self.planes):
            try:
                indices[i] = p.first_nonzero_index(p.normal_vector.coord)
            except Exception as e:
                if str(e) == Plane.NO_NONZERO_ELTS_FOUND_MSG:
                    continue
                else:
                    raise e

        return indices
    def __len__(self):
        return len(self.planes)
    def __getitem__(self, i):
        return self.planes[i]
    def __setitem__(self, i, x):
        ### Not too sure what this function does
        try:
            assert x.dimension == self.dimension
            self.planes[i] = x

        except AssertionError:
            raise Exception(self.ALL_PLANES_MUST_BE_IN_SAME_DIM_MSG)
    def __str__(self):
        ### Prints linear system
        ### Iterates each plane as an equation, and print equation of the plane.
        ret = 'Linear System:\n'
        temp = []
        for i,p in enumerate(self.planes):
            temp += ['Equation ' + str(i) + ':' + str(p)]
        ret += '\n'.join(temp)
        return ret
class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps

## Test 0
"""
p0 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p1 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
p2 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
p3 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')
s = LinearSystem([p0,p1,p2,p3])
print s.indices_of_first_nonzero_terms_in_each_row()
"""
## Test 1
"""
print s.indices_of_first_nonzero_terms_in_each_row()
print "%s,%s,%s,%s" % (s[0],s[1],s[2],s[3])
print len(s)
print s
s[0] = p1
print s
print MyDecimal('1e-9').is_near_zero()
print MyDecimal('1e-11').is_near_zero()
"""
## Test 2
"""
p0 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p1 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
p2 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
p3 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')

s = LinearSystem([p0,p1,p2,p3])
#print s
s.swap_rows(0,1)
chkrow_swap = p0 == s[1] and p1 == s[0]
chkrow_not_swap = p2 == s[2] and p3 == s[3]
if not (chkrow_swap and chkrow_not_swap):
    print 'test case 1 failed'
s.swap_rows(1,3)
if not (s[0] == p1 and s[1] == p3 and s[2] == p2 and s[3] == p0):
    print 'test case 2 failed'

s.swap_rows(3,1)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print 'test case 3 failed'

s.multiply_coefficient_and_row(1,0)
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print 'test case 4 failed'
"""