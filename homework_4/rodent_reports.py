""" Xinghua Peng
    DS 2000: Intro to Programming with Data
    Homework 4
    Oct 10, 2022
    File: rodent_reports.py
    
    Description: This program generate a map of rodent reports in Boston and 
    use bar charts to compare the relative number of rodent reports in different
    neighborhoods in Boston.
"""
import matplotlib.pyplot as plt
#  Define a constant to store the filename of the data file ???
filename = "rodents_311_2021.csv"

#Method 2 of defining constants
#FILENAME_BIG = "rodents_311_2021.csv"
#FILENAME_SMALL = "rodents_311_2021_small.csv"

def main():
    
    # Read in the provided data
    
    neighborhoods = []
    latitude = []
    longitude = []
    
    with open(filename, "r") as infile:
        # Skip the header
        header = infile.readline()
        lines = infile.readlines()
    index = 0
    while index < len(lines):
        
        # split lines into pieces / values
        vals = lines[index].split(",")
        # Ignore rows that have no neighboardhood
        if vals[0] == " ":
            index += 1
        # Read the data into three lists (latitude / longitude / neighborhoods)
        else:
            neighborhoods.append(str(vals[0]))
            latitude.append(float(vals[1]))
            longitude.append(float(vals[2]))

            index += 1
    
    # Scatter plot creation -- Map of Rodent Reports
    # Add a point representing Northeastern
    #neighborhoods.append("Northeastern")
    #latitude.append(42.3398)
    #longitude.append(-71.0892)
    neu_longitude = [-71.0892]
    neu_latitude = [42.3398]
    # Provide the label included in the legend
    plt.plot(longitude, latitude, ".", color="blue", label="Rodent Reports")
    # Place a marker for easier identification for Northeastern
    plt.plot(neu_longitude, neu_latitude, "*", color="red", label="Northeastern")

    # plot customization
    plt.title("Map of Rodent Reports in Boston 2021")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.legend()
    plt.savefig("boston_rodents.pdf", bbox_inches = "tight")
    plt.show()


    # Print Output
    # Print the total number of rodent reports in the data
    print("Total rodent reports assigned to a valid neighborhood:", len(neighborhoods))
    print("\n")
    # Find the different unique neighborhoods in the dataset in sorted order
    unique_neighborhoods = []
    for x in neighborhoods:
        if x not in unique_neighborhoods:
            unique_neighborhoods.append(x)
    unique_neighborhoods.sort()
    print("Neighborhoods:")
    # Print the neighborhoods list in new line
    for x in unique_neighborhoods:
       print(x)
    print("\n")
    
    # Method 2 - Use join function
    #print("\n".join(map(str,unique_neighborhoods)))
    
    #  Bar chart creation -- Rodent Report Comparison for Neighborhoods
    # Compute each neighborhoods' rodent reports
    
    x = 0
    counts = []
    
    while x < len(unique_neighborhoods):
        counts.append(neighborhoods.count(unique_neighborhoods[x]))
        x += 1
    
    #print(counts)
    
    color = ["dodgerblue","orangered", "green", "red", "mediumorchid", "saddlebrown", "violet", "lightslategray", "olive", "cyan"]
    plt.bar(unique_neighborhoods, counts,color=color)
    
    # plot customization
    plt.title("Rodent Report Comparison for Neighborhoods")
    plt.xlabel("Neighborhoods")
    plt.ylabel("Rodent Report Count")
    plt.xticks(rotation = 90)
    plt.savefig("neighborhoods.pdf", bbox_inches = "tight")
    plt.show()
    
    
    # Calculate and print the avergae number of rodent reports for Boston neighborhoods
    avg_reports = len(neighborhoods) / len(unique_neighborhoods)
    #print(len(neighborhoods))
    #print(int(sum(unique_neighborhoods))
    print("Average number of rodent reports", avg_reports)
    
    
    
main()