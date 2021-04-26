# IOE510-project-optimal-screening

For this project, we created a model to express the epidemic in a social network,
in which nodes represent people and arcs represent if there exist social interactions among two persons.
Initially, some nodes of this network get infected and other nodes do not.
We used the Watts-Strogatz model to randomly generate the interaction between nodes and the initially infected node.
We set minimizing total infections at the end of the time horizon as our objective function.
Finally, we evaluated our model, implemented in Python, by using the programming solver Gurobi.
