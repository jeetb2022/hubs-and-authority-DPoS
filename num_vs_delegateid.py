import random
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

# Initialize an empty list to store the delegates for each step
all_delegates = defaultdict(int)

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
        # print(new_edges[0])
        G.add_edges_from(new_edges)

    # num_steps=1000
    for step in range(num_steps):

        for node in G.nodes:
            num_incoming_edges = G.in_degree(node)
            if (num_incoming_edges == 0):

                print("This node with id : ",node,"has 0 votes")
        # Declare the delegates list
        delegates = []
        total_delegate_value=0.01;

        # The delagte value of the nodes is being computed
# The delegate value is being computed
        for node in G.nodes:
            votes_received = 0

            for predecessor in G.predecessors(node):
                # Check if there is an incoming edge with the specific attribute value
                # print( G.edges[predecessor,node]['time'] )
                if G.edges[predecessor,node]['time'] == step:
                    votes_received += 1
                # if G.nodes[predecessor].get('time') == step:
                #     votes_received += 1
            # if (votes_received == 0 ):
            #     print("This node with id : ",node,"has 0 votes")
            G.nodes[node]['delegate_value'] = votes_received

        # The voter value is being computed


        for node in G.nodes:
            votes_casted = 0

            for successor in G.successors(node):
                # Check if there is an incoming edge with the specific attribute value
                if G.edges[node,successor]['time'] == step:
                    votes_casted += G.nodes[successor]['delegate_value']

                # if G.nodes[successor].get('time') == step:
                #     # The delegate value of the voted nodes is added to the voter value of the node that it has voting.
                    # votes_casted += G.nodes[successor]['delegate_value']

            G.nodes[node]['voter_value'] = votes_casted

        # The delagte value of the nodes is being computed
        for node in G.nodes:
            # print("node",node)
            votes_received=0
            voters_to_delegate=[]

            for predecessor in G.predecessors(node):
             # Check if there is an incoming edge with the specific attribute value
                if G.edges[predecessor,node]['time'] == step:
                    votes_received += G.nodes[predecessor]['voter_value']
                # if G.nodes[predecessor].get('time') == step:
                #     votes_received = votes_received+G.nodes[predecessor]['voter_value']
                    # voters_to_delegate.append(predecessor)
            G.nodes[node]['delegate_value'] = votes_received

        # for node in G.nodes:
            # print(G.nodes[node].get('delegate_value'))
            # total_delegate_value+=G.nodes[node].get('delegate_value')

        delegate_values = {node: G.nodes[node].get('delegate_value') for node in G.nodes()}
        # print("Step:", step, "Top 5 Delegates:", delegate_values)

        # Sort nodes based on delegate reputations
        sorted_nodes = sorted(delegate_values.items(), key=lambda x: (x[1], random.random()), reverse=True)

        # Get top 5 nodes with highest delegate reputations
        top_5_nodes = [node for node, _ in sorted_nodes[:5]]
        # all_delegates.append(top_5_nodes)

        # Add these top 5 nodes to the 'delegates' list
        delegates.extend(top_5_nodes)
        #     if G[predecessor][node]['time'] == step:
        # if 'voter_value' in G.nodes[predecessor]:
        #     votes_received += G.nodes[predecessor]['voter_value']
        print("Step:", step, "Top 5 Delegates:", delegates)
        # malicious_ids = input("Enter malicious nodes:")
        # malicious_node_id = list(map(int, malicious_ids.split()))
        malicious_node_id = [31]



        #calculates the total delegate value of every delegate node
        for delegate in delegates:
            # print(G.nodes[delegate].get('delegate_value'))
            all_delegates[delegate] = all_delegates[delegate] +1;
            total_delegate_value+=G.nodes[delegate].get('delegate_value')

        # print("Step:", step, "Top 5 Delegates:", delegates)
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

        nodes_to_remove=[]
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

            # Do the processing of votes recievd by the delegate
    # Convert the list of lists to a DataFrame
        # df = pd.DataFrame(all_delegates)

        # Write the DataFrame to an Excel file
        # df.to_excel('delegates.xlsx', index=False, header=False)


    return G

# Generate the dynamic random directed graph
num_nodes = 150
max_out_degree = 5
num_steps = 10000 # Number of time steps
random_dynamic_graph = generate_dynamic_random_directed_graph(num_nodes, max_out_degree, num_steps)

# Save the dynamic graph to a GraphML file
nx.write_graphml(random_dynamic_graph, "random_dynamic_graph.graphml")



import matplotlib.pyplot as plt
import seaborn as sns

# Flatten the list of lists to get all delegate values
categories = list(all_delegates.keys())
frequencies = list(all_delegates.values())

# Create bar plot
plt.figure(figsize=(8, 5))
plt.bar(categories, frequencies, color='skyblue')
plt.xlabel('Delegate Id')
plt.ylabel('Number of times chosen delegate')
plt.title('Frequency of Each Occurrence')
plt.show()
