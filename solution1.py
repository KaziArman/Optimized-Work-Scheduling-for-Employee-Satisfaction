import gurobipy as gp
from gurobipy import GRB
import employeedata as ed
import staffingdata as sd

employees = range(14)
roles = list(ed.empl_roles[0].keys())
hours = range(12)
days = range(5)
weekdays = ["Monday","Tuesday","Wednesday","Thursday","Friday"]

availability = {}

for e in employees:
    for d in days:
        for h in hours:
            availability[e, h, d] = ed.empl_avail[e][d][h]


model = gp.Model("EmployeeScheduling")

x = model.addVars(employees, roles, hours, days, vtype=GRB.BINARY, name="x")
delta = model.addVars(employees,vtype=GRB.INTEGER, name='delta')

for e in employees:
    sum_x_over_e = gp.quicksum(x[e,r,h,d] for r in roles for h in hours for d in days)
    model.addConstr(delta[e] >= sum_x_over_e - ed.empl_hours[e][1], name='hr_overmax_' + str(e))
    model.addConstr(delta[e] >= ed.empl_hours[e][0] - sum_x_over_e, name='hr_undermin_' + str(e))
    model.addConstr(delta[e] >= 0, name='hr_geq0_' + str(e))
    
    for d in days:
        for h in hours:
            model.addConstr(gp.quicksum(x[e,r,h,d] for r in roles) <= availability[e,h,d], name='avail_' + str(e) + str(h) + str(d))
    
    for r in roles:
        #rethink this in regards to role assignments
        model.addConstr(gp.quicksum(x[e,r,h,d] for h in hours for d in days) <= 40 * ed.empl_roles[e][r], name='qual_&_hr_leq40_' + str(e) + str(r))

for r in roles:
    for h in hours:
        for d in days:
            model.addConstr(gp.quicksum(x[e,r,h,d] for e in employees) == sd.role_reqs[r][d][h], name='role_reqs_' + str(r) + str(h) + str(d))

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
