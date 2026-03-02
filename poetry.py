import os
import fpdf
import random

# pathing variables
filename_1 = "./texts/data_1.txt"
filename_2 = "./texts/data_2.txt"
font = "./fonts/riscada_doodle/RiscadaDoodle-Regular.ttf"

poem_export_path = "./poems"

# parse the text and return a list of the words with escape characters removed
def parse_and_organize_text(raw_text):

    # init our list by separating it via empty white spaces 
    # technically, we can split the text with one line using regexes including white space characters 
    # and \n with re.split(r"[\r\n|\s]") but we'll use string based functions for this case
    words = raw_text.split(" ") 

    # removes newlines here and splits words that may be connected by newlines 
    i = 0
    while i < len(words):

        word = words[i]

        # if a newline is there and it is found in the middle of the string (neither start or end)
        if (
            "\n" in word and 
            word.find("\n") > 0 and 
            word.find("\n") < len(word) - 1
            ):

            # NOTE: escape characters like newlines (\n) aren't recognized by strip or replace and it doesn't account for
            # different platforms (i.e. windows, linux, mac, etc) but .split and .splitlines seems to work
            words_split = word.splitlines()
            words.pop(i)

            for j in range(len(words_split)):
                words.insert(i+j, words_split[j])

            i += (len(words_split) - 1) 
            continue

        # if just a newline (a single word), remove it and reconfigure that index
        elif ("\n" in word):

            word = "".join(word.splitlines())
            words[i] = word    

        i += 1

    return words

# shuffles the texts issued and combines them together
def resynthesize_texts(text_collections):

    """
    Combines multiple colllections of text and returns a unique combination of all of them.

    :param text_collections: Each item of the iterable should be a collection of all the words of one text (e.g. list of all the words of a poem)
    :type text_collections: iterable (list/tuple)
    """
    # shuffle our text
    for collection in text_collections:
        random.shuffle(collection)

    # sort them by descending
    text_collections = sorted(text_collections, key = lambda collection: len(collection), reverse=True)

    output_text = str()
    for i in range(len(text_collections[0])):
        
        for j in range(len(text_collections)):

            # remove the text if we've already used up all its words
            if (i >= len(text_collections[j])):
                text_collections.pop(j)
                break

            # prefix/suffix chars are additional stuff we add to the front and back when appending to our output text
            prefix_chars = str()
            suffix_chars = str()
            # doing this for better readability
            current_word = text_collections[j][i]

            if (is_empty_str(current_word)):
                # return twice
                prefix_chars = "\n\n"
            elif (first_letter_is_capitalized(current_word)):
                # return and add space after word
                prefix_chars += "\n"
                suffix_chars += " "
            elif (contains_ending_puncutation(current_word)):
                # return (since essentially new line)
                suffix_chars += "\n"
            else:
                # just add a space
                suffix_chars += " "

            # check if this is a new line of text or is the beginning of the poem. if so, capitalize the word
            if (
                len(current_word) > 0 and 
                (len(output_text) == 0 or output_text[-1] == "\n")
                ):
                current_word = current_word[0].upper() + current_word[1:len(current_word)]

            # append/prepend all our changes to our output text
            output_text += prefix_chars + current_word + suffix_chars
            
    return output_text

# check if str is empty
def is_empty_str(value):

    return value == ""

# check if the first letter of a word is capitalized 
def first_letter_is_capitalized(value):

    index_of_first_letter = -1

    for i, char in enumerate(value):
        if(
            ord(char) >= 65 and ord(char) <= 90 or
            ord(char) >= 97 and ord(char) <= 122
        ):
            index_of_first_letter = i
            break

    if (index_of_first_letter == -1):
        print(F"Cannot find any letters in {value}. Automatically returning false.")
        return False

    return (ord(value[index_of_first_letter]) >= 65 and ord(value[index_of_first_letter]) <= 90) 

# checks if the word contains any ending punctuation 
def contains_ending_puncutation(value):

    return (
        "." in value or
        "?" in value or 
        "!" in value or 
        "," in value
    )

# extract text from file
def get_text_from_file(filename):
    # check if the file actually exists
    if os.path.exists(filename):
        # if the file exists this is how we open it (read only)
        with open(filename, "r", encoding="utf-8") as file:
            raw_text = file.read() # the info is placed into raw text        
    else:
        # if there is no file, we puse a default poem
        raw_text = """roses are red,\n
        violets are blue,\n
        there is no file,\n
        here is a poem for you"""

    return raw_text

# function for making a pdf
def make_pdf(text, pdf_name):

    pdf = fpdf.FPDF()
    # init our page
    pdf.add_page()
    # add the styling to our document
    pdf.add_font(family="RiscadaDoodle", style="", fname=font)
    pdf.set_font("RiscadaDoodle", size=10)
    pdf.set_char_spacing(0.9)
    # inscribe our text, multi_cell allows for line breaks using \n newlines escape
    pdf.multi_cell(0, None, text=text, markdown=True)
    # export it to path
    pdf.output(poem_export_path + "/" + pdf_name + ".pdf")

# our code to execute
def main():
    # get text from each file path
    raw_text_1 = get_text_from_file(filename_1)
    raw_text_2 = get_text_from_file(filename_2)
    # parse the contents into lists of individual words
    words_1 = parse_and_organize_text(raw_text_1)
    words_2 = parse_and_organize_text(raw_text_2)
    # put them into a list
    text_collections = [words_1, words_2]
    # create a title, which we'll prepend to the reshuffled texts
    title = "--Slam Poetry Jam--"
    document_text = title + "\n\n" + resynthesize_texts(text_collections)
    # convert it to a pdf
    make_pdf(document_text, "Slam Poetry Jam Poem")

# our code execution
if (__name__ == "__main__"):
    main()
