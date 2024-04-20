# Hubs-and-Authority-DPoS

## Overview
This project aims to simulate and analyze a dynamic graph representing a blockchain network's behavior during the consensus algorithm. The primary focus is analysing the performance and fairness of the proposed novel Hubs and Authority based Delegated Proof of Stake (DPoS) consensus algorithm.

## Features
- **Dynamic Graph Generation**: Generates a random directed graph with specified parameters such as the number of nodes, maximum out degree, and number of time steps.
- **Attribute Computation**: Computes various attributes for each node in the graph, including delegate reputation, voter reputation, delegate value, and voter value, based on the DPoS consensus algorithm and hub and authority principles.
- **Malicious Node Detection**: Identifies and penalizes malicious nodes based on their behavior and updates their reputation accordingly.
- **Visualization**: Visualizes the results using bar plots to analyze delegate reputation, frequency of each delegate being chosen, and delegate reputation increase over consensus rounds for non-malicious nodes.

## Requirements
- Python 3.x
- NetworkX
- Matplotlib
- Pandas
- Seaborn

## Usage
1. Clone the repository to your local machine.
2. Run the `main.py` script to execute the simulation and analysis.
3. View the results in the form of bar plots generated by the script.

## Results
The simulation provides insights into the fairness and performance of the DPoS consensus algorithm, along with the effectiveness of hub and authority principles in enhancing node interactions within the blockchain network. Key results include:

- Equal opportunities for non-malicious nodes in becoming delegates.
- Influence of hub and authority principles on delegate reputation and voting behavior.
- Detection and penalization of malicious nodes based on their actions and reputation.
- Visualization of delegate reputation trends and frequency of delegate selection over consensus rounds.

## Future Work
- Further optimization of the DPoS consensus algorithm to enhance fairness and efficiency.
- Exploration of additional metrics and attributes to evaluate blockchain consensus algorithms.
- Integration of real-world data and scenarios to validate simulation results.
- Continuous refinement and improvement of the simulation model based on feedback and research advancements.

## Contributors
- [Jeet Bhadaniya](https://github.com/jeetb2022)
- [Smeet Bhadaniya](https://github.com/Smeet1278) 


