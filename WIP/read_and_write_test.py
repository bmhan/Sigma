##############################################################################
# Name: read_and_write_test.py
# Author: Brian Han
# Date Created: 7/13/17
#
# Exploring read and write python functionality
##############################################################################

"""
Syntax for opening a file:
Modes are "r, w, a (appending), r+ (read and write)"
"""

# Opening a new file, writing to it, then closing
file = open ("test.txt", "w")
file.write("Hello World")
file.write("\nNewline character for a newline")
file.close()

#Now reading the file we just made
file_read = open ("test.txt", "r")
print file_read.read(11)
print file_read.readlines()

#Looks like when you read, you move forward just like in C++