
def find_paths(graph, traversed, start, finish):
    # If we hit the target node then we just return it
    # as a list so the caller can append to it.
    if start == finish:
        return [start]

    # Need to keep track of the nodes we've already
    # visited to ensure we don't get infinite recursion
    traversed = traversed.copy()
    traversed.extend(start)

    # Find all the possible paths to the target via any of our children
    paths = []
    for child in graph[start].keys():
        # Don't go to any node that we've already visited.
        if child not in traversed:
            for path in find_paths(graph, traversed, child, finish):
                new_path = [start]
                new_path.extend(path)
                paths.append(new_path)
    return paths


def compute_cost(graph, path):
    # 1) path with be something like ['a', 'b', 'c']
    # 2) Using the zip will turn this into [('a','b'), ('b','c')]
    # 3) Then we get the cost from the original graph
    return sum([graph[pair[0]][pair[1]] for pair in zip(path[:-1], path[1:])])


def shortest_path(graph, start, end):
    """
       Input: graph: a dictionary of dictionary
              start: starting city   Ex. a
              end:   target city     Ex. b

       Output: tuple of (distance, [path of cites])
       Ex.   (distance, ['a', 'c', 'd', 'b])
    """
    paths = find_paths(graph, [], start, end)
    costs = [(compute_cost(graph, path), path) for path in paths]
    return min(costs, key=lambda cost: cost[0])
