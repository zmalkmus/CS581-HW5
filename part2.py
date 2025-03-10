import argparse

def read_graph(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    num_nodes, num_edges = map(int, lines[0].split())
    
    graph = {i: {} for i in range(num_nodes)}
    max_node = 0

    for line in lines[1:]:
        u, v, capacity = map(int, line.split())
        graph[u][v] = capacity
        if v not in graph:
            graph[v] = {}
        if u not in graph[v]:
            graph[v][u] = 0
        max_node = max(max_node, u, v)

    source = 0  # The source is always node 0
    sink = max_node  # The sink is the largest node ID found

    return num_nodes, num_edges, graph, source, sink

def ford_fulkerson(graph, source, sink):
    # From the book:
    # FORD-FULKERSON -METHOD (G, s, t)
    # 1 initialize ﬂow f to 0
    # 2 while there exists an augmenting path p in the residual network Gf
    # 3   augment ﬂow f along p
    # 4 return f

    def dfs_find_path(residual_graph, u, t, visited, path):
        if u == t:
            return path
        visited.add(u)
        for v, capacity in residual_graph[u].items():
            if capacity > 0 and v not in visited:
                result = dfs_find_path(residual_graph, v, t, visited, path + [(u, v, capacity)])
                if result:
                    return result

        return None

    # Initialize flow to 0
    max_flow = 0
    augmenting_paths = []

    # While there exists an augmenting path p in the residual network Gf
    while True:
        visited = set()
        # Find an augmenting path
        path = dfs_find_path(graph, source, sink, visited, [])

        if not path:
            break  # No more augmenting paths
        
        path_flow = min(capacity for _, _, capacity in path)
        augmenting_paths.append(path)

        # Augment flow along path
        for u, v, capacity in path:
            graph[u][v] -= path_flow
            if v not in graph:
                graph[v] = {}
            if u not in graph[v]:
                graph[v][u] = 0
            graph[v][u] += path_flow

        max_flow += path_flow
        
    # Return max flow and augmenting paths
    return max_flow, augmenting_paths

def main():
    parser = argparse.ArgumentParser(description='Network Flow using Ford-Fulkerson Method from the Book')
    parser.add_argument('file', type=str, help='Flow network in DIMACS format')
    args = parser.parse_args()
    file_path = args.file

    num_nodes, num_edges, graph, source, sink = read_graph(file_path)
    # print(f"Number of nodes: {num_nodes}")
    # print(f"Number of edges: {num_edges}")
    # print(f"Graph: {graph}")
    # print(f"Source -> Sink: {source} -> {sink}")

    max_flow, augmenting_paths = ford_fulkerson(graph, source, sink)
    print(f"Max Flow: {max_flow}")
    
    print("\nAugmenting Paths:")
    for i, path in enumerate(augmenting_paths, 1):
        vertices = [str(u) for u, _, _ in path] + [str(path[-1][1])] if path else []
        bottleneck = min(capacity for _, _, capacity in path) if path else 0
        print(f"Path {i}: {' -> '.join(vertices)} | Capacity: {bottleneck}")


if __name__ == "__main__":
    main()