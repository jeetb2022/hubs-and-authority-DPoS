import random
import networkx as nx
import matplotlib.pyplot as plt

def generate_dynamic_random_directed_graph(num_nodes, max_out_degree, num_steps):
    G = nx.DiGraph()
    attributes = {
        "delegate_reputation": 1,
        "voter_reputation": 1,
        "delegate_value": 0,
        "voter_value" : 0,
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
            # if G.nodes[node].get("delegate_curr_flag") == 0:
            out_degree = random.randint(0, max_out_degree)
            possible_targets = list(set(range(num_nodes)) - {node})  # Avoid self-loops
            targets = random.sample(possible_targets, out_degree)
            for target in targets:
                new_edges.append((node, target, {'time': step}))  # Add edge with a specific time

        # Add the new edges to the graph
        G.add_edges_from(new_edges)


    for step in range(num_steps):
        # Declare the delegates list
        delegates = []
        total_delegate_value=0;

        # The delagte value of the nodes is being computed
        for node in G.nodes:
            votes_received=0

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

        for node in G.nodes:
            print(G.nodes[node].get('delegate_value'))
            # total_delegate_value+=G.nodes[node].get('delegate_value')

        delegate_values = {node: G.nodes[node].get('delegate_value', 0) for node in G.nodes()}
        # print("Step:", step, "Top 5 Delegates:", delegate_values)

        # Sort nodes based on delegate reputations
        sorted_nodes = sorted(delegate_values.items(), key=lambda x: x[1], reverse=True)

        # Get top 5 nodes with highest delegate reputations
        top_5_nodes = [node for node, _ in sorted_nodes[:5]]

        # Add these top 5 nodes to the 'delegates' list
        delegates.extend(top_5_nodes)
        print("Step:", step, "Top 5 Delegates:", delegates)
        malicious_ids = input("Enter malicious nodes:")
        malicious_node_id = list(map(int, malicious_ids.split()))

        #calculates the total delegate value of every delegate node
        for delegate in delegates:
            # print(G.nodes[delegate].get('delegate_value'))
            total_delegate_value+=G.nodes[delegate].get('delegate_value')
        
        for delegate in delegates:
            if delegate in malicious_node_id:
                G.nodes[delegate]['delegate_max_flag'] = G.nodes[delegate].get('delegate_max_flag', 0) + 1
                G.nodes[delegate]['delegate_curr_flag']=pow(2,G.nodes[delegate].get('delegate_max_flag'))+1
                G.nodes[delegate]['delegate_reputation']=G.nodes[delegate].get('delegate_reputation',1)-(G.nodes[delegate].get('delegate_value')/total_delegate_value)

                for predecessor in G.predecessors(delegate):
                    if G.nodes[delegate].get('delegate_value') != 0:
                        G.nodes[predecessor]['voter_reputation']= G.nodes[predecessor].get('voter_reputation',1)-G.nodes[predecessor].get('voter_value')/G.nodes[delegate].get('delegate_value')


            else:
                G.nodes[delegate]['delegate_reputation']=G.nodes[delegate].get('delegate_reputation',1)+(G.nodes[delegate].get('delegate_value')/total_delegate_value)/5
                for predecessor in G.predecessors(delegate):
                    if G.nodes[delegate].get('delegate_value') != 0:
                        G.nodes[predecessor]['voter_reputation'] = G.nodes[predecessor].get('voter_reputation',1) +G.nodes[predecessor].get('voter_value') / G.nodes[delegate].get('delegate_value')



            






        # Reset the delegate value and voter value of all the nodes
        for node in G.nodes:
            G.nodes[node]['delegate_value'] = 0     
            G.nodes[node]['voter_value'] = 0
            if G.nodes[node].get('delegate_curr_flag') is not None and G.nodes[node].get('delegate_curr_flag') > 0:
                G.nodes[node]['delegate_curr_flag'] = G.nodes[node].get('delegate_curr_flag') - 1
            if G.nodes[node].get('delegate_max_flag') == 3:
                G.remove_node(node)  # Corrected 'remove_nodes' to 'remove_node'


            # Do the processing of votes recievd by the delegate
        # print("Step:", step, "Top 5 Delegates:", delegates)
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