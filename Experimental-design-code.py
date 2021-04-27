# -*- coding: utf-8 -*-

"""
Code for test experiment

"""

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

G= nx.watts_strogatz_graph(10,6,0.1)   # Generated network from watts_strogatz_graph 
Node = nx.nodes(G)
hold = [e for e in G.edges]  #Store the edges of the network
#print(Node)
#print(hold)
#print(hold[0])
#print(type(hold))
nx.draw_networkx(G) #Draw the network


#Intial interaction arcs
Pair, interaction = multidict({
  ('1', '2'):  0,
  ('1', '3'):  0,
  ('1', '4'):  0,
  ('1', '5'):  0,
  ('1', '6'):  0,
  ('1', '7'):  0,
  ('1', '8'):  0,
  ('1', '9'):  0,
  ('1', '10'):  0,

  ('2', '1'):  0,
  ('2', '3'):  0,
  ('2', '4'):  0,
  ('2', '5'):  0,
  ('2', '6'):  0,
  ('2', '7'):  0,
  ('2', '8'):  0,
  ('2', '9'):  0,
  ('2', '10'):  0,

  ('3', '1'):  0,
  ('3', '2'):  0,
  ('3', '4'):  0,
  ('3', '5'):  0,
  ('3', '6'):  0,
  ('3', '7'):  0,
  ('3', '8'):  0,
  ('3', '9'):  0,
  ('3', '10'):  0,
  
  ('4', '1'):  0,
  ('4', '2'):  0,
  ('4', '3'):  0,
  ('4', '5'):  0,
  ('4', '6'):  0,
  ('4', '7'):  0,
  ('4', '8'):  0,
  ('4', '9'):  0,
  ('4', '10'):  0,

  ('5', '2'):  0,
  ('5', '3'):  0,
  ('5', '4'):  0,
  ('5', '1'):  0,
  ('5', '6'):  0,
  ('5', '7'):  0,
  ('5', '8'):  0,
  ('5', '9'):  0,
  ('5', '10'):  0,

  ('6', '2'):  0,
  ('6', '3'):  0,
  ('6', '4'):  0,
  ('6', '5'):  0,
  ('6', '1'):  0,
  ('6', '7'):  0,
  ('6', '8'):  0,
  ('6', '9'):  0,
  ('6', '10'):  0,

  ('7', '2'):  0,
  ('7', '3'):  0,
  ('7', '4'):  0,
  ('7', '5'):  0,
  ('7', '6'):  0,
  ('7', '1'):  0,
  ('7', '8'):  0,
  ('7', '9'):  0,
  ('7', '10'):  0,

  ('8', '2'):  0,
  ('8', '3'):  0,
  ('8', '4'):  0,
  ('8', '5'):  0,
  ('8', '6'):  0,
  ('8', '7'):  0,
  ('8', '1'):  0,
  ('8', '9'):  0,
  ('8', '10'):  0,

  ('9', '1'):  0,
  ('9', '2'):  0,
  ('9', '3'):  0,
  ('9', '4'):  0,
  ('9', '5'):  0,
  ('9', '6'):  0,
  ('9', '7'):  0,
  ('9', '8'):  0,
  ('9', '10'): 0,
  
  ('10', '1'): 0,
  ('10', '2'):  0,
  ('10', '3'):  0,
  ('10', '4'):  0,
  ('10', '5'):  0,
  ('10', '6'):  0,
  ('10', '7'):  0,
  ('10', '8'):  0,
  ('10', '9'):  0,})  #whether interaction exists between node i and j  : a_ij
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
period=[1,2,3,4,5] # day
people=[1,2,3,4,5,6,7,8,9,10] #people

initial_infect_num =2       # The number of initial infected nodes we would like to generate
#I = random.sample(people, initial_infect_num)  # Randomly intialize the infected nodes
I=[1,2,5]#initially infected people i
#print(I)
NI=[]
for i in people:
  if i not in I:
    NI.append(i)

# quarantine limit

q_limit = [1,2,3,4,5]


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
        #m.addConstr(theta[i,t+1] == infected_interact/interact)
        #print(interaction)
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
      m.addConstr(theta[i,t+1]+ z[i,t+1] >=0.16)

for t in period[:-1]:
    for i in people:
      m.addConstr(theta[i,t+1]+ z[i,t+1] <=1.159)  


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
      print('CPU runtime: %g' % m.Runtime) 
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