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


def greedy_algorithm(costs):
    """ Greedy algorithm to calculate the solution to the assignment problem.

    Args: 
        costs (list of integers): costs associated to each tasks 

    Returns: 
        list of integers: final solution
    """
    
    m = len(costs) # developers
    n = len(costs[0]) # tasks
    
    best_solution = [0 for i in range(m)]
    minor_task = 0
    index_minor_task = 0
    tasks = [i for i in range(n)]

    for i in range(m):
        for j in range(len(tasks)):
            current_task = tasks[j]
            if(costs[i][current_task] < costs[i][minor_task]):
                minor_task = current_task
                index_minor_task = j
                
        best_solution[i] = minor_task
        
        del(tasks[index_minor_task])
    
        try:
            minor_task = tasks[0]
        except:
            print(' ')
            
        index_minor_task = 0
            
    return best_solution
        

def obj_function(costs, solution):
    """ Function to calculate the objective function.

    Args: 
        costs (list of integers): costs associated to each tasks 
        solution (list of integers): solutions vector

    Returns: 
        int: objective function value
    """
    
    value = 0
    for i in range(len(costs)):
        value += costs[i][solution[i]]
    return value


solution = greedy_algorithm(costs)
best_value = obj_function(costs, solution)


# Results
print('Task assigned to each developer:')
for i in range(len(solution)):
    print('({},{})'.format(i, solution[i]))
    
print('Solution:', solution)

print('Objective function value:', best_value)