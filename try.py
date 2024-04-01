import random
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Initialize an empty list to store the delegates for each step
all_delegates = []

def generate_dynamic_random_directed_graph(num_nodes, max_out_degree, num_steps):
    G = nx.DiGraph()
    attributes = {
        "delegate_reputation": 1,
        "voter_reputation": 1,
        "delegate_value": 1,
        "voter_value" : 1,
        "delegate_curr_flag" : 0,
        "delegate_max_flag" : 0,
    }
    
    # Add nodes
    for i in range(num_nodes):
        G.add_node(i, **attributes)

    # Add edges dynamically
    for step in range(num_steps):
        new_edges = []
        for node in G.nodes():
            out_degree = random.randint(0, max_out_degree)
            possible_targets = list(set(range(num_nodes)) - {node})  # Avoid self-loops
            targets = random.sample(possible_targets, out_degree)
            for target in targets:
                if G.nodes[target].get('delegate_curr_flag') == 0:
                    new_edges.append((node, target, {'time': step}))  # Add edge with a specific time

        # Add the new edges to the graph
        G.add_edges_from(new_edges)

    for step in range(num_steps):
        # Declare the delegates list
        delegates = []
        total_delegate_value = 0.01

        for i in range(4):
            for node in G.nodes:
                votes_received = G.nodes[node].get('delegate_value', 0)
                for predecessor in G.predecessors(node):
                    if G.edges[predecessor, node]['time'] == step:
                        votes_received += 1
                G.nodes[node]['delegate_value'] = votes_received

            for node in G.nodes:
                votes_casted = G.nodes[node].get('voter_value', 0)
                for successor in G.successors(node):
                    if G.edges[node, successor]['time'] == step:
                        votes_casted += G.nodes[successor]['delegate_value']
                G.nodes[node]['voter_value'] = votes_casted

        delegate_values = {node: G.nodes[node].get('delegate_value') for node in G.nodes()}
        sorted_nodes = sorted(delegate_values.items(), key=lambda x: (-x[1], random.random()))
        top_5_nodes = [node for node, _ in sorted_nodes[:5]]
        all_delegates.append(top_5_nodes)
        delegates.extend(top_5_nodes)

        malicious_node_id = [70]
        for delegate in delegates:
            if delegate in malicious_node_id:
                G.nodes[delegate]['delegate_max_flag'] = G.nodes[delegate].get('delegate_max_flag', 0) + 1
                G.nodes[delegate]['delegate_curr_flag'] = pow(2, G.nodes[delegate].get('delegate_max_flag')) + 1
                G.nodes[delegate]['delegate_reputation'] = G.nodes[delegate].get('delegate_reputation', 1) - (G.nodes[delegate].get('delegate_value') / total_delegate_value)
                for predecessor in G.predecessors(delegate):
                    if G.nodes[delegate].get('delegate_value') != 0:
                        G.nodes[predecessor]['voter_reputation'] = G.nodes[predecessor].get('voter_reputation', 1) - G.nodes[predecessor].get('voter_value') / G.nodes[delegate].get('delegate_value')
            else:
                G.nodes[delegate]['delegate_reputation'] = G.nodes[delegate].get('delegate_reputation', 1) + (G.nodes[delegate].get('delegate_value') / total_delegate_value) / 5
                for predecessor in G.predecessors(delegate):
                    if G.nodes[delegate].get('delegate_value') != 0:
                        G.nodes[predecessor]['voter_reputation'] = G.nodes[predecessor].get('voter_reputation', 1) + G.nodes[predecessor].get('voter_value') / G.nodes[delegate].get('delegate_value')

        # List of nodes to remove
        nodes_to_remove = []
        for node in G.nodes:
            G.nodes[node]['delegate_value'] = 1
            G.nodes[node]['voter_value'] = 1
            if G.nodes[node].get('delegate_curr_flag') is not None and G.nodes[node].get('delegate_curr_flag') > 0:
                G.nodes[node]['delegate_curr_flag'] = G.nodes[node].get('delegate_curr_flag') - 1
            if G.nodes[node].get('delegate_max_flag') == 3:
                nodes_to_remove.append(node)

        # Remove nodes marked for removal
        for node in nodes_to_remove:
            G.remove_node(node)

        # Do the processing of votes received by the delegate

        # Convert the list of lists to a DataFrame
        df = pd.DataFrame(all_delegates)

        # Write the DataFrame to an Excel file
        df.to_excel('delegates.xlsx', index=False, header=False)

    return G

# Generate the dynamic random directed graph
num_nodes = 150
max_out_degree = 5
num_steps = 1000  # Number of time steps
random_dynamic_graph = generate_dynamic_random_directed_graph(num_nodes, max_out_degree, num_steps)

# Save the dynamic graph to a GraphML file
nx.write_graphml(random_dynamic_graph, "random_dynamic_graph.graphml")

# Draw the graph (optional, for visualization in matplotlib)
# plt.figure(figsize=(12, 8))
# pos = nx.spring_layout(random_dynamic_graph, seed=42)  # Fixed seed for consistent layout
# nx.draw(random_dynamic_graph, pos, with_labels=True, node_size=50, node_color='skyblue', font_size=8, edge_color='gray', arrows=True)
# plt.title("Dynamic Random Directed Graph with 150 Nodes")
# plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Flatten the list of lists to get all delegate values
all_delegates_flat = [val for sublist in all_delegates for val in sublist]

# Plotting the histogram
plt.figure(figsize=(10, 6))
sns.histplot(all_delegates_flat, kde=True, bins=50, color='blue')
plt.title('Distribution of Delegate Values')
plt.xlabel('Delegate Id')
plt.ylabel('Frequency')
plt.show()
