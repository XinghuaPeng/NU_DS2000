""" Xinghua Peng
    DS 2000: Intro to Programming with Data
    Homework 5
    Oct 16, 2022
    File: exoplanet.py
    Description: This program analyze exoplanet data, identify the most
    Earth-like exoplanet, and visualize the catalog of all discovered 
    exoplanets and their properties to see how most newly discovered 
    exoplanets are different from Earth. 
    
    *Program text output: 
        Most Earth-like exoplanet: TRAPPIST-1 d
        Euclidean distance from TRAPPIST-1 d to Earth: 1.5755117881439684

        The matching exoplanet's six attributes as follows:  
        - Name: TRAPPIST-1 d 
        - Masses: 0.29690926 
        - Radius: 0.7672418000000001 
        - Orbital Period: 0.011088039662448644 
        - Semimajor Axis: 0.02228038 
        - Surface Temperature: 288.0
"""

# Import package as needed
import matplotlib.pyplot as plt

# Define a collection of functions
# Code in a modular style
def read_data(filename):
    """ Read exoplanet dataset into a list of lists
    filename - name of the datafile - * exoplanet.file in this case
    return - a table as lists of lists containing six planet attributes:
    name / mass/ radius / orbital period / semimajoraxis / surface temperature
    * each sublist is the data for one planet
    """
    # Store exoplanet data
    data = []

    with open(filename, "r") as infile:
        for line in infile.readlines():

            # Ignore any line that begins with a hashtag #
            if "#" in line:
                pass
            else:
                # Extract values
                vals = line.strip().split(",")

                # a. name (string)
                name = str(vals[0])

                # b. mass (float)
                jupiter_masses = vals[2]
                # looking for empty strings and stored as 0.0
                if jupiter_masses == "":
                    jupiter_masses = 0.0
                else:
                    # Convert data type
                    jupiter_masses = float(jupiter_masses)
                # Convert the mass from Jupiter to Earth
                # One Jupiter mass = 317.89 Earth masses
                masses = jupiter_masses * 317.89

                # c. radius (float)
                jupiter_radii = vals[3]  # float
                # looking for empty strings and stored as 0.0
                if jupiter_radii == "":  
                    jupiter_radii = 0.0
                else:
                    # Convert data type
                    jupiter_radii = float(jupiter_radii)
                # Convert the planet radius from Jupiter radii to Earth radii
                # One Jupiter radius = 10.97 Earth radius
                radius = jupiter_radii * 10.97

                # d. orbital period (float)
                period = vals[4]
                # looking for empty strings and stored as 0.0
                if period == "":
                    period = 0.0
                else:
                    # Convert data type
                    period = float(period)
                # Convert measurement in days to year
                # 1 year = 365.2422 days
                orbital_period = period / 365.2422

                # e. semimajoraxis (float)
                semimajoraxis = vals[5]
                # looking for empty strings and stored as 0.0
                if semimajoraxis == "":
                    semimajoraxis = 0.0
                else:
                    # Convert data type
                    semimajoraxis = float(semimajoraxis)

                # f. Surface temperature (K) (float)
                surface_temperature = vals[11]
                # looking for empty strings and stored as 0.0
                if surface_temperature == "":
                    surface_temperature = 0.0
                else:
                    # Convert data type
                    surface_temperature = float(surface_temperature) 

                # Store data into lists of lists
                plant = [name, masses, radius, orbital_period, semimajoraxis, 
                         surface_temperature]
                data.append(plant)

    return data

def lookup_planet(name, data):
    """ Fetch the planet attributes (sublists) from the data table
    name - the name of the planet that we are looking up
    data - full planetary dataset - lists of lists containing six planet attributes
    return - a list of the six planet attributes for the named planet
    """
    attrs = []
    for i in data:
        if i[0] == name:
            attrs = i

    return attrs
    
def euclidean_distance(L1, L2):
    """ Calculate Euclidean distance / how different two planets are
    L1, L2 - lists represent each attributes
    L1 / L2 - data for planet 1 / planet 2 in the form of lists
    return - the Euclidean distance score between planet 1 and planet 2
    """
    # Calculate Euclidean distance score
    # euclid =((Mass)² + (Radius)² + (Period)² + (SemimajorAxis)² + (SurfaceTemp)²)1/2
    euclid = ((L1[1] - L2[1]) ** 2 + (L1[2] - L2[2]) ** 2 + (L1[3] - L2[3]) ** 2 
              + (L1[4] - L2[4]) ** 2 + (L1[5] - L2[5]) ** 2) ** 0.5

    return euclid
    
def find_most_similar_planet(name, data):
    """ Find the planet that is most similar to the specified planet
    name - the name of a planet we're trying to match
    data - full planetary dataset - lists of lists containing six planet attributes
    return - the name of the matching planet
    """
    similar_planet = ""
    min = 0
    flag = True

    # Read the planet's attributes
    planet_input = lookup_planet(name, data)
    # Compute and compare the Euclidean distance
    for i in data:
        if i[0] != name:
            # Calculate the Euclidean distance
            score = euclidean_distance(L1=planet_input, L2=i)
            if flag:
                min = score
                similar_planet = i[0]
                flag = False
            else:
                if score < min:
                    min = score
                    similar_planet = i[0]
    return similar_planet

def generate_planet_report(name, data):
    """ Summarize a planet with a printed report
    name - the name of a particular planet
    data - full planetary dataset - lists of lists containing six planet attributes
    return - planet's attributes report
    """
    
    for i in data:
        if i[0] == name:
            print("The matching exoplanet's six attributes as follows: ", 
                  "\n- Name:", i[0], "\n- Masses:", i[1], "\n- Radius:", i[2], 
                  "\n- Orbital Period:", i[3], "\n- Semimajor Axis:", i[4], 
                  "\n- Surface Temperature:", i[5])

def extract_column(data, colidx):
    """ Extract one specific column as a list from the lists of lists
    data - full planetary dataset - lists of lists containing six planet attributes
    colidx - the index of the column to be extracted
    return - a list of every value in that specific column
    """
    col = []
    for row in data:
        col.append(row[colidx])
    return col
    
def visualize_exoplanets(data):
    """ Plot Semimajor Axis (y-axis) vs. Exoplanet Mass for all planets 
    data - full planetary dataset - lists of lists containing six planet attributes
    *Semimajor Axis - List of Semimajor Axis / Mass - List of Mass
    return - a scatter plot of all discovered exoplanets and their properties
    """
    
    # Record exoplanet Semimajor Axis on y-axis & exoplanet mass on x-axis
    y = extract_column(data, 4)
    x = extract_column(data, 1)

    # Create a canvas & scatter plot
    plt.scatter(x, y, marker = ".")

    # Label x / y axis and add the title
    plt.xlabel("Planetary Mass (in Earth masses)")
    plt.ylabel("Semimajor Axis (in AUs )")
    plt.title("Planetary Mass vs. Semimajor Axis for exoplanets")
    
    # Put the x / y axis on a logarithmic scale
    plt.xscale("log")
    plt.yscale("log")

    # Mark Earth with a red "X"
    earth = lookup_planet("Earth", data)
    plt.scatter(earth[1], earth[4], color="red", marker="x", label="Earth")
    plt.legend()
    
    # Add a text label "Earth" near the "X"
    plt.text(earth[1], earth[4], "Earth", ha="left", wrap=True)
    plt.savefig("exoplanet.png")
    plt.show()
    

def main():
    
    # Read the exoplanet data
    data = read_data("exoplanets.csv")
   
    # Determine and print out which exopanet is most similar to Earth
    similar_planet = find_most_similar_planet("Earth", data)
    print("Most Earth-like exoplanet:", similar_planet)
    
    # Print out the Edclidean distance
    print("Euclidean distance from", similar_planet, "to Earth:", 
          euclidean_distance(lookup_planet("Earth", data),
                             lookup_planet(similar_planet, data)))
    print("")
    
    # Print out this matching planet's six attributes
    generate_planet_report(similar_planet,data)
    
    # Visualize the data
    visualize_exoplanets(data)
    

if __name__ == "__main__":
    main()