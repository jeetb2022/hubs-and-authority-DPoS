import random
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

# Initialize an empty list to store the delegates for each step
all_delegates = defaultdict(int)
delegate_reputations = defaultdict(int)
voter_reputations = defaultdict(int)
soledelgate_value = defaultdict(int)
total_delegate_value_dict = defaultdict(int)
       # Record reputations for plotting
       
def generate_dynamic_random_directed_graph(num_nodes, max_out_degree, num_steps):
    G = nx.DiGraph()
    attributes = {
        "delegate_reputation": 60,
        "voter_reputation": 60,
        "delegate_value": 1,
        "voter_value" : 1,
        "delegate_curr_flag" : 0,
        "delegate_max_flag" : 0,
        "voter_curr_flag" : 0,
        "voter_max_flag" : 0,

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
                # if G.nodes[target].get('delegate_curr_flag') == 0:
                new_edges.append((node, target, {'time': step}))  # Add edge with a specific time

        # Add the new edges to the graph
        G.add_edges_from(new_edges)
        print("\n",len(new_edges))

    return G

def compute(G, num_steps):

    for step in range(num_steps):

        delegates = []
        total_delegate_value=0.01

        for i in range (5):

            for node in G.nodes:
                votes_received = G.nodes[node].get('delegate_value')

                for predecessor in G.predecessors(node):
                                # Check if there is an incoming edge with the specific attribute value
                    if G.has_edge(predecessor, node) and 'time' in G[predecessor][node]:
                        if G.nodes[node].get('delegate_curr_flag') > 0:
                            votes_received += 0                       
                        elif G[predecessor][node]['time'] == step:
                            if G.nodes[predecessor].get('voter_curr_flag') == 0:
                                votes_received += G.nodes[node].get('voter_value')

                G.nodes[node]['delegate_value']+= votes_received



            # The voter value is being computed
            for node in G.nodes:
                votes_casted = G.nodes[node].get('voter_value')

                for successor in G.successors(node):
                    # Check if there is an incoming edge with the specific attribute value
                    if G.nodes[node].get('voter_curr_flag') > 0:
                            votes_casted += 0  
                    elif G.edges[node,successor].get('time') == step:
                         if G.nodes[successor].get('delegate_curr_flag') == 0: 
                            votes_casted += G.nodes[successor].get('delegate_value')

                G.nodes[node]['voter_value'] = votes_casted


        delegate_values = {node: G.nodes[node].get('delegate_value') for node in G.nodes()}
        # print("Step:", step, "Top 5 Delegates:", delegate_values)

        # Sort nodes based on delegate reputations
        sorted_nodes = sorted(delegate_values.items(), key=lambda x: (x[1], random.random()), reverse=True)

        # Get top 5 nodes with highest delegate reputations
        top_5_nodes = [node for node, _ in sorted_nodes[:5]]
        # all_delegates.append(top_5_nodes)

        # Add these top 5 nodes to the 'delegates' list
        delegates.extend(top_5_nodes)

        print("Step:", step, "Top 5 Delegates:", delegates)
        # malicious_ids = input("Enter malicious nodes:")
        # malicious_node_id = list(map(int, malicious_ids.split()))
        malicious_node_id = [45]
        if (step % 2 == 0 ):
            malicious_node_id.append([45]);
        



        #calculates the total delegate value of every delegate node
        for delegate in delegates:
            all_delegates[delegate] = all_delegates[delegate] +1
            total_delegate_value+=G.nodes[delegate].get('delegate_value')

        total_delegate_value_dict[total_delegate_value] = total_delegate_value_dict[total_delegate_value] + 1
        for delegate in delegates:
            # print(G.nodes[delegate].get('delegate_value'))
            if delegate in malicious_node_id:
                G.nodes[delegate]['delegate_max_flag'] = G.nodes[delegate].get('delegate_max_flag', 0) + 1
                G.nodes[delegate]['delegate_curr_flag']=pow(2,G.nodes[delegate].get('delegate_max_flag'))+1
                G.nodes[delegate]['delegate_reputation']=G.nodes[delegate].get('delegate_reputation',1)-(G.nodes[delegate].get('delegate_value')/total_delegate_value*5)

                for predecessor in G.predecessors(delegate):
                    if G.nodes[delegate].get('delegate_value') != 0:
                        G.nodes[predecessor]['voter_reputation']= G.nodes[predecessor].get('voter_reputation',1)-G.nodes[predecessor].get('voter_value')/G.nodes[delegate].get('delegate_value')


            else:
                G.nodes[delegate]['delegate_reputation']=G.nodes[delegate].get('delegate_reputation',1)+((100-G.nodes[delegate].get('delegate_reputation',1))*((G.nodes[delegate].get('delegate_value')/total_delegate_value)))
                for predecessor in G.predecessors(delegate):
                    if G.nodes[delegate].get('delegate_value') != 0:
                        G.nodes[predecessor]['voter_reputation'] = G.nodes[predecessor].get('voter_reputation',1) +(100 - G.nodes[predecessor].get('voter_reputation',1))*(G.nodes[predecessor].get('voter_value') / (G.nodes[delegate].get('delegate_value')))


        # Reset the delegate value and voter value of all the nodes

        nodes_to_remove=[]
        for node in G.nodes:
            G.nodes[node]['delegate_value'] = 1
            G.nodes[node]['voter_value'] = 1
            if G.nodes[node].get('delegate_curr_flag') is not None and G.nodes[node].get('delegate_curr_flag') > 0:
                G.nodes[node]['delegate_curr_flag'] = G.nodes[node].get('delegate_curr_flag') - 1
            if G.nodes[node].get('delegate_max_flag') == 3:
                nodes_to_remove.append(node)
            if G.nodes[node].get('voter_curr_flag') is not None and G.nodes[node].get('voter_curr_flag') > 0:
                G.nodes[node]['voter_curr_flag'] = G.nodes[node].get('voter_curr_flag') - 1
            if G.nodes[node].get('voter_max_flag') == 3:
                nodes_to_remove.append(node)

        for node in G.nodes:
            delegate_reputations[node] = (G.nodes[node].get('delegate_reputation'))
            voter_reputations[node] =(G.nodes[node].get('voter_reputation'))
            if G.nodes.get(45) is not None:
                soledelgate_value[step] = (G.nodes[45].get('delegate_reputation'))
            else:
                soledelgate_value[step] = 0
        for node in nodes_to_remove:
            G.remove_node(node)

    return G

# Generate the dynamic random directed G
num_nodes = 50
max_out_degree = 5
num_steps = 100  # Number of time steps
random_dynamic_graph = generate_dynamic_random_directed_graph(num_nodes, max_out_degree, num_steps)
random_dynamic_graph2 = compute(random_dynamic_graph,num_steps)

# Save the dynamic graph to a GraphML file
nx.write_graphml(random_dynamic_graph, "random_dynamic_graph.graphml")



import matplotlib.pyplot as plt
import seaborn as sns



# Flatten the list of lists to get all delegate values
categories = list(delegate_reputations.keys())
frequencies = list(delegate_reputations.values())
categories2 = list(all_delegates.keys())
frequencies2 = list(all_delegates.values())
categories3 = list(soledelgate_value.keys())
frequencies3 = list(soledelgate_value.values())
categories4 = list(total_delegate_value_dict.keys())
frequencies4 = list(total_delegate_value_dict.values())

# Create bar plot

plt.figure(figsize=(8, 5))
plt.bar(categories, frequencies, color='skyblue')
plt.xlabel('Delegate Id')
plt.ylabel('Delegate reputation')
plt.title('Delegate reputation of every node')
plt.figure(figsize=(8, 5))
plt.bar(categories2, frequencies2, color='skyblue')
plt.xlabel('Delegate Id')
plt.ylabel('Number of times chosen delegate')
plt.title('Frequency of Each Occurrence')
plt.bar(categories3, frequencies3, color='skyblue')
plt.xlabel('Consensus round')
plt.ylabel('Delegate reputation')
plt.title('Delegate reputation increase of a non malicious node')
# plt.figure(figsize=(8, 5))
# plt.bar(categories4, frequencies4, color='skyblue')
# plt.xlabel('Delegate Id')
# plt.ylabel('Total delegate reputation')
# plt.title('Total delegate reputation of one plot')
plt.show()