#!/usr/bin/env python
# coding: utf-8

# In[11]:


import random

# read the file and save a list of target, budget, output flag, restart and items
def read_input(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    
    first_line = lines[0].split()
    target, budget, output_flag = int(first_line[0]), int(first_line[1]), first_line[2]
    restarts = int(first_line[3]) if len(first_line) > 3 else 0
    items = [(line.split()[0], int(line.split()[1]), int(line.split()[2])) for line in lines[1:]]

    return target, budget, output_flag, restarts, items

# calculate the error
def error_function(value, cost, target, budget):
    return max(cost - budget, 0) + max(target - value, 0)

# random state
def random_states(i):
    return [i for i in i if random.choice([True, False])]

# get value and cost
def value_cost(state):
    value_total = sum(i[1] for i in state)
    cost_total = sum(i[2] for i in state)
    return value_total, cost_total

# get the neighbours 
def get_neighbours(cur_state, items):
    neighbours = []
    for item in items:
        updated_state = cur_state[:] if item in cur_state else cur_state + [item]
        if item in cur_state:
            updated_state.remove(item)
        neighbours.append(updated_state)
    return neighbours


# format the results
def print_result(result, value, cost, error):
    items = "{" + ' '.join(item[0] for item in result) + "}"
    return f"{items}. Value = {value}. Cost = {cost}. Error = {error}."

# running hill climbing
def hill_climbing(items, target, budget, output_flag, restarts):
    best_solution = "No Solution" # if not overwite, then no solution
    for _ in range(restarts + 1):
        cur_state = random_states(items)
        cur_value, cur_cost = value_cost(cur_state)
        cur_error = error_function(cur_value, cur_cost, target, budget)

        if output_flag == 'V':
            print(f"Randomly chosen starting state:\n{print_result(cur_state, cur_value, cur_cost, cur_error)}")
        if cur_error == 0: # find solution
            best_solution = print_result(cur_state, cur_value, cur_cost, cur_error)
            print("\nFound solution:")
            print(best_solution)
            return best_solution 
        
        while True:
            # for neighbous
            neighbours = get_neighbours(cur_state, items)
            if output_flag == 'V':
                print("\nNeighbors:")
                for n in neighbours:
                    n_value, n_cost = value_cost(n)
                    n_error = error_function(n_value, n_cost, target, budget)
                    print(print_result(n, n_value, n_cost, n_error))

            next_state = min(neighbours, key=lambda n: error_function(*value_cost(n), target, budget))
            next_value, next_cost = value_cost(next_state)
            next_error = error_function(next_value, next_cost, target, budget)

            if next_error < cur_error:
                if output_flag == 'V':
                    print("\nMove to " + print_result(next_state, next_value, next_cost, next_error))
                cur_state, cur_value, cur_cost, cur_error = next_state, next_value, next_cost, next_error
            else:
                if output_flag == 'V':
                    print('Search failed.\n')
                break # no improvement, stop 

            if cur_error == 0: # find solution
                best_solution = print_result(cur_state, cur_value, cur_cost, cur_error)
                print("\nFound solution:")
                print(best_solution)
                return best_solution 

    print(best_solution)

def run_hc(filename):
    target, budget, output_flag, restarts, items = read_input(filename)
    hill_climbing(items, target, budget, output_flag, restarts)

def main():
    run_hc('input_hc.txt')
    print('\n1:')
    run_hc('input1_hc.txt')
    print('\n2:')
    run_hc('input2_hc.txt')
    print('\n3:')
    run_hc('input3_hc.txt')
    print('\n4:')
    run_hc('input4_hc.txt')
    print('\n5:')
    run_hc('input5_hc.txt')
    

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:




