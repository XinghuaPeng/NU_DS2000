"""
Xinghua Peng
DS 2000: Intro to Programming with Data


Date: Fri Sep 16 17:02:41 2022
    
File: applecider.py
    
Description: This program read the data from one donut_ratings text file and print out the maximum & minimum donut rating. 


"""

def main():
    
    # Get the name of the data file from user
    filename = input("Which donut rating file? ")
    #print(filename)
    
    # Open the file and read the data from one donut_ratings file
    with open(filename, "r") as infile:
        shop_1 = infile.readline().strip()
        rating_1 = float(infile.readline())
        
        shop_2 = infile.readline().strip()
        rating_2 = float(infile.readline())
        
        shop_3 = infile.readline().strip()
        rating_3 = float(infile.readline())
        
        shop_4 = infile.readline().strip()
        rating_4 = float(infile.readline())
    
    
    # Compare and output the maximum donut rating
    maximum_rating = max(rating_1, rating_2, rating_3, rating_4)
    
    print("Maximum (best) donut rating:", maximum_rating)
    
    # Compare and output the minimum donut rating
    minimum_rating = min(rating_1, rating_2, rating_3, rating_4)
        
    print("Minimum (worst) donut rating:", minimum_rating)
    

main()

