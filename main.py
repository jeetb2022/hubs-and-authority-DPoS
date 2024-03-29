import random
import networkx as nx
import matplotlib.pyplot as plt

def generate_dynamic_random_directed_graph(num_nodes, max_out_degree, num_steps):
    G = nx.DiGraph()

    # Add nodes
    for i in range(num_nodes):
        attributes = {
        "delegate_reputation": 1,
        "voter_reputation": 1,
        "delegate_value": 1,
        "voter_value" : 1
    }
    G.add_node(i, **attributes)

    # Add edges dynamically
    for step in range(num_steps):
        new_edges = []
        for node in G.nodes():
            out_degree = random.randint(0, max_out_degree)
            possible_targets = list(set(range(num_nodes)) - {node})  # Avoid self-loops
            targets = random.sample(possible_targets, out_degree)
            for target in targets:
                new_edges.append((node, target, {'time': step}))  # Add edge with a specific time

        # Remove edges randomly (commented out for now)
        # for edge in list(G.edges()):
        #     if random.random() < 0.1:  # Probability of edge removal
        #         G.remove_edge(edge[0], edge[1])

    # Add the new edges to the graph
        G.add_edges_from(new_edges)

    list_isMalicious = [[False] * num_steps for _ in range(50)]
    for step in range(num_steps):
        # Declare the delegates list
        delegates = []


        # The delagte value of the nodes is being computed
        for node in G.nodes:
            votes_received=0
            voters_to_delegate=[]

            for predecessor in G.predecessors(node):
             # Check if there is an incoming edge with the specific attribute value
                if G[predecessor][node].get('time') == step:
                    votes_received = votes_received+1
                    # voters_to_delegate.append(predecessor)
            G.nodes[node]['delegate_value'] = votes_received


        # The voter value is being computed
        for node in G.nodes:
            votes_casted=0

            for successor in G.successors(node):
             # Check if there is an incoming edge with the specific attribute value
                if G[node][successor].get('time') == step:
                  # The delegate value of the voted nodes is added to the voter value of the node that it has voting.
                    votes_casted += G.nodes[successor]['delegate_value']
            G.nodes[node]['voter_value'] = votes_casted



        # The delagte value of the nodes is being computed
        for node in G.nodes:
            # print("node",node)
            votes_received=0
            voters_to_delegate=[]

            for predecessor in G.predecessors(node):
             # Check if there is an incoming edge with the specific attribute value
                if G[predecessor][node].get('time') == step:
                    votes_received = votes_received+G.nodes[predecessor]['voter_value']
                    # voters_to_delegate.append(predecessor)
            G.nodes[node]['delegate_value'] = votes_received



        delegate_values = {node: G.nodes[node].get('delegate_value', 0) for node in G.nodes()}
        # print("Step:", step, "Top 5 Delegates:", delegate_values)

        # Sort nodes based on delegate reputations
        sorted_nodes = sorted(delegate_values.items(), key=lambda x: x[1], reverse=True)

        # Get top 5 nodes with highest delegate reputations
        top_5_nodes = [node for node, _ in sorted_nodes[:5]]

        # Add these top 5 nodes to the 'delegates' list
        delegates.extend(top_5_nodes)






        # Reset the delegate value and voter value of all the nodes
        for node in G.nodes:
            G.nodes[node]["delegate_value"] = 1
            G.nodes[node]["voter_value"] = 1



            # Do the processing of votes recievd by the delegate
        print("Step:", step, "Top 5 Delegates:", delegates)
    return G

# Generate the dynamic random directed graph
num_nodes = 50
max_out_degree = 5
num_steps = 10  # Number of time steps
random_dynamic_graph = generate_dynamic_random_directed_graph(num_nodes, max_out_degree, num_steps)

# Save the dynamic graph to a GraphML file
nx.write_graphml(random_dynamic_graph, "random_dynamic_graph.graphml")

# Draw the graph (optional, for visualization in matplotlib)
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(random_dynamic_graph, seed=42)  # Fixed seed for consistent layout
nx.draw(random_dynamic_graph, pos, with_labels=True, node_size=50, node_color='skyblue', font_size=8, edge_color='gray', arrows=True)
plt.title("Dynamic Random Directed Graph with 150 Nodes")
plt.show()
