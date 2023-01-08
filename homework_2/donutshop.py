"""
Xinghua Peng
DS 2000: Intro to Programming with Data


Date: Fri Sep 16 17:03:05 2022
    
File: donutshop.py
    
Description: This program asks the user what kind of donut and how many donuts they'd like and report their donuts cost and profits the donut shop made from this sale. 


"""

def main():
    
    # Ask the user what kind of donut they'd like / Get the name of the data file from user
    filename = input("What kind of donut would you like [glazed, chocolate, sprinkled]? ")
    filename = filename + ".txt"
    #print(filename)
    
    # Ask the user how many donuts they'd like / Get the number of donuts from user
    number_donuts = int(input("How many donuts would you like? "))
    
    # Open the file and read the data
    with open(filename, "r") as infile:
        sale_price = float(infile.readline())
        cost = float(infile.readline())

    
    ## Analyze the purchase
    # Compute and output the price you need to pay
    total_price = float(number_donuts * sale_price)
    print("Please pay: $" + str(total_price))
    
    # Compute and output the profits made by the shop
    profit = float(number_donuts * (sale_price - cost))
    print("This sale made us $" + str(round(profit,2)) + "!")
    
    # Print ending sentence
    print("Enjoy your donuts!")
    

main()
    
    