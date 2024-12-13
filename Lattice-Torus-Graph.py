from itertools import product

def generate_cartesian_product(cycles, paths):

    dimensions = cycles + paths
    is_cycle = [True] * len(cycles) + [False] * len(paths)

    all_nodes = list(product(*(range(d) for d in dimensions)))

    graph = {node: [] for node in all_nodes}

    for node in all_nodes:
        for dim, (length, cycle_flag) in enumerate(zip(dimensions, is_cycle)):
            
            if cycle_flag:  # Cycle: wrap around
                prev_node = list(node)
                next_node = list(node)
                prev_node[dim] = (node[dim] - 1) % length
                next_node[dim] = (node[dim] + 1) % length
                graph[node].append(tuple(prev_node))
                graph[node].append(tuple(next_node))
            else:  # Path: no wrap-around
                if node[dim] > 0:
                    prev_node = list(node)
                    prev_node[dim] -= 1
                    graph[node].append(tuple(prev_node))
                if node[dim] < length - 1:
                    next_node = list(node)
                    next_node[dim] += 1
                    graph[node].append(tuple(next_node))

    return graph


def count_maximal_independent_sets(graph):
    
    def is_order_3_maximal(graph, independent_set):

        #Maximal check
        for node in graph:
            if node not in independent_set:
                if all(neighbor not in independent_set for neighbor in graph[node]):
                    return False
        return True
    
        for vertex_to_remove in independent_set:
            
            candidate_set = independent_set - {vertex_to_remove}
            
            forbidden_vertices = set(candidate_set) | {neighbor for v in candidate_set for neighbor in graph[v]}
            potential_additions = [v for v in graph if v not in forbidden_vertices]

            for v1 in range(len(potential_additions)):
                for v2 in range(v1 + 1, len(potential_additions)):
                    extended_set = candidate_set | {potential_additions[v1], potential_additions[v2]}
                    if is_independent_set(graph, extended_set):
                        return False
        return True

    def is_independent_set(graph, independent_set):
        for node in independent_set:
            for neighbor in graph[node]:
                if neighbor in independent_set:
                    return False
        return True

    def dfs(remaining_nodes, current_set):
        if not remaining_nodes:
            return 1 if is_order_3_maximal(graph, current_set) else 0

        node = remaining_nodes[0]
        rest = remaining_nodes[1:]

        # Include node
        include_set = current_set | {node}
        include_rest = [n for n in rest if n not in graph[node]]
        count_with_node = dfs(include_rest, include_set)

        # Exclude node
        count_without_node = dfs(rest, current_set)

        return count_with_node + count_without_node

    nodes = list(graph.keys())
    result = dfs(nodes, set())
    return result

def input_list(prompt):
    user_input = input(prompt)
    
    if not user_input.strip():
        return []
    
    return [int(item.strip()) for item in user_input.split(',')]


# ------------------- #

while True:
    print("------------------------------")
    print("Enter the size of each Path and Cycle Graph. Separate the elements by commas.")
    cycles = input_list("Enter the cycles graphs: ")
    paths = input_list("Enter the cycle graphs: ")

    graph = generate_cartesian_product(cycles, paths)
    result = count_maximal_independent_sets(graph)
    print("------------------------------")
    print("Cycles:",cycles)
    print("Paths:",paths)
    #print("Number of Order-3 Maximal Independent Sets:", result)
    print(result)



''' Code for large datasets

data = []
for i in range(3, 21):
    for j in range(2, 21):
        
        cycles = [i]
        paths = [j]
        graph = generate_cartesian_product(cycles, paths)
        
        result = count_maximal_independent_sets(graph)
        data.append({"i": i, "j": j, "result": result})
        print(f"Processed ({i}, {j}): {result}")
        

print(f"Data saved to {output_file}")

'''
