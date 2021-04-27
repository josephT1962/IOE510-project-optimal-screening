# -*- coding: utf-8 -*-
"""ioe510_final_project_test.ipynb

Code for Model Formulation
Author:Jianyang Tang

"""

# Commented out IPython magic to ensure Python compatibility.
# %pip install -i https://pypi.gurobi.com gurobipy

from itertools import product
from math import sqrt
import gurobipy as gp
from gurobipy import GRB
from gurobipy import *
import numpy as np
import networkx as nx
import random
#N=[1,2,3,4] # Number of people i
#T=[1,2,3,4,5] # Number of day t

G= nx.watts_strogatz_graph(4,2,1)   # Generated network from watts_strogatz_graph 
Node = nx.nodes(G)
hold = [e for e in G.edges]  #Store the edges of the network
#print(Node)
#print(hold)
#print(hold[0])
#print(type(hold))
#nx.draw_networkx(G) #Draw the network


#Intial interaction arcs
Pair, interaction = multidict({
  ('1', '2'):  0,
  ('1', '3'):  0,
  ('1', '4'):  0,
  ('2', '1'):  0,
  ('2', '3'):  0,
  ('2', '4'):  0,
  ('3', '1'):  0,
  ('3', '2'):  0,
  ('3', '4'):  0,
  ('4', '1'):  0,
  ('4', '2'):  0,
  ('4', '3'):  0})  #whether interaction exists between node i and j  : a_ij
#print(interaction)
for ele in hold:     # Put the edge information we got from the network into the edges of our model aka. put the edges into our model
  i = ele[0]+1  # Plus one because the network count start from 0 although our model count from 1
  j = ele[1]+1
  interaction[(str(i),str(j))] = 1
  interaction[(str(j),str(i))] = 1
#print(interaction)

#Parameters

probability=0.8; #the probability of successful infection of node i from node j

#period=[1,2,3,4,5,6] # day
period=[1,2,3,4,5,6,7,8,9,10,11,12] # day
people=[1,2,3,4] #people

initial_infect_num =2       # The number of initial infected nodes we would like to generate
I = random.sample(people, initial_infect_num)  # Randomly intialize the infected nodes
#I=[1,2]#initially infected people i



NI=[]
for i in people:
  if i not in I:
    NI.append(i)

# quarantine limit
#q_limit = [1,1,1,1,1,1]
q_limit = [0,1,1,1,1,1,1,1,1,1,1,1]
#q_limit = [1,2,2,2,2,2]

print("Initial infected nodes",I)
print("Interaction network", interaction)
print("quarantine limit of each day", q_limit)

#Model formulation
m=gp.Model("IOE510 final project")

#Creat Variables 

x=m.addVars(people,period,vtype=GRB.BINARY, name="x(it)")
#wether node i is tested during time t

v=m.addVars(people,period,vtype=GRB.BINARY,name="v(it)")
#wether node i is infected during time t

#r=m.addVars(people,period,vtype=GRB.BINARY,name="r(it)")
#wether node i is recovered during time t

theta=m.addVars(people,period,name="theta(it)")
#probability that node i gets infected at time t

z=m.addVars(people,period,vtype=GRB.BINARY,name="z(it)")
#if theta(it)<0.5,z=0, theta(it)>=0.5,z=1

alpha=m.addVars(people,period,vtype=GRB.BINARY,name="alpha(it)")

beta=m.addVars(people,period,vtype=GRB.BINARY,name="beta(it)")

#some nodes initially infected
# initialinfect=m.addConstrs((v[i,1]==1 for i in I), "initialinfect")
for j in I:
    m.addConstr(v[j,1]==1)

for i in NI:
   m.addConstr(v[i,1]==0)

#theta definition
for t in period[:-1]:
    for i in people :
        
        infected_interact=0
        interact = 0
        for j in people:
          if i == j:
            continue 
          #infected_interact+=(probability*v[j,t]*interaction[(str(i),str(j))]*(1-x[j,t]))  #Before linearlizing
          infected_interact+=(probability*v[j,t]*interaction[(str(i),str(j))]-probability*alpha[j,t]*interaction[(str(i),str(j))]) #Linearized
          interact+=interaction[(str(i),str(j))] 
        #print(infected_interact)
        #print(interact)
        if interact ==0:
          m.addConstr(theta[i,t+1] == 0)
          continue
        m.addConstr(theta[i,t+1] == infected_interact/len(people))

#Use alpha to linearized x[i,t]*v[i,t]
for t in period:
  for i in people:
    m.addConstr(alpha[i,t]>=x[i,t]+v[i,t]-1)
    m.addConstr(alpha[i,t]<=x[i,t]) 
    m.addConstr(alpha[i,t]<=v[i,t])  


for t in period[:-1]:
    for i in people:
      m.addConstr(x[i,t+1]>=x[i,t])

#z constraints
for t in period[:-1]:
    for i in people:
      m.addConstr(theta[i,t+1]+ z[i,t+1] >=0.5)

for t in period[:-1]:
    for i in people:
      m.addConstr(theta[i,t+1]+ z[i,t+1] <=1.499)  


# #Dicide wether node i is infected in the next period 
for t in period[:-1]:
  for i in people:
      #m.addConstr(v[i,t+1]==(1-(1-v[i,t])*z[i,t+1]))  #Before linearizing
      #m.addConstr(v[i,t+1]==(1-z[i,t+1]+z[i,t+1]*v[i,t]))
      m.addConstr(v[i,t+1]==(1-z[i,t+1]+beta[i,t+1]))  #Linearized

#Use beta to linearized z[i,t+1]*v[i,t]
for t in period[:-1]:
  for i in people:
    m.addConstr(beta[i,t+1]>=z[i,t+1]+v[i,t]-1)
    m.addConstr(beta[i,t+1]<=z[i,t+1]) 
    m.addConstr(beta[i,t+1]<=v[i,t])  


#numbers of quarantine limit
for t in period: 
    test_people_t =0
    for i in people:
       test_people_t += x[i,t]
    m.addConstr(test_people_t <= q_limit[t-1])


for t in period[:-1]:   # node got infected for the whole period since it got infected
  for i in people:
    m.addConstr(v[i,t+1] >= v[i,t])

obj=0
for i in people:
  obj += v[i,period[-1]]  #Summation i in N Summation t in T v_it
  #print(period[-1])

m.setObjective(obj, GRB.MINIMIZE); # Set the minimize objective function 

m.optimize()

if m.status == GRB.Status.OPTIMAL:    
     print('\nCost: %g' % m.objVal)    
     for v in m.getVars():
       print('%s %g' % (v.varName, v.x))
else:    
     print('No solution')


if m.status == GRB.Status.INFEASIBLE:
        print('Optimization was stopped with status %d' % m.status)
        # do IIS, find infeasible constraints
        m.computeIIS()
        m.write("model.ilp")
