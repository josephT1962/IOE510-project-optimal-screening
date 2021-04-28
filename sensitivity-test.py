# -*- coding: utf-8 -*-

"""
Code for sensitivity test 

"""

# %pip install -i https://pypi.gurobi.com gurobipy

from itertools import product
from math import sqrt
import gurobipy as gp
from gurobipy import GRB
from gurobipy import *
import numpy as np
import networkx as nx

#N=[1,2,3,4] # Number of people i
#T=[1,2,3,4,5] # Number of day t

#G= nx.watts_strogatz_graph(20,7,0.15)   # Generated network from watts_strogatz_graph 
#Node = nx.nodes(G)
#hold = [e for e in G.edges]  #Store the edges of the network
#print(Node)
#print(hold)
#print(hold[0])
#print(type(hold))
#nx.draw_networkx(G) #Draw the network


#Intial interaction arcs
Pair, interaction = multidict({
  ('1', '2'):  1,
  ('1', '3'):  1,
  ('1', '4'):  1,
  ('1', '5'):  0,
  ('1', '6'):  0,
  ('1', '7'):  0,
  ('1', '8'):  0,
  ('1', '9'):  0,
  ('1', '10'): 0,
  ('1', '11'): 0,
  ('1', '12'): 0,
  ('1', '13'): 0,
  ('1', '14'): 0,
  ('1', '15'): 0,
  ('1', '16'): 0,
  ('1', '17'): 0,
  ('1', '18'): 1,
  ('1', '19'): 1,
  ('1', '20'): 1,
  
  ('2', '1'):  1,
  ('2', '3'):  0,
  ('2', '4'):  0,
  ('2', '5'):  1,
  ('2', '6'):  0,
  ('2', '7'):  0,
  ('2', '8'):  0,
  ('2', '9'):  0,
  ('2', '10'): 0,
  ('2', '11'): 0,
  ('2', '12'): 0,
  ('2', '13'): 0,
  ('2', '14'): 0,
  ('2', '15'): 1,
  ('2', '16'): 0,
  ('2', '17'): 0,
  ('2', '18'): 1,
  ('2', '19'): 1,
  ('2', '20'): 1,
  
  ('3', '1'):  1,
  ('3', '2'):  0,
  ('3', '4'):  1,
  ('3', '5'):  0,
  ('3', '6'):  0,
  ('3', '7'):  0,
  ('3', '8'):  0,
  ('3', '9'):  0,
  ('3', '10'): 0,
  ('3', '11'): 0,
  ('3', '12'): 0,
  ('3', '13'): 0,
  ('3', '14'): 0,
  ('3', '15'): 1,
  ('3', '16'): 0,
  ('3', '17'): 0,
  ('3', '18'): 0,
  ('3', '19'): 0,
  ('3', '20'): 1,
  
  ('4', '1'):  1,
  ('4', '2'):  1,
  ('4', '3'):  1,
  ('4', '5'):  1,
  ('4', '6'):  1,
  ('4', '7'):  1,
  ('4', '8'):  0,
  ('4', '9'):  0,
  ('4', '10'): 0,
  ('4', '11'): 1,
  ('4', '12'): 0,
  ('4', '13'): 0,
  ('4', '14'): 0,
  ('4', '15'): 0,
  ('4', '16'): 0,
  ('4', '17'): 0,
  ('4', '18'): 0,
  ('4', '19'): 0,
  ('4', '20'): 0,
  
  ('5', '1'):  1,
  ('5', '2'):  0,
  ('5', '3'):  0,
  ('5', '4'):  1,
  ('5', '6'):  1,
  ('5', '7'):  1,
  ('5', '8'):  1,
  ('5', '9'):  0,
  ('5', '10'): 0,
  ('5', '11'): 0,
  ('5', '12'): 0,
  ('5', '13'): 0,
  ('5', '14'): 0,
  ('5', '15'): 0,
  ('5', '16'): 0,
  ('5', '17'): 0,
  ('5', '18'): 0,
  ('5', '19'): 0,
  ('5', '20'): 0,
  
  ('6', '2'):  0,
  ('6', '3'):  1,
  ('6', '4'):  1,
  ('6', '5'):  1,
  ('6', '1'):  0,
  ('6', '7'):  1,
  ('6', '8'):  1,
  ('6', '9'):  1,
  ('6', '10'): 0,
  ('6', '11'): 0,
  ('6', '12'): 0,
  ('6', '13'): 0,
  ('6', '14'): 0,
  ('6', '15'): 0,
  ('6', '16'): 0,
  ('6', '17'): 0,
  ('6', '18'): 0,
  ('6', '19'): 0,
  ('6', '20'): 0,
  
  ('7', '2'):  0,
  ('7', '3'):  0,
  ('7', '4'):  1,
  ('7', '5'):  1,
  ('7', '6'):  1,
  ('7', '1'):  0,
  ('7', '8'):  1,
  ('7', '9'):  1,
  ('7', '10'): 1,
  ('7', '11'): 0,
  ('7', '12'): 0,
  ('7', '13'): 0,
  ('7', '14'): 0,
  ('7', '15'): 0,
  ('7', '16'): 0,
  ('7', '17'): 0,
  ('7', '18'): 0,
  ('7', '19'): 0,
  ('7', '20'): 0,
  
  ('8', '2'):  0,
  ('8', '3'):  0,
  ('8', '4'):  0,
  ('8', '5'):  1,
  ('8', '6'):  1,
  ('8', '7'):  1,
  ('8', '1'):  0,
  ('8', '9'):  1,
  ('8', '10'): 1,
  ('8', '11'): 0,
  ('8', '12'): 0,
  ('8', '13'): 0,
  ('8', '14'): 0,
  ('8', '15'): 0,
  ('8', '16'): 0,
  ('8', '17'): 0,
  ('8', '18'): 0,
  ('8', '19'): 0,
  ('8', '20'): 0,
  
  ('9', '2'):  0,
  ('9', '3'):  0,
  ('9', '4'):  0,
  ('9', '5'):  0,
  ('9', '6'):  1,
  ('9', '7'):  1,
  ('9', '8'):  1,
  ('9', '1'):  0,
  ('9', '10'): 1,
  ('9', '11'): 1,
  ('9', '12'): 1,
  ('9', '13'): 0,
  ('9', '14'): 1,
  ('9', '15'): 0,
  ('9', '16'): 0,
  ('9', '17'): 0,
  ('9', '18'): 0,
  ('9', '19'): 0,
  ('9', '20'): 0,
  
  ('10', '2'):  0,
  ('10', '3'):  0,
  ('10', '4'):  0,
  ('10', '5'):  0,
  ('10', '6'):  0,
  ('10', '7'):  1,
  ('10', '8'):  1,
  ('10', '9'):  1,
  ('10', '1'):  0,
  ('10', '11'): 1,
  ('10', '12'): 1,
  ('10', '13'): 1,
  ('10', '14'): 0,
  ('10', '15'): 0,
  ('10', '16'): 0,
  ('10', '17'): 0,
  ('10', '18'): 0,
  ('10', '19'): 0,
  ('10', '20'): 0,
  
  ('11', '2'):  0,
  ('11', '3'):  0,
  ('11', '4'):  0,
  ('11', '5'):  0,
  ('11', '6'):  0,
  ('11', '7'):  0,
  ('11', '8'):  0,
  ('11', '9'):  1,
  ('11', '10'): 1,
  ('11', '1'): 0,
  ('11', '12'): 1,
  ('11', '13'): 1,
  ('11', '14'): 1,
  ('11', '15'): 0,
  ('11', '16'): 0,
  ('11', '17'): 0,
  ('11', '18'): 0,
  ('11', '19'): 0,
  ('11', '20'): 0,
  
  ('12', '2'):  0,
  ('12', '3'):  0,
  ('12', '4'):  0,
  ('12', '5'):  0,
  ('12', '6'):  0,
  ('12', '7'):  0,
  ('12', '8'):  0,
  ('12', '9'):  1,
  ('12', '10'): 1,
  ('12', '11'): 1,
  ('12', '1'): 0,
  ('12', '13'): 1,
  ('12', '14'): 1,
  ('12', '15'): 0,
  ('12', '16'): 0,
  ('12', '17'): 0,
  ('12', '18'): 0,
  ('12', '19'): 0,
  ('12', '20'): 1,
   
  ('13', '2'):  0,
  ('13', '3'):  0,
  ('13', '4'):  0,
  ('13', '5'):  0,
  ('13', '6'):  0,
  ('13', '7'):  0,
  ('13', '8'):  0,
  ('13', '9'):  0,
  ('13', '10'): 1,
  ('13', '11'): 1,
  ('13', '12'): 1,
  ('13', '1'): 0,
  ('13', '14'): 1,
  ('13', '15'): 1,
  ('13', '16'): 1,
  ('13', '17'): 0,
  ('13', '18'): 0,
  ('13', '19'): 0,
  ('13', '20'): 0,
  
  
  ('14', '2'):  0,
  ('14', '3'):  0,
  ('14', '4'):  0,
  ('14', '5'):  0,
  ('14', '6'):  0,
  ('14', '7'):  0,
  ('14', '8'):  0,
  ('14', '9'):  1,
  ('14', '10'): 0,
  ('14', '11'): 1,
  ('14', '12'): 1,
  ('14', '13'): 1,
  ('14', '1'): 0,
  ('14', '15'): 1,
  ('14', '16'): 0,
  ('14', '17'): 1,
  ('14', '18'): 0,
  ('14', '19'): 0,
  ('14', '20'): 0,
  
  ('15', '2'):  1,
  ('15', '3'):  1,
  ('15', '4'):  0,
  ('15', '5'):  0,
  ('15', '6'):  0,
  ('15', '7'):  0,
  ('15', '8'):  1,
  ('15', '9'):  0,
  ('15', '10'): 0,
  ('15', '11'): 0,
  ('15', '12'): 0,
  ('15', '13'): 1,
  ('15', '14'): 1,
  ('15', '1'): 0,
  ('15', '16'): 1,
  ('15', '17'): 1,
  ('15', '18'): 1,
  ('15', '19'): 0,
  ('15', '20'): 0,
  
  ('16', '2'):  0,
  ('16', '3'):  0,
  ('16', '4'):  0,
  ('16', '5'):  0,
  ('16', '6'):  0,
  ('16', '1'):  0,
  ('16', '7'):  0,
  ('16', '8'):  1,
  ('16', '9'):  0,
  ('16', '10'): 0,
  ('16', '11'): 0,
  ('16', '12'): 0,
  ('16', '13'): 1,
  ('16', '14'): 0,
  ('16', '15'): 0,
  ('16', '17'): 0,
  ('16', '18'): 1,
  ('16', '19'): 1,
  ('16', '20'): 0,
  
  ('17', '2'):  0,
  ('17', '3'):  0,
  ('17', '4'):  0,
  ('17', '5'):  0,
  ('17', '6'):  0,
  ('17', '7'):  0,
  ('17', '8'):  0,
  ('17', '9'):  0,
  ('17', '10'): 0,
  ('17', '11'): 0,
  ('17', '12'): 0,
  ('17', '13'): 0,
  ('17', '14'): 1,
  ('17', '15'): 1,
  ('17', '16'): 0,
  ('17', '1'): 1,
  ('17', '18'): 1,
  ('17', '19'): 1,
  ('17', '20'): 1,
  
  ('18', '2'):  0,
  ('18', '3'):  0,
  ('18', '4'):  0,
  ('18', '5'):  0,
  ('18', '6'):  0,
  ('18', '7'):  0,
  ('18', '8'):  0,
  ('18', '9'):  0,
  ('18', '10'): 0,
  ('18', '11'): 0,
  ('18', '12'): 0,
  ('18', '13'): 0,
  ('18', '14'): 0,
  ('18', '15'): 1,
  ('18', '16'): 1,
  ('18', '17'): 1,
  ('18', '1'): 1,
  ('18', '19'): 1,
  ('18', '20'): 1,
  
  ('19', '2'):  1,
  ('19', '3'):  0,
  ('19', '4'):  0,
  ('19', '5'):  0,
  ('19', '6'):  0,
  ('19', '7'):  0,
  ('19', '8'):  0,
  ('19', '9'):  0,
  ('19', '10'): 0,
  ('19', '11'): 0,
  ('19', '12'): 0,
  ('19', '13'): 0,
  ('19', '14'): 0,
  ('19', '15'): 0,
  ('19', '16'): 1,
  ('19', '17'): 1,
  ('19', '18'): 1,
  ('19', '1'):  1,
  ('19', '20'): 1,
  
  ('20', '2'):  1,
  ('20', '3'):  1,
  ('20', '4'):  0,
  ('20', '5'):  0,
  ('20', '6'):  0,
  ('20', '7'):  1,
  ('20', '8'):  0,
  ('20', '9'):  0,
  ('20', '10'): 0,
  ('20', '11'): 0,
  ('20', '12'): 1,
  ('20', '13'): 0,
  ('20', '14'): 0,
  ('20', '15'): 0,
  ('20', '16'): 0,
  ('20', '17'): 1,
  ('20', '18'): 1,
  ('20', '19'): 1,
  ('20', '1'): 1, })  #whether interaction exists between node i and j  : a_ij



#Parameters

probability=0.75; #the probability of successful infection of node i from node j

period=[1,2,3,4,5,6] # day
people=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20] #people

I=[1,2,10]#initially infected people i
print(I)
NI=[]
for i in people:
  if i not in I:
    NI.append(i)

q_limit = [0,1,3,4,5,6]



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
      m.addConstr(theta[i,t+1]+ z[i,t+1] >=0.1125)

for t in period[:-1]:
    for i in people:
      m.addConstr(theta[i,t+1]+ z[i,t+1] <=1.11249)  


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