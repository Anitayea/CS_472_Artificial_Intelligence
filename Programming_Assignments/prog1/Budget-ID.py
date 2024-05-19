#!/usr/bin/env python
# coding: utf-8

# In[1]:


# read the file and save a list of target, budget, output flag and items
def read_input(file_name):
    with open(file_name, 'r') as file:
        lines = file.readlines()
    
    target, budget, output_flag = map(str.strip, lines[0].split())
    target, budget = int(target), int(budget)
    items = [line.strip().split() for line in lines[1:]]
    items = [(item[0], int(item[1]), int(item[2])) for item in items]  # (name, value, cost)
    
    return target, budget, output_flag, items


# In[2]:


# dfs, and display the results
def id_search(target, budget, items, output_flag):
    depth = 1
    solution = None
    while solution is None and depth <= len(items):
        solution, trace = depth_limited_search([], items, target, budget, depth, [])
        if output_flag == 'V':
            print(f"Depth = {depth}.")
            for state in trace:
                print(state)
        if solution:
            break
        depth += 1
    
    if solution:
        solution_str = ' '.join([item[0] for item in solution])
        total_value = sum([item[1] for item in solution])
        total_cost = sum([item[2] for item in solution])
        if output_flag == 'V':
            print(f"\nFound solution {{{solution_str}}}. Value = {total_value}. Cost = {total_cost}.")
        else:
            print(f"Found solution {{{solution_str}}}. Value = {total_value}. Cost = {total_cost}.")
    else:
        print("No Solution")


# In[3]:


# iterative deepening: iteratively search for the state
def depth_limited_search(path, items, target, budget, limit, trace, last_added_index=-1):
    if sum(item[1] for item in path) >= target and sum(item[2] for item in path) <= budget:
        return path, trace
    if limit == 0 or last_added_index >= len(items) - 1:
        return None, trace
    
    for index, item in enumerate(items):
        if index <= last_added_index:
            continue
        new_path = path + [item]
        new_trace = f"{{{' '.join([x[0] for x in new_path])}}}. Value = {sum([x[1] for x in new_path])}. Cost = {sum([x[2] for x in new_path])}."
        if sum([x[2] for x in new_path]) <= budget:
            trace.append(new_trace)
            solution, trace = depth_limited_search(new_path, items, target, budget, limit-1, trace, index)
            if solution:
                return solution, trace
    
    return None, trace


# In[4]:


def run_id(filename):
    file_name = filename
    target, budget, output_flag, items = read_input(file_name)
    id_search(target, budget, items, output_flag)


# In[5]:


def main():
    run_id('input.txt')
    print('\n 1:')
    run_id('input1.txt')
    print('\n 2:')
    run_id('input2.txt')
    print('\n 3:')
    run_id('input3.txt')
    print('\n 4:')
    run_id('input4.txt')
    print('\n 5:')
    run_id('input5.txt')


# In[6]:


if __name__ == "__main__":
    main()


# In[ ]:




