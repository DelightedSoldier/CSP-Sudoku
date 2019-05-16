import sys
import matplotlib.pyplot as plt
import numpy as np
import collections
from sets import Set

from copy import deepcopy


class Solver:
    
    def __init__(self):
        return
        
    def combine(self, rows, columns):
        "Combining files and columns"
        return [r + c for r in rows for c in columns]

    def solve(self):    
        
        '''
        grid : [a1 a2 a3 a4 a5 a6 a7 a8 a9 b1 b2 b3 ....]
        
        4 . . |. . . |8 . 5 
        . 3 . |. . . |. . . 
        . . . |7 . . |. . . 
        ------+------+------
        . 2 . |. . . |. 6 . 
        . . . |. 8 . |4 . . 
        . . . |. 1 . |. . . 
        ------+------+------
        . . . |6 . 3 |. 7 . 
        5 . . |2 . . |. . . 
        1 . 4 |. . . |. . .
        '''
        
        
        
        
        
        rows     = 'ABCDEFGHI'
        columns     = '123456789'
        
        #grid(list) : list of all squares 
        grid  = self.combine(rows, columns)
        
        #unitlist(list) : list of all files, columns and boxes
        unitlist = ([self.combine(rows, col) for col in columns] +
                    [self.combine(row, columns) for row in rows] +
                    [self.combine(rws, clmns) for rws in ('ABC','DEF','GHI') for clmns in ('123','456','789')])
        
        #units(dict) , sq : [sq belongs to [row][column][box]]          
        units = dict((s, [u for u in unitlist if s in u]) for s in grid)
        
        #peers(dict) , sq : set([list of all squares affected by the current square sq] ) 
        peers = dict((s, set(sum(units[s],[]))-set([s])) for s in grid)
        
        #values(dict) , sq : value
        values = self.grid_values(grid)
        
        
        domain = self.domain_values(values, peers)
        
            
        assignment = self.backtracking_search(values, domain, peers)
        values_string = ''
        
        if assignment:
            for item in grid:
                values_string += assignment[item]
        
        f= open("output.txt","a")
        f.write(values_string+'\n')
        f.close()
        return values
       
        
        
    def grid_values(self, grid):
        
        "Convert grid into a dict of {square: value}"
        chars = [c for c in sys.argv[1]]
        #assert len(chars) == 81
        return dict(zip(grid, chars))
    
    def domain_values(self, values, peers):
        
        "Convert grid into a dict of {square: domain_values}"
        domain = {}
        digits = '123456789'
        for s,d in values.items():
            if not str(d) in digits:
                temp_domain = digits
                for item in peers[s]:
                    if str(values[item]) in digits:
                       temp_domain = temp_domain.replace(values[item], '') 
                       
                domain[s] = temp_domain
        return domain
                
    def ac_3(self, values,  domain, peers):
        
        queue_blank_squares = Set()
        domain_cc = dict(domain)#.deepcopy()
        digits = '123456789'
        for s,d in values.items():
            if not str(d) in digits:
                for p in peers[s]:
                    if not str(values[p]) in digits:
                        queue_blank_squares.add((s,p))
        
        while queue_blank_squares:
            
            current_pair = queue_blank_squares.pop()
            
            a = current_pair[0]
            b = current_pair[1]
            
            a_d = domain_cc[a]
            b_d = domain_cc[b]
            
            revised = self.revise(current_pair, domain_cc)
            if revised:
                if len(domain_cc[a]) == 0:
                    return False
                    
                for p in peers[a]:
                    if not str(values[p]) in digits and not p == b:
                        queue_blank_squares.add((a,p))
        inference = {}
        for s, d in domain_cc.items():
            
            
            if len(d) == 1:
                inference[s] = domain_cc[s]
        
       return True, inference , domain_cc
                    
                
            
                
    def revise(self, pair, domain_cc):
        
        
        revised = False
        
        a = pair[0]
        b = pair[1]
        
        a_d = domain_cc[a]
        b_d = domain_cc[b]
        
        
        if len(b_d) == 1:
            for x in a_d:
                if b_d == x:
                    domain_cc[a] = domain_cc[a].replace(x,'') # a_d holds a copy of domain_cc[a] string only, not a reference
                    revised = True
                    
        elif len(a_d) == 1:
            for x in b_d:
                if a_d == x:
                    domain_cc[b] = domain_cc[b].replace(x,'') # a_d holds a copy of domain_cc[a] string only, not a reference
                    revised = True
                    
        return revised 
        
        
    
    
    def backtracking_search(self,values, domain, peers) :
        
        '''Entry point to backtracking, returns assignment'''
        
        assignment = {}
        digits = '123456789'
        assignment = self.backtrack(assignment, values, domain, peers)
        if assignment:
            for s,d in values.items():
                if not str(d) in digits:
               
                   values[s] = assignment[s] 
        
        return values
        
    def backtrack(self, assignment, values, domain, peers):
        
        '''self recursive, finds the assignment'''
        
        if not domain:
            return assignment
        
        
        _mrv = []
        min = 9
        for s , d in domain.items():
            if len(d) < min:
                min = len(d)
                mrv = s
        for value in domain[mrv]: #mrv : minimum remaining value variable
            values_cc = dict(values)
            values_cc[mrv] =  value  # assigning a value to the mrv
            domain_cc_BT = self.domain_values(values_cc, peers)  # rewriting domain for each vacant square
            assignment[mrv] = value
            consistency = self.ac_3(values_cc, domain_cc_BT, peers) # checking if consistent, forwards check
            if consistency:
                consistency , inference , domain = consistency  # if consistent, then new inference, new domain returned
                assignment = self.merge_two_dicts(assignment, inference) # merging inference and assignment
                result = self.backtrack(assignment, values_cc, domain_cc_BT, peers)
                if result:
                    return result
            del assignment[mrv] 
        
        return False
            
    
    def merge_two_dicts(self,x, y):
        """Given two dicts, merge them into a new dict as a shallow copy."""
        z = x.copy()
        z.update(y)
        return z                     
            
        
                 
            
        
        

#-------------------------------------------- Main -------------------------------------------------------  
  
  
# Define a main() function 
def main():
    solver = Solver()
  
    solver.solve()


#-----------------------------------------------------------------------------------------------------  


# This is the standard boilerplate that calls the main() function.   
if __name__ == '__main__':
    main()
