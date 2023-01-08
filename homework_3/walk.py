"""
Xinghua Peng
DS 2000: Intro to Programming with Data


Date: Sat Sep 24 19:35:35 2022
    
File: walk.py
    
Description: This program plot the position of the squirrel as a function of time over 1000 seconds. 


"""

# Import the package
import random as rnd
import matplotlib.pyplot as plt
#import numpy as np

def main():
    
    time = 0
    position = 0
    
    while time <= 1000: 
        direction = rnd.randint(0,1)
        
        if direction == 0 : 
            position = position - 1
            
        elif direction == 1 :
            position = position + 1
        
        
        #col = (np.random.random(), np.random.random(), np.random.random())
        plt.plot(time, position, ".", color = "orangered")
        
        time += 1
        
    ## Plot Customization
    
    # Set the x-axis and y-axis label for the graph
    plt.xlabel("Time")
    plt.ylabel("Position")
    
    # Set the title for the graph
    plt.title("Squirrel's Position vs. Time")
    
    # Save the graph and exclude extra whitespace around the graph
    plt.savefig("walk.png", bbox_inches = "tight")
    
    # Display the current graph
    plt.show()
    
    
main()
    