"""
Xinghua Peng
DS 2000: Intro to Programming with Data


Date: Sat Sep 24 19:35:17 2022
    
File: simulation.py
    
Description: A program that repeatedly rolls three 6-sided dice and calculates how often the three dice all have different values. 
 

"""
# Import the package
import random as rnd


def main(): 
    
    
    iteration_num = 0
    x = 1
    
    while x < 5:
        total_times = 10 ** x # Rolling dice <10 & 100 & 1000 & 10000> times 
        mismatched_rolls = 0
    
        while iteration_num < total_times:
            dice_num_1 = rnd.randint(1,6) # rolls three 6-sided dice
            dice_num_2 = rnd.randint(1,6)
            dice_num_3 = rnd.randint(1,6)
        
            # define mis-matched rolls
            if dice_num_1 != dice_num_2 and dice_num_3 != dice_num_1 and dice_num_2!= dice_num_3:
                mismatched_rolls += 1
                
            iteration_num += 1
         
        # Calculate experimental probability
        probability = mismatched_rolls / total_times
        
        # Print output & results
        print("Rolling dice", total_times, "times.")
        print("Number of mis-matched rolls:", mismatched_rolls)
        print("Experimental probability:", probability)
        print('\n')
        
        x += 1

main()