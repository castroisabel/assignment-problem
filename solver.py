# Requirements: Pyomo and GLPK
import pyomo.environ as pyEnv

""" Min x11 + 4x12 + 6x13 + 3x14 
     + 9x21 + 7x22 + 10x23 + 9x24 
     + 4x31 + 5x32 + 11x33 + 7x34 
     + 8x41 + 7x42 + 8x43 + 5x44

    S.t x11 + x12 + x13 + x14 = 1 
        x21 + x22 + x23 + x24 = 1 
        x31 + x32 + x33 + x34 = 1 
        x41 + x42 + x43 + x44 = 1                               
        x11 + x21 + x31 + x41 = 1 
        x12 + x22 + x32 + x42 = 1 
        x13 + x23 + x33 + x43 = 1 
        x14 + x24 + x34 + x44 = 1 
"""

costs = [[1, 4, 6, 3], [9, 7, 10, 9], [4, 5, 11, 7], [8, 7, 8, 5]]
m = len(costs) # number of developers
n = len(costs[0]) # number of tasks

# Declaring the model
model = pyEnv.ConcreteModel()

# Indexes
model.m = pyEnv.RangeSet(m)
model.n = pyEnv.RangeSet(n)

# Variables
model.variables = pyEnv.Var(model.m, model.n, within = pyEnv.NonNegativeReals)
model.allocated_cost = pyEnv.Param(model.m, model.n, initialize = lambda model, i, j: costs[i-1][j-1])

# Objective function
def obj_function(model):
    return sum(model.variables[i,j]*model.allocated_cost[i,j] for i in model.m for j in model.n)

model.obj_function = pyEnv.Objective(rule = obj_function, sense = pyEnv.minimize)

# Constraints 
def c1(model, i):
    return sum(model.variables[i,j] for j in model.n) == 1

def c2(model, j):
    return sum(model.variables[i,j] for i in model.m) == 1

model.c1 = pyEnv.Constraint(model.m, rule = c1)
model.c2 = pyEnv.Constraint(model.n, rule = c2)

# Solver 
solver = pyEnv.SolverFactory('glpk', executable = '/usr/bin/glpsol')
obj_results = solver.solve(model, tee = True)

# Results
l = list(model.variables.keys())
model.obj_function()

print('\nTask assigned to each developer:')
for i in l:
    if model.variables[i]() != 0:
        print(i)

print('Objective function value:', model.obj_function())
