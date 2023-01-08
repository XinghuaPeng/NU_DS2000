""" Xinghua Peng
    DS 2000: Intro to Programming with Data
    Homework 6
    Oct 28, 2022
    File: heart_explore.py
    Description: This program analyze heart disease data and help doctors identtify
    patients at risk of heart disease by generating an patient information report.
    
    Program Output: 
        Number of patients: 918
        Number of patients with heart disease: 508
        Average age: 53.510893246187365
        Average age of patients with heart disease: 55.8996062992126
        Average resting blood pressure: 132.39651416122004
        Average resting blood pressure of patients with heart disease: 134.18503937007873

"""
# Import package as needed
import matplotlib.pyplot as plt

# Define a constant (filename)
HEART_FILE = "heart.csv"

# Define a collection of functions & Code in a modular style
def read_data(filename):
    """ Read the heart disease data into a list of lists
    filename - name of the .csv file containing the data
    return - File data in the form of a list of lists containing six attributes
    (Age, Sex, ChestPainType, RestingBP, Cholesterol, MaxHR, HeartDisease) """
    
    # Store heart disease data
    data = []

    with open(filename, "r") as infile:
        # Skip the header
        infile.readline()

        for line in infile.readlines():
            # Extract values
            vals = line.strip().split(",")

            # (Age,Sex,ChestPainType,RestingBP,Cholesterol,MaxHR,HeartDisease)
            # Convert numeric values to numeric data types as appropriate
            age = int(vals[0])
            sex = vals[1]
            chestpain_type = vals[2]
            resting_bp = int(vals[3])
            cholesterol = int(vals[4])
            maximum_hr = int(vals[5])
            heartdisease = int(vals[6])

            # Store data into lists of lists
            patient = [age, sex, chestpain_type, resting_bp, cholesterol, maximum_hr, heartdisease] 
            data.append(patient)

    return data


def lookup_patients(data):
    """ Find a filtered list of lists that contains only rows with patients with heart disease
    data - full heart disease dataset - list of lists containing six attributes
    return - a list of lists that contains only rows with patients with heart disease """
    
    attrs = []
    for i in data:  
        # 
        if i[6] == 1:
            attrs.append(i)

    return attrs


def extract_column(data, colidx):
    """ Extract one specific column as a list from the list of lists
    data - full heart disease dataset - list of lists containing six attributes
    colidx - the index of the column to be extracted
    return - a list of every value in that specific column """
    
    col = []
    for row in data:
        col.append(row[colidx])
    
    return col


def avg(L):
    """ Compute the numerical average of a list
    L - list being calculated
    return - numerical average"""
    
    sum = 0
    for item in L:
        # Compute the sum value
        sum += item  
    # compute the numerical average
    mean = sum / len(L)
    
    return mean


def generate_user_report(data):
    """ Answer the questions and display the report to the user
    data - full heart disease dataset - list of lists containing six attributes
    return - None (patients information report) """
    
    # How many patients are there total?
    # total patients - length of the list
    total = len(data)

    # How many patients with heart disease?
    heart_disease_data = lookup_patients(data)
    # total patients with heart disease - length of the list
    heart_disease_total = len(heart_disease_data)

    # What is the average age of patients?
    # Retrieve all patients' age data
    all_age = extract_column(data, 0)
    # Calculate the numerical average
    all_age_average = avg(all_age)

    # What is the average age of patients who have heart disease?
    # Retrieve all patients' age data (with heart disease)
    heart_disease_age = extract_column(heart_disease_data, 0)
    # Calculate the numerical average
    heart_disease_age_average = avg(heart_disease_age)

    # What is the average resting blood pressure of patients?
    # Retrieve resting blood pressure of patients' data
    bp = extract_column(data, 3)
    # Calculate the numerical average
    bp_average = avg(bp)

    # What is the average resting blood pressure of patients who have heart disease?
    # Retrieve resting blood pressure of patients' data (with heart disease)
    heart_disease_bp = extract_column(heart_disease_data, 3)
    # Calculate the avergae 
    heart_disease_bp_average = avg(heart_disease_bp)

    # print and display the well-labeled answers to the user
    print("Number of patients:", total)
    print("Number of patients with heart disease:", heart_disease_total)
    print("Average age:", all_age_average)
    print("Average age of patients with heart disease:", heart_disease_age_average)
    print("Average resting blood pressure:", bp_average)
    print("Average resting blood pressure of patients with heart disease:", heart_disease_bp_average)


def visualize_heart(data):
    """ Plot Cholesterol (y-axis) vs. Maximum Heart Rate (x-axis) for all patients
    data - full heart disease dataset - list of lists containing six attributes
    return - None """

    # Record Cholesterol on y-axis & Maximum Heart Rate on x-axis
    y = extract_column(data, 4)
    x = extract_column(data, 5)

    # Retrieve the true value of heart disease in the last column
    heart_disease = extract_column(data, 6)

    # Color code the markers
    # Use the true value of heart disease to decide on color
    colors = []
    for i in heart_disease:
        if i == 1:
            # Patients with heart disease are red
            colors.append('r')
        else:
            # Patients without heart disease are blue
            colors.append('b')

    # Label the axes and set the title
    plt.xlabel("Maximum Heart Rate")
    plt.ylabel("Cholesterol")
    plt.title("Cholesterol vs. Maximum Heart Rate for Patients")

    # Generate a scatter plot
    plt.scatter(x, y, marker=".", color=colors)
    plt.savefig("heart.png")
    plt.show()


def main():
    # Read the heart disease data
    data = read_data(HEART_FILE)
    # Answer the questions and display answers to the user
    generate_user_report(data)
    # Generate a scatter plot of Cholesterol vs. Maximum Heart Rate
    visualize_heart(data)


if __name__ == "__main__":
    main()
