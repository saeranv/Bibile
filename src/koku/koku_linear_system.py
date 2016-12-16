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
        #You can achieve this swap using a temporary container
        #or you can use this, which accounts for the temp storage
        #Mutate
        self.planes[row0],self.planes[row1] = self.planes[row1],self.planes[row0]
    def multiply_coefficient_and_row(self, coefficient, row):
        #Multiples normal vector and constant by scalar coefficient
        #Makes a NEW normal vector and NEW scalar coefficient and then
        #creates a new plane instance for the row
        #This is done for two reasons:
        #1. Redefining the vector/coefficient will mutate the original 
        # plane that was referenced in initiating the object, which gets confusing
        # Will mutate.
        
        new_normal_vector = self.planes[row].normal_vector.times_scalar(coefficient)
        new_constant_term = self.planes[row].constant_term * coefficient
        self.planes[row] = Plane(normal_vector=new_normal_vector, constant_term=new_constant_term)
    def add_multiple_times_row_to_row(self, coefficient, row_index_to_add, row_index):
        # Multiples the row_index_to_add with coefficient and then
        # adds it to the row_index
        # This function will mutate the row
        
        #print 'old rows'
        #print self[row_index], 'row index'
        #print self[row_index_to_add], 'row index to add'
        #Create new row normal and constant
        new_normal = self.planes[row_index_to_add].normal_vector.times_scalar(coefficient)
        new_constant = self.planes[row_index_to_add].constant_term * coefficient
        
        #Add the rows normal and constants
        sum_normal_vector = self.planes[row_index].normal_vector.plus(new_normal)
        sum_constant_term = self.planes[row_index].constant_term + new_constant
        
        #Create new plane
        self.planes[row_index] = Plane(normal_vector=sum_normal_vector,constant_term=sum_constant_term)
        #print 'new rows'
        #print self[row_index], 'row index'
        #print self[row_index_to_add], 'row index to add'
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
    def rref(self):
        #RREF:
        #1. rows with all zeros are below nonzero rows
        #2. leading coefficients (pivots) are left of leading
        #   coefficients below them. And are 1.
        #3. Coefficients below pivots (leading) coefficients = zero
        #4. If RREF acheived, then one variable is a parameter
        #   find the parameter, and define it as such
        
        system = deepcopy(self)
        
        # Find leading coefficients index
        # Loop through rows
        # divide row by leading coefficient
        numofplanes = len(self.planes)
        nonzero_indices = system.indices_of_first_nonzero_terms_in_each_row()
        for i in xrange(len(system.planes)):
            coeff_index = nonzero_indices[i]
            coeff2one = system.planes[i].normal_vector.coord[coeff_index]
            onefactor = Decimal(str(1/float(coeff2one)))
            system.multiply_coefficient_and_row(onefactor,i)
            
            # Now we go down row cells 
            j = coeff_index + 1
            while j < self.dimension:
                print j, self.dimension
                print system.planes[i].normal_vector
                coeff2zero = MyDecimal(system.planes[i].normal_vector.coord[j]) 
                #check if already zero
                if not coeff2zero.is_near_zero(): 
                    #check if row below exists and is nonzero
                    print 'data', coeff2zero, system.planes[i], 'j:', j
                    if i+1 < numofplanes:
                        coeff2divby = MyDecimal(system.planes[i+1].normal_vector.coord[j])
                        print 'coeff2divby', coeff2divby
                        if not coeff2divby.is_near_zero():
                            zerofactor = -1/coeff2divby * coeff2zero
                            print zerofactor , 'zerofactor'
                            #system.multiply_coefficient_and_row(zerofactor,i+1)
                            system.add_multiple_times_row_to_row(zerofactor,i+1,i)
                            break
                            #continue
                            """
                            #PROBLEM:
                            if we continue, then the next iteration in row will increase
                            subsequent row
                            so we must increment 1 and j....
                            1,0,-2 = 3
                            0,1,0 = 4
                            0,0,1 = 5
                            """
                        else:
                            pass
                            #increment by 1...recurse?
                    else:
                        #this is a paramater
                        pass
                j += 1
            # if all rows below are zero, then it is a parameter: continue
        print '---'
        print system
        return system
    def compute_triangular_form(self):
        # Compute triangular form, i.e
        # 2 1 1 = 4
        # 0 3 1 = 5
        # 0 0 2 = 5
        
        # Assumptions: 
        # 1. Swap with current row with topmost row below current row
        # 2. Don't multiply rows by numbers
        # 3. Only add a multiple of a row to rows underneat row underneath.
    
        system = deepcopy(self)
        #print 'orig', system
        lstofplanes = system.planes
        # define system variables
        numofeqn = len(lstofplanes)
        numofcoord = system.dimension
        col_i = 0 #the column/coordinate
        # Iterate down through each row
        for row_i in xrange(numofeqn):
            # Iterate through each column of each row
            roweqn = lstofplanes[row_i]
            while col_i < numofcoord:
                coef = MyDecimal(roweqn.normal_vector.coord[col_i])
                #Check if coeff == 0
                if coef.is_near_zero():
                    #swap rows with one below
                    IsSwap = system.swap_first_nonzero_row(row_i,col_i)
                    if not IsSwap:
                        #then all zero, so move to next column
                        col_i += 1
                        continue # this continues to next iterative loop
                system.clear_all_terms_below(row_i,col_i)
                col_i += 1
                break #break b/c done all terms below, move to next
            col_i = 0
            #print '---'
        #print 'rref', system
        return system
    def clear_all_terms_below(self,rowi,coli):
        #check not last row
        if rowi+1 < len(self.planes):
            beta = self[rowi].normal_vector.coord[coli]
            for i,roweqn in enumerate(self.planes[rowi+1:]):
                index = rowi + 1 + i
                gamma = roweqn.normal_vector.coord[coli]
                alpha = -gamma/beta
                self.add_multiple_times_row_to_row(alpha,rowi,index)
    def swap_first_nonzero_row(self,rowi,coli):
        #check if last row
        if rowi+1 < len(self.planes):
            for i,eqn in enumerate(self.planes[rowi+1:]):
                index = rowi + 1 + i
                coef2chk = eqn.normal_vector.coord[coli]
                if not MyDecimal(coef2chk).is_near_zero():
                    self.swap_rows(rowi,index)
                    return True
        return False
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
    def is_near_zero(self, eps=1E-10):
        return abs(float(self)) < eps


## Test 3: Triangular Form



p1 = Plane(normal_vector=Vector(['0','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['3','3','1']), constant_term='2')
p3 = Plane(normal_vector=Vector(['2','5','6']), constant_term='2')
s = LinearSystem([p1,p2,p3])
t = s.compute_triangular_form()
#print t
r = t.rref()

#print r 



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
#print '---'
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
#print s[0].basepoint
#print p1.basepoint #basepoints are the same
if not (s[0] == p1 and s[1] == p0 and s[2] == p2 and s[3] == p3):
    print 'test case 4 failed'

s.multiply_coefficient_and_row(-1,2)
if not (s[0] == p1 and
        s[1] == p0 and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print 'test case 5 failed'

s.multiply_coefficient_and_row(10,1)
if not (s[0] == p1 and
        s[1] == Plane(normal_vector=Vector(['10','10','10']), constant_term='10') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print 'test case 6 failed'

s.add_multiple_times_row_to_row(0,0,1)
if not (s[0] == p1 and
        s[1] == Plane(normal_vector=Vector(['10','10','10']), constant_term='10') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print 'test case 7 failed'

s.add_multiple_times_row_to_row(1,0,1)
if not (s[0] == p1 and #p1 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
        s[1] == Plane(normal_vector=Vector(['10','11','10']), constant_term='12') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print 'test case 8 failed'

#Plane(normal_vector=['-10','-10','-10', constant_term='-10')
s.add_multiple_times_row_to_row(-1,1,0)
if not (s[0] == Plane(normal_vector=Vector(['-10','-10','-10']), constant_term='-10') and
        s[1] == Plane(normal_vector=Vector(['10','11','10']), constant_term='12') and
        s[2] == Plane(normal_vector=Vector(['-1','-1','1']), constant_term='-3') and
        s[3] == p3):
    print 'test case 9 failed'
"""
"""
## Compute triangular form tests
p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','1']), constant_term='2')
s = LinearSystem([p1,p2])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == p2):
    print 'test case 1 failed'
    

p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1','1','1']), constant_term='2')
s = LinearSystem([p1,p2])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == Plane(constant_term='1')):
    print 'test case 2 failed'

p1 = Plane(normal_vector=Vector(['1','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['0','1','0']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1','1','-1']), constant_term='3')
p4 = Plane(normal_vector=Vector(['1','0','-2']), constant_term='2')
s = LinearSystem([p1,p2,p3,p4])
t = s.compute_triangular_form()
if not (t[0] == p1 and
        t[1] == p2 and
        t[2] == Plane(normal_vector=Vector(['0','0','-2']), constant_term='2') and
        t[3] == Plane()):
    print 'test case 3 failed'


p1 = Plane(normal_vector=Vector(['0','1','1']), constant_term='1')
p2 = Plane(normal_vector=Vector(['1','-1','1']), constant_term='2')
p3 = Plane(normal_vector=Vector(['1','2','-5']), constant_term='3')
s = LinearSystem([p1,p2,p3])
t = s.compute_triangular_form()
if not (t[0] == Plane(normal_vector=Vector(['1','-1','1']), constant_term='2') and
        t[1] == Plane(normal_vector=Vector(['0','1','1']), constant_term='1') and
        t[2] == Plane(normal_vector=Vector(['0','0','-9']), constant_term='-2')):
    print 'test case 4 failed'
"""

