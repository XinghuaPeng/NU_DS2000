""" Xinghua Peng
    DS 2000: Intro to Programming with Data
    Homework 8
    Nov 17, 2022
    File: starwars.py
    Description: Apply our data science skills to explore the story of the 
    Star Wars Movie. 
    
    Program Output: 
    Most positive line:
    character: BIGGS
    dialogue: I feel for you, Luke, you're going to have to learn what seems to 
    be important or what really is important.  What good is all your uncle's 
    work if it's taken over by the Empire?...  You know they're starting to 
    nationalize commerce in the central systems...it won't be long before your 
    uncle is merely a tenant, slaving for the greater glory of the Empire.
    score: 5

    Most negative line:
    character: LEIA
    dialogue: General Kenobi, years ago you served my father in the Clone Wars.  
    Now he begs you to help him in his struggle against the Empire.  I regret 
    that I am unable to present my father's request to you in person, but my 
    ship has fallen under attack and I'm afraid my mission to bring you to 
    Alderaan has failed.  I have placed information vital to the survival of 
    the Rebellion into the memory systems of this R2 unit.  My father will know 
    how to retrieve it.  You must see this droid safely delivered to him on 
    Alderaan.  This is our most desperate hour.  Help me, Obi-Wan Kenobi, 
    you're my only hope.
    score: -6

    +——————————————-+——————————————-+——————————————-+——————————————-+
    |   character   |    minimum    |    average    |    maximum    |
    +——————————————-+——————————————-+——————————————-+——————————————-+
    |  DARTH VADER  |      -2       |   -0.243902   |       1       |
    |     LEIA      |      -6       |   -0.070175   |       1       |
    |     C3PO      |      -3       |   -0.033613   |       5       |
    |     LUKE      |      -2       |   0.161417    |       3       |
    |    OBIWAN     |      -3       |   0.195122    |       3       |
    |   HAN SOLO    |      -5       |   0.248366    |       5       |
    +——————————————-+——————————————-+——————————————-+——————————————-+

"""
# Import package as needed
import matplotlib.pyplot as plt

# Define constant to make it easier if I need to switch filename for testing purposes
STAR_WARS_FILE = "starwars.txt"
NEGATIVE_WORDS_FILE = "negative-words.txt"
POSITIVE_WORDS_FILE = "positive-words.txt"
CHARACTERS = ["DARTH VADER", "LEIA", "C3PO", "LUKE", "OBIWAN", "HAN SOLO"]
PUNC = ["!", '"', "#", "$", "%", "&", "'", "(", ")",
        "*", "+", ",", "-", ".", "/", ":", ";",
        "<", "=", ">", "?", "@", "[", "]", "^", "_",
        "`", "{", "}", "|", "~"]
LUKE = "LUKE"
LEIA = "LEIA"
WINDOW_SIZE = 20
LOW_POINT_LABEL = "Tarkin's Conference"
HIGH_POINT_LABEL = "Attack!!"


def read_data(filename):
    """ Read the data into a list of dictionaries
    filename - datafile that contains the entire script of the movie
    return - a list of dictionaries (line_number, character, dialogue)
    """
    data = []
    coltypes = [int, str, str]

    with open(filename, "r") as infile:

        # Read the header
        header = infile.readline().strip().split("|")

        # read remaining lines
        for line in infile:
            rowdict = {}

            # parse the values
            vals = line.strip().split("|")

            # store the key-value pairs
            for i in range(len(vals)):
                key = header[i]
                value = vals[i]
                if value != "":  # value is not missing
                    value = coltypes[i](value)
                rowdict[key] = value

            data.append(rowdict)

    return data


def read_text(filename):
    """ Read a text file into lists
    filename - text file contains a list of positive or negative words
    return - a lists of positive/negative words
    """
    data = []

    for line in open(filename, "r"):
        # parse the values
        vals = line.strip()
        data.append(vals)

    return data


def count_words(L, words):
    """
    Count the number of times a word in one sentence that appear in the list
    L - list of dictionaries
    words - a list of words
    return - count the number of times
    """
    sum = 0
    for i in words:
        if i in L:
            sum = sum + 1

    return sum


def compute_sentiment_score(data, positive_words, negative_words):
    """ Compute a sentiment score for each line by adding the number of positive
    words and subtracting the number of negative words in that line.
    data - a lists of positive/negative words
    positive_words - words from the positive-words.txt
    negative_words - words from the negative-words.txt
    return - sentiment score
    """
    for line in data:

        # convert the dialogue text to lowercase letters
        dialogue = line["dialogue"].lower()

        # CLEAN each spoken line
        for i in PUNC:
            if i in dialogue:
                dialogue = dialogue.replace(i, "")

        # Compute the number of positive & negative words
        words = dialogue.split(" ")  # Convert a string to a list of words
        positive = count_words(positive_words, words)
        negative = count_words(negative_words, words)

        # Adding # of positive words and subtracting # of negative words
        score = positive - negative
        line["sentiment"] = score

    return data


def the_most_negative_line_and_the_most_positive_line(data):
    """ Report the most negative line and the most positive line in the movie
    data - movie data 
    """
    most_positive_line_number = 0
    most_negative_line_number = 0

    for i in range(1, len(data)):

        score = data[i]['sentiment']

        if score > data[most_positive_line_number]['sentiment']:
            most_positive_line_number = i

        if score < data[most_negative_line_number]['sentiment']:
            most_negative_line_number = i
    
    # Print and generate the most negative line and most positive line
    print("Most positive line:")
    print("character:", data[most_positive_line_number]['character'])
    print("dialogue:", data[most_positive_line_number]['dialogue'])
    print("score:", data[most_positive_line_number]['sentiment'])
    print("")
    print("Most negative line:")
    print("character:", data[most_negative_line_number]['character'])
    print("dialogue:", data[most_negative_line_number]['dialogue'])
    print("score:", data[most_negative_line_number]['sentiment'])
    print("")
    
    
def get_sentiment(data, character_name=""):
    """
    Retrieve list of sentiment scores according to the character name
    data - sentiment socre
    character_name -  character name in the movie
    return - a list of data
    """
    sentiment = []  # list of data
    for line in data:
        if line["character"] == character_name or character_name == "":
            sentiment.append(line["sentiment"])

    return sentiment


def generate_table(data, characters):
    """ Generate a table that displays the minimum,average,and maximum sentiment score
    data - sentiment score
    characters - the specified characters according to the prompt
    """
    # Include a table header
    print("+{:—>15s}+{:—>15s}+{:—>15s}+{:—>15s}+".format("-","-","-","-"))
    print("|{:^15s}|{:^15s}|{:^15s}|{:^15s}|".format("character", "minimum", "average", "maximum"))
    print("+{:—>15s}+{:—>15s}+{:—>15s}+{:—>15s}+".format("-","-","-","-"))

    # Character statistics
    for character in characters:
        # Retrieve the list of sentiment scores
        sentiment = get_sentiment(data, character)
        # Compute the minimum,average,and maximum sentiment score for list
        minimum = min(sentiment)
        average = avg(sentiment)
        maximum = max(sentiment)
        # display sentiment score of the character
        print("|{:^15s}|{:^15d}|{:^15f}|{:^15d}|".format(character, minimum, average, maximum))

    # the end of table
    print("+{:—>15s}+{:—>15s}+{:—>15s}+{:—>15s}+".format("-","-","-","-"))


def luke_leia(data):
    """ Create overlapping histograms of the sentiment scores for LUKE and LEIA
    data - sentiment scores
    """
    # Retrieve the data
    LUKE_data = get_sentiment(data, LUKE)
    LEIA_data = get_sentiment(data, LEIA)

    # Create overlapping histograms
    plt.hist(LUKE_data, bins=10, color='blue', alpha=0.5)
    plt.hist(LEIA_data, bins=10, color='red', alpha=0.5)

    # Label the axes and title
    plt.xlabel("sentiment scores")
    plt.ylabel("total")
    plt.title("The sentiment scores for LUKE (blue bars)and LEIA(red bars)")
    
    plt.xlim(-6, 6)
    plt.savefig("luke_leia.pdf")
    plt.show()


def avg(L):
    """ Compute the numerical average of a list of numbers.
    If list is empty, return 0.0
    L - List of values
    """

    if len(L) > 0:
        return sum(L) / len(L)
    else:
        return 0.0
    

def get_window(L, idx, window_size=1):
    """ Extract a window of values of specified size
    centered on the specified index
    L - List of values
    idx - Center index
    window_size - window size
    """
    minrange = max(idx - window_size // 2, 0)
    maxrange = idx + window_size // 2 + (window_size % 2)

    return L[minrange:maxrange]


def moving_average(L, window_size=1):
    """ Compute a moving average over the list L
    using the specified window size
    L - List of values
    window size - The windowsize(default=1)
    return - Anew list with smoothed values
    """
    mavg = []
    for i in range(len(L)):
        window = get_window(L, i, window_size)
        mavg.append(avg(window))

    return mavg


def story_arc(data):
    """ Visualize the story arc of the Star Wars Movie using sentiment scores
    Plot a moving average sentiment score using a window size of 20
    data - sentiment scores
    """
    # Retrieve the data
    sentiments = get_sentiment(data)

    # Moving average sentiment score
    average = moving_average(sentiments, WINDOW_SIZE)

    # Create overlapping histograms
    plt.plot(average)

    # Find the index of the low point：“Tarkin’s Conference”
    x_coordinate = average.index(min(average))
    window = get_window(sentiments, x_coordinate, WINDOW_SIZE)
    y_coordinate = avg(window)
    # Label at this point with the text
    plt.text(x_coordinate, y_coordinate, LOW_POINT_LABEL)

    # Find the index of the high point
    x_coordinate = average.index(max(average))
    window = get_window(sentiments, x_coordinate, WINDOW_SIZE)
    y_coordinate = avg(window)
    # Label at this point with the text: "Attack!!"
    plt.text(x_coordinate, y_coordinate, HIGH_POINT_LABEL)
    plt.savefig("story_arc.pdf")
    plt.show()


def character_scores(data):
    """ Count the number of positive and negative lines spoken by each character
    (lines with sentiment score of 0 should be ignored)
    data - sentiment scores
    """
    # square plot with high resolution for clarity
    plt.figure(figsize=(6, 6), dpi=200)
    # Overlay a grid
    plt.grid()
    
    # Label the axes and have a descriptive title
    plt.xlabel("negative line")
    plt.ylabel("positive line")
    plt.title("The number of positive and negative lines spoken by each character")
    
    # draw a diagonal line from (0.0) to (70.70) in green
    plt.plot([0, 70], [0, 70], color='g')     
    
    # Both the x and y axis should range from 0 to 70
    plt.xlim([0, 70])
    plt.ylim([0, 70])
    
    # characters = {'character1':[negative lines, positive lines],
    #               'character2':[negative lines, positive lines]
    #               ...}
    characters = {}

    for line in data:

        character = line['character']  # character name
        sentiment = line['sentiment']  # sentiment score
        sentiment_idx = -1  # index of sentiment lines（0 ：negative lines，1：positive lines）

        # lines with sentiment score of 0 should be ignored
        if sentiment != 0:

            if sentiment > 0:
                sentiment_idx = 0
            if sentiment < 0:
                sentiment_idx = 1

            if character in characters:
                characters[character][sentiment_idx] = characters[character][sentiment_idx] + 1
            else:
                characters[character] = [0, 0]
                characters[character][sentiment_idx] = 1

    # Plot
    for character in characters:
        negative_lines = characters[character][0]
        positive_lines = characters[character][1]

        # Only plot characters where negative lines+positive lines>10
        if negative_lines + positive_lines > 10:
            # a scatter plot:(negative lines, positive lines)
            plt.scatter(negative_lines, positive_lines, label=character)

    # Show a legend to identify each character
    plt.legend()
    plt.savefig("character_scores.pdf")
    plt.show()



def main():
    # Read the data
    data = read_data(STAR_WARS_FILE)
    # Separately read the lists of positive words and negative words into lists
    positive_words = read_text(POSITIVE_WORDS_FILE)
    negative_words = read_text(NEGATIVE_WORDS_FILE)
    
    # Analysis
    # 1. Compute a sentiment score for each line
    data = compute_sentiment_score(data, positive_words, negative_words)
    # 2. Report the most negative line and the most positive line in the movie
    the_most_negative_line_and_the_most_positive_line(data)
    # 3. Generate a table that displays the min, avg, and max sentiment score 
    # for lines spoken by 'DARTH VADER', 'LEIA', 'C3PO', 'LUKE', 'OBIWAN', 'HAN SOLO'.
    generate_table(data, CHARACTERS)

    # Visualization
    # 1. Create overlapping histograms of the sentiment scores for LUKE/LEIA
    luke_leia(data)
    # 2. Visualize the story arc of the Star Wars Movie using sentiment scores
    story_arc(data)
    # 3. Count the number of positive and negative lines spoken by each character
    character_scores(data)


if __name__ == "__main__":
    main()
