#!/usr/bin/python3.8

import sys, getopt, fileinput, os.path

# Setting global variables.
###########################
# The current version of the program.
version = "1.0"
# Importing command line arguments into a list.
options = sys.argv[1:]
# This variable specifies what file to read from.
input_file = ""
# This variable specifies what delimiter to use when parsing text file records.
delimiter = " "
# This variable stores the provided options/arguments after being checked.
arguments = []
# This variable stores the field specified from the command line that will be
# extracted from a text file record.
field = ""
# This variable is where the extracted field will be stored.
extracted_field = ""
# This variable defines how the program will read data. 0 for STDIN, 1 for file based input.
read_mode = "0"
# This variable contains the raw text line records which will be processed.
input_lines = ""
###########################

# This function performs input validation on provided arguments to the program.
# If input validation succeeds the program will return a list of options and their
# provided arguments.
def OPTION_CHECK(option_list):
    try:
        opts, args = getopt.getopt(option_list, 'hd:f:F:')
    except getopt.GetoptError as error:
        print(error)
        sys.exit(2)
    return opts

# This function will print a useful page about the usage of this command. Otherwise
# know as a 'help page' containing a list of available options. It will also provide
# the current version of the program.
def USAGE():
    print("Version:",version)
    print("")
    print("Description:")
    print("This program will parse through an input (whether that input be from a file or STDIN)")
    print("using the provided delimiter. It will extract fields specified and write them to STDOUT.")
    print("")
    print("Options:")
    print("-F, Designates input file.")
    print("-d, Designates what delimiter to use. By default a space ( ) is used.")
    print("-h, Presents this page.")
    print("-f, What field to extract.")
    sys.exit(1)

# This function parses the arguments provided to it and performs certain actions based
# on them. If no options are provided it will error out and close the program. It will call 
# the USAGE function if '-h' is provided. It will set variables with the other provided options.
# -F input file
# -f field
# -d delimiter
# -h help
def ARGUMENT_PARSE(argument_list):
    global input_file
    global delimiter
    global field
    if not argument_list:
        print("No options provided!")
        sys.exit(2)
    for o, a in argument_list:
        if o == "-h":
            USAGE()
        elif o == "-F":
            input_file = a
        elif o == "-d":
            delimiter = a
        elif o == "-f":
            field = a
        else:
            print("Unhandled option/argument.")
            sys.exit(2)

# Function for taking text line records and converting them to a list where
# each character (including spaces and special characters) is an individual
# entry in the list. Text line records are passed onto this function in variable
# 'raw_input'. and returned as converted to a list.
def RECORD_SPLIT(raw_input):
    parsed_output = []
    parsed_output = list(raw_input)
    return parsed_output

# Function for obtaining fields from a text line record that has been converted 
# to a list of invidual characters. A list of characters must be passed to this 
# function in argument 'list_input'. The location of delimiter one (del1) and 
# delimiter two (del2) must also be passed. Note that if the value you want is 
# at the beginning of the text line record (I.E. isn't preceded by a delimiter) 
# then you need to pass a '0' as 'del1'. If the value desired is at the end of 
# the record (I.E. isn't proceeded by a delmiter then you need to pass a '0' for 
# 'del2'. This function will extract the index values either between two delimiters
# or up to or from a specified delimiter.
def EXTRACTOR(list_input,del1,del2):
    list_output = []
    parsed_output = ""
    if (del1 != 0):
        del1 = del1 + 1
    if (del2 == 0):
        del2 = len(list_input)
    for x in range(del1,del2):
        list_output.append(list_input[x])
    parsed_output = ''.join(list_output)
    return parsed_output

# This function will search through a list of characters for the specified
# delimiter. It will return a list of the index entries locating each delimiter
# within the list. A list must be passed to this function as well as a delimiter.
# Note that it's best that the passed delimiter value be encased within single
# quotations.
def LOCATOR(list_input,delimiter):
    list_output = []
    list_entries = (len(list_input) - 1)
    for x in range(0,list_entries):
        if (delimiter == list_input[x]):
            list_output.append(x)
    return list_output

# This function will find the index numbers of delimiters surrounding a specified
# field number. Essentially, this function provides the boundary delimiters of a
# specified field. If the field is either the first or last field then this function
# provides the closest delimiter (either before or after the field).
def FINDER(field,delimiter_locations):
    # This variable is the first delimiter in the list behind the specified field.
    del1 = "0"
    # This variable is the second delimiter in the list ahead of the specified field.
    del2 = "0"
    # This variable will determine what the length of the list is.
    delimiter_amount = (len(delimiter_locations))
    # This variable is the amount of fields in the original list.
    field_amount = delimiter_amount + 1
    if field > field_amount:
        print("The field number provided is greater than the amount of fields available!")
        sys.exit(2)
    if (field == 1):
        del1 = 0
        del2 = delimiter_locations[0]
    elif (field == field_amount):
        del1 = delimiter_locations[(delimiter_amount - 1)]
        del2 = 0
    else:
        del1 = (delimiter_locations[field - 2])
        del2 = (delimiter_locations[field - 1])
    return del1,del2

# This function performs some pre-flight checks. It will make sure that the input file
# exists and can be read. It will also check to see if the provided field is numerical in value.
def CHECKS(input_file, field):
    if input_file == "":
        pass
    elif os.path.exists(input_file) == False:
        print("The input file specified either doesn't exist or you don't have appropriate permissions to read the file.")
        sys.exit(2)
    if field == "":
        print("No field selected. Use the -f option and enter a field number to extract.")
        sys.exit(2)
    elif field.isnumeric() == False:
        print("The argument provided with the field (-f) option must be numeric! You provided:",field)
        sys.exit(2)
    elif field == "0":
        print("The argument provided with the field (-f) option must be greater than one! You provided:",field)
        sys.exit(2)

# This function will open a file and import its contents to a variable. 
# This variable will then be returned. You must pass the filename or
# filepath to this function.
def FILE_OPENER(filename):
    file_contents = ""
    file_contents = open(filename, "r")
    file_contents.close
    return file_contents

# This function will read each line from STDIN and store them to a single
# variable. It will then return that variable.
def STDIN_READ():
    lines = ""
    for line in sys.stdin:
        lines += line
    return lines

# Main function.
def main():
    # Setting variables.
    global arguments
    global read_mode
    global input_lines
    global field
    global extracted_field
    line = "0"
    delimiter_index = "0"
    del1 = "0"
    del2 = "0"
    # Parsing CLI input.
    arguments = (OPTION_CHECK(options))
    ARGUMENT_PARSE(arguments)
    # Performing input validation.
    CHECKS(input_file,field)
    field = int(field)
    # Determining read mode.
    if not input_file:
        read_mode = "0"
    else:
        read_mode = "1"
    if read_mode == "1":
        input_lines = (FILE_OPENER(input_file))
        input_lines = input_lines.read()
    elif read_mode == "0":
        input_lines = STDIN_READ()
    else:
        print("Exception when determining read mode!")
        sys.exit(2)
    # Splitting input lines into a list based on newline characters.
    input_lines = input_lines.split('\n')
    # Iterating over each line.
    input_index_entries = (len(input_lines) - 1)
    for x in range(0,input_index_entries):
        line = (RECORD_SPLIT(input_lines[x]))
        delimiter_index = (LOCATOR(line,delimiter))
        del1, del2 = (FINDER(field,delimiter_index))
        extracted_field = (EXTRACTOR(line,del1,del2))
        print(extracted_field)

if __name__ == "__main__":
    main()
