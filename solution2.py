# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 11:33:33 2024

@author: rackl
"""

import gurobipy as gp
from gurobipy import GRB
import employeedata as ed
import staffingdata as sd

employees = range(14)
roles = list(ed.empl_roles[0].keys())
hours = range(12)
days = range(5)
weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

#adding dummy hour to the start of the day
hours = range(len(hours) + 1)
workable_hrs = range(1, len(hours) + 1)
empl_avail = []
for e in employees:
    availability = []
    for d in days:
        availability.append([0] + ed.empl_avail[e][d])
    empl_avail.append(availability)

role_reqs = {}
for r in roles:
    reqs = []
    for d in days:
        reqs.append([0] + sd.role_reqs[r][d])
    role_reqs.update({r:reqs})

#defining employee availability
availability = {}
for e in employees:
    for d in days:
        for h in hours:
            availability[e, h, d] = empl_avail[e][d][h]


#creating model and decision variables
model = gp.Model("EmployeeScheduling")

x = model.addVars(employees, roles, hours, days, vtype=GRB.BINARY, name="x")
y = model.addVars(employees, roles, hours, days, vtype=GRB.BINARY, name="y")
delta = model.addVars(employees,vtype=GRB.INTEGER, name='delta')


#adding constraints
for e in employees:
    #deviation from desired total hours
    sum_x_over_e = gp.quicksum(x[e,r,h,d] for r in roles for h in hours for d in days)
    model.addConstr(delta[e] >= sum_x_over_e - ed.empl_hours[e][1], name='hr_overmax_' + str(e))
    model.addConstr(delta[e] >= ed.empl_hours[e][0] - sum_x_over_e, name='hr_undermin_' + str(e))
    model.addConstr(delta[e] >= 0, name='hr_geq0_' + str(e))
    
    #employee availability & time-based role exclusivity
    for d in days:
        for h in hours:
            model.addConstr(gp.quicksum(x[e,r,h,d] for r in roles) <= availability[e,h,d], name='avail_' + str(e) + str(h) + str(d))
    
    #role qualification & disallowed overtime
    for r in roles:
        model.addConstr(gp.quicksum(x[e,r,h,d] for h in hours for d in days) <= 40 * ed.empl_roles[e][r], name='qual_&_hr_leq40_' + str(e) + str(r))
    
    for r in roles:
        for d in days:
            for h in hours:
                if h < 10:
                    #minimum shift length
                    model.addConstr(x[e,r,h,d] + x[e,r,h+1,d] + x[e,r,h+2,d] + x[e,r,h+3,d] >= 4 * y[e,r,h,d], name='min_shift_' + str(e) + str(r) + str(h) + str(d))
                    
                    #shift cannot start after a work period
                    model.addConstr(y[e,r,h+1,d] + x[e,r,h,d] + x[e,r,h+1,d] <= 2, name='shift_start_after_' + str(e) + str(r) + str(h) + str(d))
                    #if working now, must have either worked previously or be starting shift
                    model.addConstr(y[e,r,h+1,d] + x[e,r,h,d] - x[e,r,h+1,d] >= 0, name='shift_start_' + str(e) + str(r) + str(h) + str(d))
                    #if shift starts, work starts
                    model.addConstr(y[e,r,h,d] - x[e,r,h,d] <= 0, name='work_start_' + str(e) + str(r) + str(h) + str(d))
                else:
                    #can't start work after hour 9
                    model.addConstr(x[e,r,h-1,d] - x[e,r,h,d] >= 0, name='no_late_work_starts_' + str(e) + str(r) + str(h) + str(d))
                    #can't start shift after hour 9
                    model.addConstr(y[e,r,h,d] == 0, name='no_late_starts_' + str(e) + str(r) + str(h) + str(d))
                 


#restaurant staffing needs
for r in roles:
    for h in hours:
        for d in days:
            model.addConstr(gp.quicksum(x[e,r,h,d] for e in employees) == role_reqs[r][d][h], name='role_reqs_' + str(r) + str(h) + str(d))


model.setObjective(gp.quicksum(delta[e] for e in employees), GRB.MINIMIZE)

model.optimize()
'''
model.computeIIS()

for c in model.getConstrs():
    if c.IISConstr:
        print(f"Infeasible constraint: {c.constrName}")

for v in model.getVars():
    if v.IISLB or v.IISUB:
        print(f"Infeasible variable bound: {v.varName}")
'''

print(f"Number of variables: {model.NumVars}")
print(f"Number of constraints: {model.NumConstrs}")

