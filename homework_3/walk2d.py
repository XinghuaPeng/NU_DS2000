"""
Xinghua Peng
DS 2000: Intro to Programming with Data


Date: Sat Sep 24 19:35:48 2022
    
File: walk2d.py
    
Description: An updated version of the walk.py. This program plot the position pf the squirrel in two dimensions. 


"""

# Import the package
import random as rnd
import matplotlib.pyplot as plt

def main():
   
    time = 0
    positions_SN = 0
    positions_WE = 0
    
    while time <= 1000:
        
        # 1: South, 2: North, 3 & 4: West, 5 & 6: East
        walk_choice = rnd.randint(1,6) 
        
        if walk_choice == 1:
            positions_SN = positions_SN - 1
            
        elif walk_choice == 2:
             positions_SN = positions_SN + 1
             
        elif walk_choice == 3 or walk_choice == 4:
             positions_WE = positions_WE - 1
             
        elif walk_choice == 5 or walk_choice == 6:
                 positions_WE = positions_WE + 1
                 
        
        plt.plot(positions_WE, positions_SN, "o", color = "blue")
        
        time += 1
    
    # Set the x-axis and y-axis label for the graph
    plt.xlabel("West <---> East")
    plt.ylabel("South <---> North")
    
    # Set the title for the graph
    plt.title("Squirrel's walk in 2 dimensions")
    
    # Save the graph and exclude extra whitespace around the graph
    plt.savefig("walk2d.png", bbox_inches = "tight")
    
    # Display the current graph
    plt.show()
  
      
main()