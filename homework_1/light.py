"""
Xinghua Peng
DS 2000: Intro to Programming with Data


Date: Tue Sep 13 18:42:04 2022
    
File: light.py
    
Description: Input an astronomical obeject's distance in miles and report the number of hrs, mins, and secs it taks for light from that object to reach the earth.


"""

# Input an astronomical object's distance in miles 

distance=int(input("Enter distance [miles]: "))

# Convert distance in miles into meters

distance_meters = int(distance * 1.61 * 1000) # <1.61 kms = 1 mile & 1000 meters = 1 kilometer>

# Input light travel's speed

light_speed = int(299792458)

# Compute total numbers of seconds <light travels from the object to Earth>

total_secs = distance_meters / light_speed

# Use % to convert total seconds to numbers of hours, minutes, and seconds

hours = int (total_secs/3600)
minutes = int((total_secs % 3600)/60)
seconds = round (total_secs % 60, 1)

# Print output
print("Light travel time:", str(hours) + "h", str(minutes) + "m", str(seconds) + "s")
