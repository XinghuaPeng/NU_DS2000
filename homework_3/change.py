"""
Xinghua Peng
DS 2000: Intro to Programming with Data


Date: Sat Sep 24 19:34:57 2022
    
File: change.py
    
Description: This program takes in the price of one US dollar or less for an item from the user then calculates the appropriate change to give back to the user. 


"""

def main():
    
    # Ask the user to enter a number 1 - 100
    price = int(input("Enter price in cents (1-100): "))
    
    # Calculate the change to give them
    if 100 >= price >= 1:
        
        
        # Calculate total changes 
        change_total = int(100 - price)
                
        print("Change to be given:", change_total)
        
        # Calculate quarters to be given to the user
        quarters = change_total // 25
        
        if quarters != 0:
            print("Quarters:", quarters)
        
        # Calculate dimes to be given to the user
        dimes = (change_total % 25) // 10
        
        if dimes != 0:
            print("Dimes:", dimes)
        
        # Calculate nickels to be given to the user
        nickels = (change_total % 25) % 10 // 5
        
        if nickels != 0:
            print("Nickels:", nickels)
        
        # Calculate pennies
        pennies = (change_total % 25) % 10 % 5 // 1
        
        if pennies != 0:
            print("Pennies:", pennies)
   
    else:
        # Inform the user they have entered an incorrect price and exit
        
        print("I'm sorry, you need to enter a number between 1 and 100!")
 
    
main()
