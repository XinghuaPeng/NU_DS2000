"""
Xinghua Peng
DS 2000: Intro to Programming with Data


Date: Tue Sep 13 13:21:35 2022
    
File: running.py
    
Description: A program where a runner inputs their running distance and time, and output the average pace measured in minutes per mile. 


"""

# Input running parameters: distance and time <mins & secs>

distance_km = float(input("Enter distance [km]: "))

time_mins = int (input("Enter time [minutes]: "))
time_secs = int (input("Enter time [seconds]: "))

# Convert kilometers to miles <1.61 kilometers = 1 mile>

distance_mi = float(distance_km / 1.61)

# Convert seconds to minutes
# Calculate total minutes used for the run <60 seconds = 1 minute>

total_mins = float(time_mins + (time_secs / 60))

# Compute average pace measured in minutes per mile
# Pace = time / distance

pace = total_mins / distance_mi

# Convert pace into minutes and seconds section
pace_mins = int (pace)
pace_secs = pace - int(pace_mins)

# Convert minutes into seconds & Round
secs_actual = round(pace_secs * 60,1)

# Print Output
print ("Your pace was", pace_mins, "minutes", secs_actual, "seconds per mile.")
