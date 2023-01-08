"""
Xinghua Peng
DS 2000: Intro to Programming with Data


Date: Fri Sep 16 17:03:32 2022
    
File: wages.py
    
Description: This program runs a summary analysis of the business at the donut shop that day to determine the max amount you can afford to pay employees. 


"""

def main():
    
    # Ask the user which day to read to data for
    
    date = input("What day should we analyze? ")
    profits = "profits_" + date + ".txt"
    employees = "employees_" + date + ".txt"
    
    
    # Open the file and read the data <profits & employees>
    with open(profits, "r") as infile:
        glazed_profits = float(infile.readline())
        
        chocolate_profits = float(infile.readline())
       
        sprinkled_profits = float(infile.readline())
    
    with open(employees, "r") as infile:
        employees_num = int(infile.readline())
        
        employees_hrs = int(infile.readline())
    
    
    # Reports the total profits made on that day from selling donuts
    total_profits = float(glazed_profits + chocolate_profits + sprinkled_profits)
    print("On", date + ", you made $" + str(total_profits) + ".")
    
    # Reads how many employees worked on that day and their hours
    total_hrs = int(employees_num * employees_hrs)
    
    # Compute the hourly wage for the donut shop employees
    # hourly_wage = total profits / total hours worked
    salary = float(total_profits / total_hrs)
    
    # Output and print results
    print(employees_num, "employees worked for", employees_hrs, "hours each, totaling", total_hrs, "hours.")
    print("You should pay your employees $" + str(round(salary,2)), "per hour.")
    
    
    
    
main()

