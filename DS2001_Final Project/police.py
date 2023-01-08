""" Group #1
    Xinghua Peng, Sijia Peng, Yu Ji, Jinghong Chen
    DS 2001
    Group Project
    Nov 27, 2022
    Files: police.py
    Description: Discover the correlation between police salaries and crime 
    rate in the city of Boston. 
    Program Output: Refer to the graph outputs for more information.

"""

# Import packages/libraries as needed
import csv
import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns #Color Palette
from sklearn.linear_model import LinearRegression # Data Prediction Model
from sklearn.model_selection import train_test_split  # Data Slicing
import geopandas as gpd # Mapping
from shapely.geometry import Point
import numpy as np
import wordcloud  # Vocabulary Could Library
from PIL import Image  # Image Processing
from adjustText import adjust_text

# Define constants as needed
N = 3 # Number of years for prediction
START_YEAR = 2011  # Police data starting year
END_YEAR = 2021 # Police data ending year
FILE_NAME = "employee-earnings-report-"
HEADER = "Name,Department Name,Title,Regular,Retro,Other,Overtime,Injured,Detail,Quinn,Total Earnings,Zip".split(",") # Police data title
COLTYPES = [str, str, str, float, float, float, float, float, float, float, float, str] # Data type
ZIP = "ZIP_Codes.geojson" # Map data
CRIME_START_YEAR = 2015 # Crime data starting year
CRIME_END_YEAR = 2022 # Crime data ending year
CRIME_FILE_NAME = "crime-incident-reports-"
CRIME_HEADER = "INCIDENT_NUMBER,OFFENSE_CODE,OFFENSE_CODE_GROUP,OFFENSE_DESCRIPTION,DISTRICT,REPORTING_AREA,SHOOTING,OCCURRED_ON_DATE,YEAR,MONTH,DAY_OF_WEEK,HOUR,UCR_PART,STREET,Lat,Long,Location".split(",") # Crime data title
CRIME_COLTYPES = [str, int, str, str, str, int, str, str, int, int, str, int, str, str, float, float, str] # Data type
IMG_NAME='pic.jpg' # Word cloud map images

def read_data(filename, header, coltypes):
    """ Read the data into a list of dictionaries
    filename - data files for reading purposes
    return - a list of data
    """
    data = []

    with open(filename, "r") as infile:
        # Read the header
        infile.readline()
        lines = csv.reader(infile)

        for vals in lines:
            rowdict = {}

            if len(vals) == len(header):  # Data cleaning
                # store the key-value pairs
                for i in range(len(vals)):
                    key = header[i]
                    value = vals[i]

                    # parse the values
                    value = value.strip()

                    if value != "" and value != "-":  # value is not missing
                        
                        if coltypes[i] == float:  # Remove irrelevant characters and keep the numbers only
                            value = value.replace("$", "").replace("(", "").replace(")", "").replace(",", "")

                        # Process the zip codes
                        if "Zip" == key:
                            value = value.split("-")[0]  # Only keep the first part of the zip data (initial five numbers)
                            if len(value) < 5:  # Add a zero (or zeros) before the numbers if it is less than five digits
                                value = str(value).zfill(5)

                        value = coltypes[i](value)
                    else:
                        if coltypes[i] == float or coltypes[i] == int:  
                            value = 0
                        else:
                            value = ""
                    rowdict[key] = value

                data.append(rowdict)

    return data


def read_all_data(filename, start, end, header, coltypes):
    """Read the data for each year accordingly"""
    data = {}
    for i in range(start, end + 1):
        data[i] = read_data(filename + str(i) + ".csv", header, coltypes)
    return data


def extract_column(data, colidx, coltype = str):
    """ Return data from specific columns in the form of list
    data - all data
    colidx - column
    return - list
    """
    col = []
    for row in data:
        col.append(coltype(row[colidx]))
    return col


def get_zip(data):
    """Get the same zip codes from each year's data"""
    res = []
    for i in range(START_YEAR, END_YEAR + 1):
        zips = extract_column(data[i], "Zip")
        if len(res) == 0:  # Store first year's data into the list if there is no data yet 
            res = zips
        else:  # Get the intersection with the previous results to get the zip codes that is present in all years of data
            res = list(set(res).intersection(set(zips)))
    return res


def bulletgraph(l, aim, title, color):
    """ Build out bullet graphs
        	 l - label, measurement, and lists of the target value
         aim - target value
         title - title of the chart
         color - stacked background colors
         return - a matplotlib figure
    """
    # Stacked bar chart's ranges and labels
    LIMITS = [25000, 75000, 125000, 175000]
    LABLES = ["Low", "Middle", "High", "Top"]

    # Append the data
    data = []
    for i in l:
        data.append((i["zip"], i["mean"], aim))
    
    # Create color values for the palette to use as the color of the stacked bar chart
    palette = sns.light_palette(color, len(LIMITS), reverse=False)

    # Plot the graph
    fig, axarr = plt.subplots(len(data), figsize=(8, 6))  # Create the canvas
    h = LIMITS[-1] / 10  # Set the maximum value of the height of the tool bar

    # Add each bar into the graph
    for idx, item in enumerate(data):

        ax = axarr[idx]  # Get the axis

        # Eliminate unnecessary labels and lines
        ax.set_aspect('equal')
        ax.set_yticklabels([item[0]])
        ax.set_yticks([1])
        ax.spines['bottom'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)

        # Plot the background of the stack graph
        prev_limit = 0
        for i, lim in enumerate(LIMITS):
            ax.barh([1], lim - prev_limit, left=prev_limit, height=h, color=palette[i])  # barh：Build horizontal bar graph
            prev_limit = lim
        # Build horizontal bar graph
        ax.barh([1], item[1], height=(h / 3), color="black")
        # Draw marker lines
        ymin, ymax = ax.get_ylim()  # Need ymin and ymax to locate the target mark
        ax.vlines(item[2], ymin * .9, ymax * .9, linewidth=1.5, color="white")  # Build marked vertical lines

    # Add labels
    rects = ax.patches  # Get every rectangular bar from the bar chart
    for rect, label in zip(rects, LABLES):  # Calculate the location of each text and plot the graph
        ax.text(rect.get_x() + rect.get_width()/2, -rect.get_height() * .4, label, ha='center', va='bottom', color="black")

    ax.set_xlabel("annual_income")
    fig.suptitle(title)
    fig.subplots_adjust(hspace=0)  # Adjust the distance between figure layer and sub-figures to show the entire title
    plt.savefig("Figure_"+title+".png", pad_inches=0, dpi=300)
    plt.show()
    plt.close()


def zip_income_sort(data, zips):
    """Get data from five regions with the highest average income and the lowest ones respectively,
    present the bar chart and return the data"""
    res = []  # [{zip code: , average income: [], average total income:}]
    for zip in zips:  # Get the annual income from each zip code
        annual_income = []  # average annual income
        # Calculate the annual income for each year
        for i in range(START_YEAR, END_YEAR + 1):
            total = 0  # Total annual income
            count = 0  # The number of bars for annual income data
            for row in data[i]:
                if row["Zip"] == zip:
                    total = total + row["Total Earnings"]
                    count = count + 1
            annual_income.append(total / count)
        mean = sum(annual_income) / len(annual_income)
        res.append({
            "zip": zip,
            "annual_income": annual_income,
            "mean": mean,
        })

    # Rank the average annual income
    res.sort(key=lambda x: (x["mean"]))
    # Find the regions with the highest and lowest average annual income respectively
    maximum = res[-5:]
    minimum = res[:5]

    # Plot the bullet graph
    bulletgraph(maximum, color="green", aim=150000,title="Five regions with the highest average gross income")
    bulletgraph(minimum, color="royalblue", aim=40000, title="Five regions with the lowest average gross income")

    return maximum, minimum


def zip_total(data, title):
    """Annual trend graph of zip codes and total income"""
    plt.figure(figsize=(8, 6))  # Size of the graph
    plt.title(title)

    # x-axis: year
    # To keep each value from being omitted, convert all the elements in the list into string
    x = [str(i) for i in range(START_YEAR, END_YEAR + 1)]  

    # Get the annual income from each zip code
    for zip in data:  
        # y-axis: average annual income
        y = zip["annual_income"]  
        # Plot the line chart
        plt.plot(x, y, label=zip["zip"], alpha=0.5)  

    plt.legend() 
    plt.grid()
    plt.xlabel("Year")
    plt.ylabel("Average Gross Income")
    plt.savefig("Figure_"+title+".png", pad_inches=0, dpi=300)
    plt.show()
    plt.close()


def get_color(length):
    """Create a color sequence to show symmetrical gradient colors
    length - number of desired colors
    """
    colors = []  # colors

    # Generate color RGB values
    for i in range(int(length / 2)):
        colors.append([i / int(length / 2), 0.5, 0.5]) 

    # To ensure the colors are symmetrically from the middle, we create the sequence, revert it, and splice it with the original one
    colors = colors + colors[::-1] 

    return colors


def income(data, header, coltypes):
    """Statistics of average annual income"""
    res = {"Year":[]}  # {year: [], average annual income: [], ...}
    # Initialize the data list
    for i in header:
        res[i] = []
    # Process the data
    for year in range(START_YEAR, END_YEAR + 1):
        res["Year"].append(str(year))
        # Calculate the average value for each column
        for i in range(len(header)):  
            key = header[i]
            # Get the data column
            list_data = extract_column(data[year], key, coltypes[i])
            # Calculate the average            
            mean = sum(list_data) / len(data[year])
            res[key].append(mean)  

    x = res["Year"]
    y = res["Total Earnings"]
    plt.figure(figsize=(8, 6)) 
    plt.title("Average annual income statistics")
    # Plot the bar chart
    plt.bar(x, y, color=get_color(len(x)))  
    # Plot the line chart
    plt.plot(x, y, marker="o", markersize=5, color="royalblue")  
    plt.xlabel("Year")
    plt.ylabel("Average Gross Income")
    plt.savefig("Figure_annual_income.png", pad_inches=0, dpi=300)
    plt.show()
    plt.close()

    return res

def annual_forecast(annual):
    """Projection of gross revenue: predict the gross revenue after 3 years based on current data
    	Output/Conclusions: R^2 = 0.8 with a better fitting
    """

    # Create a dataframe
    df = pd.DataFrame(annual)
    # Treat year data as a row index
    df = df.set_index("Year")  

    # Create label columns corresponding to the total revenue after N days
    df["Label"] = df["Total Earnings"].shift(-N)
    # Data cleaning, clear null values: last N rows of data without label values
    data = df.dropna()

    # Constructing test and training datasets
    # Features used for model prediction
    x = data.drop(["Label"], axis=1).values  
    # Prediction
    y = data.Label.values  

    # Seperate data for testing + training 
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=42)

    # Train the data with the linear regression model
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    r2 = lr.score(X_test, y_test)
    #  The higher the value of R^2 or RSquare (the closer to 1), 
    #  the better the fit and the more adequate the explanation of the dependent variable by the independent variable
    print("RSquare =",r2)

    # Plot trend comparison of predicted and actual values
    # Remove parameters that are not relevant to the prediction
    forecast_data = df.drop(["Label"], axis=1)
    # Calculate predicted value
    forecast = lr.predict(forecast_data.values)
    # Actual value
    actual = df["Total Earnings"].values
    # value of x axis: increase N in the backward year
    x = []
    for i in range(START_YEAR + N, END_YEAR + N + 1):
        x.append(str(i))
    # Plot comparison figure
    plt.scatter(x[:-N], actual[N:], marker="s", s=127, color="g", alpha=0.5, label="actual value")
    plt.scatter(x, forecast, marker="s", s=86, color="orange", alpha=0.5, label="forecast value")
    plt.xlabel("Year")
    plt.ylabel("Average Annual Salary of Police Dept.")
    plt.title("Forecast of Average Police Dept. Salary in 2022-2024")
    plt.legend()
    plt.savefig("Figure_forecast.png", pad_inches=0, dpi=300)
    plt.show()
    plt.close()



def crime_map(case_data, filename):
    """read crime data and return crime map in Boston
    """
    # 1.Read the file of Boston map
    data = gpd.read_file(filename, encoding='utf-8')

    # 2. Use polyplot under geoplot to map Boston's administrative divisions
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.dpi = 300
    ax.set_aspect('equal')
    fig.set_facecolor('grey')
    data.plot(ax=ax,
            legend=False,
            linewidth=1,
            facecolor='black',
            edgecolor='white',
            alpha=0.6)

    # 3. Mark out the zip
    data['coords'] = data['geometry'].apply(lambda x: x.representative_point().coords[0])
    for n, i in enumerate(data['coords']):
        plt.text(i[0], i[1], data['ZIP5'][n], fontsize=5, horizontalalignment="center",fontdict={'color':'white'})  # Marking position X, Y, marking content

    # 4. Mark the location of the criminal record
    # Crime record coordinate points
    case_point = [] 
    for i in case_data:
        # Longitude and latitude of statistical criminal records
        for line in case_data[i]:
            # Acquire latitude and longitude data
            x = line["Long"]
            y = line["Lat"]
            # Clear the anomaly, the point must be within the map area
            if x<-70.95 and x>-71.2 and y<42.4 and y>42.2:
                case_point.append(Point((x,y)))

    # Transformation to map data
    pts = gpd.GeoSeries(case_point)
    # Map point labeling
    pts.plot(ax=ax,marker='o', markersize=1, alpha=0.05, label="crime record",cmap='Spectral_r')
    ax.set_title("Boston Crime Incident Map", fontsize=14, color='white')
    # Do not display the axes
    ax.set_axis_off() 
    # Removing the edges
    plt.subplots_adjust(bottom=0, left=0, right=1, hspace=0, wspace=0)
    plt.savefig("Figure_crime_map.png", pad_inches=0, dpi=300)
    plt.show()
    plt.close()


def crime_salary(data, start,end,case_data,case_start,case_end):
    """ 
    data - list of average annual earnings
    start - start year of salary data
    end - end year of wage data
    case_data - all crime data
    case_start - start year of crime data
    case_end - end year of crime data
    """
    
    # Crime data
    case_num = [] 
    # Statistical of Year and Crime Data
    for i in case_data:
        case_num.append(len(case_data[i]))

    # Select the salary data of the same year
    # Assign value to salary, year, and crime rate
    salary = data["Total Earnings"][case_start-start:] #salary
    year = data["Year"][case_start-start:] # year
    case_num = case_num[:-case_end+end] # crime quantity

    # Scatter plot
    plt.scatter(salary, case_num, marker="o", label="Annual data")
    texts = [plt.text(salary[i], case_num[i], year[i]) for i in range(len(salary))]
    adjust_text(texts, arrowprops={'arrowstyle':'fancy','color':'crimson'})

    # Calculate the fitting curve
    # Create the model
    model = LinearRegression()
    # Transforming data into a DataFrame
    x = pd.DataFrame({'salary': salary})
    # Retrieve the value of salary and transform it into a matrix
    x = x['salary'].values.reshape((-1, 1)) 
    # Fit Model: Fit() - One dimensional linear regression model
    # 𝑓(𝑥)=𝑤𝑥+𝑏 / 𝑥 = years / 𝑓(𝑥) = predicted scores
    # The first parameter x - array of shape (number of samples, number of attributes)
    # or a matrix type parameter, representing the input space
    # The second parameter y - array type parameter of shape(number of samples)
    # representing the output space
    model.fit(x, case_num)
    # Plot the fitted curve
    plt.plot(salary, model.predict(x), color='g')
    plt.xlabel("Salary")
    plt.ylabel("Number of Crimes")
    plt.title("Correlation between Salary and Crime Quantity - 2015 to 2021")
    plt.grid()
    plt.legend()
    plt.savefig("Figure_crime_salary.png", pad_inches=0, dpi=300)
    plt.show()
    plt.close()

    # Wage growth rate, number of crimes, year bubble chart - showing the relationship between wage growth rate, number of crimes, and year
    # Calculating the wage growth rate: (Current year - previous year) / previous year
    salary_ratio = [] 
    # Calculation of data from 2015 to 2021
    for i in range(case_start - start, len(data["Total Earnings"])):  
        ratio = (data["Total Earnings"][i] - data["Total Earnings"][i - 1]) / data["Total Earnings"][i - 1]
        salary_ratio.append(ratio)
    # use the scatter function
    # Drawing the basic bubble diagram
    # s parameter Sets the size of the bubble
    s = []  
    for x in salary_ratio:
        s.append(x*x*3600000) # The value of the growth rate is 0. A few decimal places, expanded to 3600000 times the square, the comparison will be more obvious
    # Change color with c and alpha
    # Set c="purple" parameter to change the color of the bubble
    plt.scatter(year, case_num, s=s, c="purple", alpha=0.4)
    plt.title("Bubble chart of Salary Growth Rate & Crime Quantity in Each Year")
    plt.xlabel("Year")
    plt.ylabel("Crime Record")
    # show the graph
    plt.savefig("Figure_crime_salary_year.png", pad_inches=0, dpi=300)
    plt.show()
    plt.close()


def shooting(case_data):
    """Statistics on the frequency of shootings per day of the week
    case_data - All crime data
    """
    res = {} # Counting

    # Statistics DAY_OF_WEEK how many times each shooting
    for i in case_data:
        for line in case_data[i]:
            # Find Gunshot Data
            if line["SHOOTING"] == 'Y': # A value of y indicates a gunshot
                week = line["DAY_OF_WEEK"] # Day of the week
                if week in res:  # If data is already available, add 1 to the current number
                    res[week] = res[week]+1
                else: # If not, add to dictionary and set to 1
                    res[week] = 1
                    
    # Converting statistics into a list                
    week = [] # Week
    values = [] # Number of shooting
    for i in res: 
        week.append(i)
        values.append(res[i])
    
    plt.bar(week, values)
    plt.xticks(rotation=45, ha='right')
    plt.title('Distribution of Shooting Throughout the Week')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Shooting')
    plt.savefig("Shooting.png", pad_inches=0, dpi=300)
    plt.show()
    plt.close

    # Drawing the pie chart
    fig = plt.figure(figsize=[8,6],facecolor=(235/255,235/255,235/255))
    # Create polar coordinates as dials for charts
    ax1=fig.add_subplot(1,1,1,facecolor=(235/255,235/255,235/255), projection='polar')
    # Generate a list of gradient colors
    palette = sns.color_palette('Paired', len(week))
    # Plot the data for each day of the week in turn
    for i in range(len(week)):
        # width = 1 is roughly 60 degrees, so shooting number/60
        ax1.barh(height=1,width=values[i]/60,y=i,color=palette[i],label=week[i])

    # Use set_theta_zero_location() to make the starting point of the circle start from north
    ax1.set_theta_zero_location('N')
    # Use set_theta_direction() to make the ring rotate clockwise
    ax1.set_theta_direction(-1)
    # Use set_rlabel_position() to move radial labels
    ax1.set_rlabel_position(0)
    # Use set_thetagrids() and set_rgrids() to set the scales and tags.
    ax1.set_thetagrids([0, 100, 200, 300], labels=[0, 100, 200, 300])
    # set_rgrids sets the horizontal coordinate scale, i.e. the number of turns for each week
    rgrids = [] 
    for x in range(len(week)):
        rgrids.append(x)
    ax1.set_rgrids(rgrids, labels=week)
   
    plt.title("Pie Chart distribution of Shooting Throughout the Week")
    plt.legend()
    plt.savefig("Figure_shooting.png", pad_inches=0, dpi=300)
    plt.show()
    plt.close() 


def dangerous_streets(data,img):
    """ a word cloud of the most dangerous streets in Boston
    data - crime incident data
    img - background picture
    """
    # 1. Processing data
    street_dic = {} # street word frequency
    # Statistics of street's word frequency
    for i in data:
        # Extract all streets
        street_list = extract_column(data[i],"STREET")

        # Word frequency statistics
        for item in street_list: 
            if item != "": # Skip Null
                item_list = item.replace("\n","&").split("&")  # Data cleaning and generating lists of separated block words

                for j in item_list:
                    word = j.strip()
                    if word in street_dic: # If the word is already in the dictionary, add 1 to the frequency of the word
                        street_dic[word] = street_dic[word] + 1
                    else: # If not, add the word and set the word frequency to 1
                        street_dic[word] = 1

    # 2.Importing background images
    pic = Image.open(img) # Importing images
    backgroud = np.array(pic)  # Formatting images into RBG arrays

    # 3.Plot Word Cloud
    # Create and configure word cloud properties
    cloudword = wordcloud.WordCloud(
                                width=1000, height=700,
                                mask=backgroud,  # Specify the rectangle shape
                                max_words=len(street_dic),  # Max number of words = Total
                                min_font_size=5,  # Specify the min font size
                                max_font_size=100,  # Specify the max font size
                                random_state=90,  # Random Angle
                                background_color='white',  # Background color
                                colormap="Paired" # Text color
                                )
    # Load the result
    cloudword.fit_words(street_dic)
    plt.figure(figsize=(8, 6))
    plt.axis('off') # No coordinates
    plt.tight_layout() # Remove the border
    plt.imshow(cloudword)
    plt.savefig("Figure_wordcloud.png", pad_inches=0, dpi=300)
    plt.show() 
    plt.close() 


def crime_hour(data):
    """Crime by Time Range of Day
    Conclusion: Most of the crime is committed between 6am and 6pm. 
    Most incidents happen between 12pm and 6pm, while the least happens between 12am and 6am
    """
    # Crime time classification - HOUR
    hours = ["00:00-06:00","06:00-12:00","12:00-18:00","18:00-24:00"]
    values = [0,0,0,0] # Numbers

    # Crime time statistics
    for i in data:
        # Extract the time of the crime
        hour_list = extract_column(data[i],"HOUR",int)

        # Category statistics
        for hour in hour_list: 
            if hour >= 0 and hour < 6: # 00-06
                values[0] = values[0] + 1
            if hour >= 6 and hour < 12: # 06-12
                values[1] = values[1] + 1
            if hour >= 12 and hour < 18: # 12-18
                values[2] = values[2] + 1
            if hour >= 18 and hour < 24: # 18-24
                values[3] = values[3] + 1

    # Plot the pie chart
    plt.pie(values,
            labels=hours,
            autopct="%.1f%%", # only show data labels with percentage greater than 1%
            textprops=dict(fontsize=11), # fontsize
            wedgeprops=dict(width=0.3, edgecolor='w'),   # Convert pie chart to a circular chart
            pctdistance=0.55  # Specify the scale / position
            )

    plt.title("Crime by Time Range of Day")
    plt.savefig("Figure_time_pie.png", pad_inches=0, dpi=300)
    plt.show() 
    plt.close()


def offense_group(data):
    """Crime / Offense type statistics"""
    offense_type = {}
    # Offense type
    for i in data:
        # Extract that year's crime type
        offense_type_list = extract_column(data[i],"OFFENSE_CODE_GROUP")

        # Word frequency statistics
        for item in offense_type_list: 
            if item != "": # Skip empty values
                if item in offense_type: # If already exist, word frequency + 1
                    offense_type[item] = offense_type[item] + 1
                else: # If not, add the word frequency to 1
                    offense_type[item] = 1

    # Convert statistics into a list                
    labels = [] # offense type
    values = [] # Number of crimes / offenses
    for i in offense_type: 
        labels.append(i)
        values.append(offense_type[i])

    #2.Plot bar charts
    plt.style.use('fivethirtyeight') # Select the defined style
    fig,ax=plt.subplots()
    ax.barh(labels,values,left=-10)
    plt.title("Analysis of crime types")
    plt.yticks(size = 3) # Label / Font size
    plt.xticks(size = 5) # Label / Font size
    plt.xlabel("number of crime",fontdict=dict(fontsize=5)) 
    plt.savefig("Figure_crime_types.png", bbox_inches='tight',dpi=300)
    plt.show() 
    plt.close()


def main():
    # Read police salary data
    data = read_all_data(FILE_NAME, START_YEAR, END_YEAR, HEADER, COLTYPES)
    # Retrieve the zip code that is available in several years' data
    zips = get_zip(data)
    # Five regions with highest/lowest average gross income
    # Show the bullet chart
    maximum, minimum = zip_income_sort(data, zips)
    # Trends in police salaries for five regions with highest/lowest average income
    zip_total(maximum,"Annual Police Dept. Income Trends in the Five Regions with the Highest Average Income")
    zip_total(minimum,"Annual Police Dept. Income Trends in the Five Regions with the Lowest Average Income")

    # Average Total Revenue Statistics
    annual = income(data, HEADER[3:-1], COLTYPES[3:-1])
    # Salary Prediction
    annual_forecast(annual)

    # Read crime data
    case_data = read_all_data(CRIME_FILE_NAME, CRIME_START_YEAR, CRIME_END_YEAR, CRIME_HEADER, CRIME_COLTYPES)
    # Boston Crime Report Marker Chart - Map
    crime_map(case_data, ZIP)
    # Relationship between crime rate and salary change + bubble chart
    crime_salary(annual, START_YEAR, END_YEAR, case_data, CRIME_START_YEAR, CRIME_END_YEAR)
    # Frequency of shootings per day of the week - Statistics
    shooting(case_data)
    # Word cloud of the most dangerous streets in Boston
    dangerous_streets(case_data,IMG_NAME)
    # Crime type Statistics
    offense_group(case_data)
    # Crime by Time Range of Day
    crime_hour(case_data)


if __name__ == "__main__":
    main()