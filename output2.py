# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 21:23:10 2024

@author: rackl
"""
import matplotlib.pyplot as plt
import solution3 as sol

role_colors = {
    'Cook': '#D46F1A',
    'Expo': '#ECA61D',
    'Front Counter': '#D6841F',
    'Runner': '#F2D200',
    'Dishwasher': '#C1C1C1',
}


def plot_gantt_chart(schedule, employee_id):
    fig, ax = plt.subplots(figsize=(10, 5))

    # Loop through the schedule and plot each shift
    for shift in schedule:
        day, start_hour, end_hour, role = shift
        ax.barh(day, end_hour - start_hour + 1, left=start_hour, color= role_colors[role], label=f"{role}")
    
    # Customize the chart
    ax.set_yticks(range(5))
    ax.set_yticklabels([f"{sol.weekdays[i]}" for i in range(5)])
    ax.set_xticks(list(range(9,13)) + list(range(1,10)))
    ax.set_xlabel("Hour of the Day")
    ax.set_title(f"Employee {employee_id}'s Work Schedule for Third Formulation")
    
    # Add legend (to show roles)
    handles, labels = ax.get_legend_handles_labels()
    
    # Sort by labels (title)
    sorted_handles_labels = sorted(zip(labels, handles), key=lambda x: x[0])
    sorted_labels, sorted_handles = zip(*sorted_handles_labels)
    
    unique_labels = dict(zip(sorted_labels, sorted_handles))  # Remove duplicate labels
    ax.legend(unique_labels.values(), unique_labels.keys(), loc='upper right')
    
    plt.tight_layout()
    plt.show()


#creating employee schedules from decision variables
schedule = {}
for e in sol.employees:
    schedule[e] = []  # Initialize a schedule for each employee
    for r in sol.roles:
        for h in sol.hours:
            for d in sol.days:
                if sol.x[e, r, h, d].x > 0:  # If the employee is scheduled for this role at this time
                    schedule[e].append((d, h, r))  # Save day, hour, role

plt_schedule = {}
for e in sol.employees:
    plt_schedule[e] = []
    i = 0
    emp_sch = sorted(schedule[e])
    curr_day = emp_sch[0][0]
    start_h = emp_sch[0][1]
    start_r = emp_sch[0][2]
    last_h = 0
    plt_schedule[e].append([sol.weekdays[curr_day], start_h, 0, start_r])
    for (day, hour, role) in emp_sch:
        if day == curr_day and role == start_r and hour == last_h + 1 or last_h == 0:
            last_h = hour
            continue
        plt_schedule[e][i][2] = last_h
        curr_day = day
        start_r = role
        start_h = hour
        plt_schedule[e].append([sol.weekdays[curr_day], start_h, 0, start_r])
        i += 1
        last_h = hour
    else:
        plt_schedule[e][i][2] = last_h

#displaying schedules in output
for e in sol.employees:
    print(f"\nEmployee {e} Schedule:")
    total_hrs = 0
    for day, start, end, role in plt_schedule[e]:
        total_hrs += end - start + 1
        start = str(start + 8) + (" am" if start < 4 else " pm") if start <= 4 else str(start - 4) + " pm"
        end = str(end + 9) + (" am" if end < 3 else " pm") if end <= 3 else str(end - 3) + " pm"
        print(f'    {day} {role} from {start} to {end}')
    print(f'Total hours scheduled: {total_hrs}')

plot_gantt_chart(plt_schedule[11], 11)
plot_gantt_chart(plt_schedule[12], 12)