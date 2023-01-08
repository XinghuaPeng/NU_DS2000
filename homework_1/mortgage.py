"""
Xinghua Peng
DS 2000: Intro to Programming with Data


Date: Tue Sep 13 18:14:37 2022
    
File: mortgage.py
    
Description: Write a program to calculate monthly mortgage payment.


"""

# Input the principal loan amount, annual interest rate, and years

p = int(input("Principal loan amount: "))
i = float(input("Annual interest rate : "))
y = int(input("Loan terms (years)   : "))

# Covert annual interest rate to monthly interest rate

r = i / 12

# Compute total numbers of payments

n = y * 12 # making 12 monthly payments per year

# Calculate monthly mortgage payment using the formula
# payment = [ P * r * (1 + r) ** n ] / [ (1 + r) ** n - 1]

payment = round(float((p * r * (1+r) ** n)/((1+r) ** n - 1)),2)

# Print Output

print("Monthly payment      :", payment)


