# ============================================================================
# FILE HANDLING IN PYTHON
# ============================================================================

"""
File handling allows you to read from and write to files.
Python provides built-in functions and methods for file operations.
Always close files after use, or use 'with' statement for automatic closing.
"""

# ============================================================================
# 1. OPENING A FILE
# ============================================================================

"""
Files are opened using the open() function.
Different modes determine how the file is accessed.
"""

# Opening a file in different modes
# file = open("filename.txt", "r")  # read mode
# file = open("filename.txt", "w")  # write mode
# file = open("filename.txt", "a")  # append mode
# file = open("filename.txt", "x")  # exclusive creation
# file = open("filename.txt", "b")  # binary mode
# file = open("filename.txt", "t")  # text mode (default)
# file = open("filename.txt", "+")  # read and write

# File modes explained:
# "r" - Read (default) - Opens file for reading, raises error if file doesn't exist
# "w" - Write - Opens file for writing, creates file if doesn't exist, overwrites if exists
# "a" - Append - Opens file for appending, creates file if doesn't exist
# "x" - Exclusive creation - Creates file, raises error if file exists
# "b" - Binary mode - Opens file in binary mode
# "t" - Text mode (default) - Opens file in text mode
# "+" - Read and write - Opens file for both reading and writing

# Combining modes
# "r+" - Read and write (file must exist)
# "w+" - Write and read (creates/overwrites file)
# "a+" - Append and read (creates file if doesn't exist)


# ============================================================================
# 2. READING FROM FILE
# ============================================================================

"""
Several methods are available for reading file contents.
"""

# Example: Reading entire file
# Note: In real usage, you would have an actual file
# For demonstration, we'll show the methods

# Method 1: read() - reads entire file
# file = open("example.txt", "r")
# content = file.read()  # reads entire file as string
# file.close()

# Method 2: readline() - reads one line
# file = open("example.txt", "r")
# line = file.readline()  # reads one line
# file.close()

# Method 3: readlines() - reads all lines as list
# file = open("example.txt", "r")
# lines = file.readlines()  # reads all lines as list
# file.close()

# Example: Reading line by line
# file = open("example.txt", "r")
# for line in file:
#     print(line.strip())  # strip() removes newline
# file.close()


# ============================================================================
# 3. WRITING TO FILE
# ============================================================================

"""
Files can be written to using write() or writelines() methods.
"""

# Writing to file
# file = open("output.txt", "w")
# file.write("Hello, World!")
# file.close()

# Writing multiple lines
# file = open("output.txt", "w")
# file.writelines(["Line 1\n", "Line 2\n", "Line 3\n"])
# file.close()

# Note: write() doesn't add newline automatically
# file.write("Line 1\n")  # Need to add \n manually


# ============================================================================
# 4. CLOSING A FILE
# ============================================================================

"""
Always close files after use to free system resources.
"""

# Manual closing
# file = open("example.txt", "r")
# content = file.read()
# file.close()  # Always close the file

# Important: Always close files to avoid resource leaks


# ============================================================================
# 5. USING WITH STATEMENT (RECOMMENDED)
# ============================================================================

"""
The 'with' statement automatically closes the file.
This is the recommended way to handle files.
"""

# Using with statement (recommended - automatically closes file)
# with open("filename.txt", "r") as file:
#     content = file.read()
#     # file automatically closed here

# Example: Reading with 'with'
# with open("example.txt", "r") as file:
#     content = file.read()
#     print(content)

# Example: Writing with 'with'
# with open("output.txt", "w") as file:
#     file.write("Hello, World!\n")
#     file.write("This is a test.\n")

# Multiple files
# with open("input.txt", "r") as infile, open("output.txt", "w") as outfile:
#     content = infile.read()
#     outfile.write(content.upper())


# ============================================================================
# 6. FILE MODES DETAILED
# ============================================================================

"""
Understanding file modes is crucial for proper file handling.
"""

# "r" - Read (default)
# - Opens file for reading
# - File pointer at beginning
# - Raises FileNotFoundError if file doesn't exist
# Example:
# with open("readme.txt", "r") as file:
#     content = file.read()

# "w" - Write
# - Opens file for writing
# - Creates file if doesn't exist
# - Overwrites existing file
# - File pointer at beginning
# Example:
# with open("output.txt", "w") as file:
#     file.write("New content")

# "a" - Append
# - Opens file for appending
# - Creates file if doesn't exist
# - File pointer at end
# - Doesn't overwrite existing content
# Example:
# with open("log.txt", "a") as file:
#     file.write("New log entry\n")

# "x" - Exclusive creation
# - Creates file, fails if file exists
# - Useful for ensuring file doesn't already exist
# Example:
# try:
#     with open("newfile.txt", "x") as file:
#         file.write("New file")
# except FileExistsError:
#     print("File already exists")

# "b" - Binary mode
# - Opens file in binary mode
# - Used for images, videos, executables, etc.
# Example:
# with open("image.jpg", "rb") as file:
#     data = file.read()

# "t" - Text mode (default)
# - Opens file in text mode
# - Handles line endings automatically
# Example:
# with open("text.txt", "rt") as file:  # 't' is default
#     content = file.read()

# "+" - Read and write
# - Opens file for both reading and writing
# - "r+": file must exist, pointer at beginning
# - "w+": creates/overwrites, pointer at beginning
# - "a+": creates if needed, pointer at end
# Example:
# with open("data.txt", "r+") as file:
#     content = file.read()
#     file.write("Additional content")


# ============================================================================
# 7. FILE METHODS
# ============================================================================

"""
Files have various methods for different operations.
"""

# .read() - reads entire file
# with open("example.txt", "r") as file:
#     content = file.read()  # Returns entire file as string

# .readline() - reads one line
# with open("example.txt", "r") as file:
#     line1 = file.readline()  # First line
#     line2 = file.readline()  # Second line

# .readlines() - reads all lines as list
# with open("example.txt", "r") as file:
#     lines = file.readlines()  # Returns list of lines

# .write() - writes string to file
# with open("output.txt", "w") as file:
#     file.write("text")  # Writes string

# .writelines() - writes list of strings to file
# with open("output.txt", "w") as file:
#     file.writelines(["line1\n", "line2\n"])  # Writes list

# .seek() - changes file position
# with open("example.txt", "r") as file:
#     file.seek(0)  # Move to beginning
#     file.seek(10)  # Move to position 10
#     file.seek(0, 2)  # Move to end (2 = end)

# .tell() - returns current file position
# with open("example.txt", "r") as file:
#     position = file.tell()  # Returns current position
#     content = file.read()
#     new_position = file.tell()  # New position after read

# .close() - closes file
# file = open("example.txt", "r")
# file.close()  # Closes file manually

# .flush() - flushes internal buffer
# with open("output.txt", "w") as file:
#     file.write("Data")
#     file.flush()  # Forces write to disk immediately


# ============================================================================
# 8. PRACTICAL EXAMPLES
# ============================================================================

# Example 1: Reading and displaying file content
def read_file(filename):
    """Read and display file content"""
    try:
        with open(filename, "r") as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print(f"File '{filename}' not found")
    except Exception as e:
        print(f"Error: {e}")

# Example 2: Writing to file
def write_to_file(filename, content):
    """Write content to file"""
    try:
        with open(filename, "w") as file:
            file.write(content)
        print(f"Content written to {filename}")
    except Exception as e:
        print(f"Error writing file: {e}")

# Example 3: Appending to file
def append_to_file(filename, content):
    """Append content to file"""
    try:
        with open(filename, "a") as file:
            file.write(content + "\n")
        print(f"Content appended to {filename}")
    except Exception as e:
        print(f"Error appending to file: {e}")

# Example 4: Copying file
def copy_file(source, destination):
    """Copy content from source to destination"""
    try:
        with open(source, "r") as src, open(destination, "w") as dst:
            content = src.read()
            dst.write(content)
        print(f"File copied from {source} to {destination}")
    except FileNotFoundError:
        print(f"Source file '{source}' not found")
    except Exception as e:
        print(f"Error copying file: {e}")

# Example 5: Reading line by line
def process_file_lines(filename):
    """Process file line by line"""
    try:
        with open(filename, "r") as file:
            for line_num, line in enumerate(file, start=1):
                print(f"Line {line_num}: {line.strip()}")
    except FileNotFoundError:
        print(f"File '{filename}' not found")

# Example 6: Counting lines, words, characters
def file_stats(filename):
    """Count lines, words, and characters in file"""
    try:
        with open(filename, "r") as file:
            content = file.read()
            lines = content.count("\n") + (1 if content else 0)
            words = len(content.split())
            characters = len(content)
            
            print(f"File: {filename}")
            print(f"  Lines: {lines}")
            print(f"  Words: {words}")
            print(f"  Characters: {characters}")
    except FileNotFoundError:
        print(f"File '{filename}' not found")

# Example 7: Searching in file
def search_in_file(filename, search_term):
    """Search for term in file"""
    try:
        with open(filename, "r") as file:
            for line_num, line in enumerate(file, start=1):
                if search_term.lower() in line.lower():
                    print(f"Line {line_num}: {line.strip()}")
    except FileNotFoundError:
        print(f"File '{filename}' not found")

# Example 8: Reading CSV-like data
def read_csv_like(filename):
    """Read CSV-like file and process data"""
    try:
        with open(filename, "r") as file:
            for line in file:
                # Split by comma and process
                parts = line.strip().split(",")
                print(f"Data: {parts}")
    except FileNotFoundError:
        print(f"File '{filename}' not found")

# Example 9: Writing formatted data
def write_formatted_data(filename, data):
    """Write formatted data to file"""
    try:
        with open(filename, "w") as file:
            for item in data:
                file.write(f"{item}\n")
        print(f"Formatted data written to {filename}")
    except Exception as e:
        print(f"Error: {e}")

# Example 10: Binary file handling
def copy_binary_file(source, destination):
    """Copy binary file"""
    try:
        with open(source, "rb") as src, open(destination, "wb") as dst:
            data = src.read()
            dst.write(data)
        print(f"Binary file copied from {source} to {destination}")
    except FileNotFoundError:
        print(f"Source file '{source}' not found")
    except Exception as e:
        print(f"Error: {e}")

# Example 11: File existence check
import os

def check_and_read_file(filename):
    """Check if file exists before reading"""
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return file.read()
    else:
        return f"File '{filename}' does not exist"

# Example 12: Reading with encoding
def read_with_encoding(filename, encoding="utf-8"):
    """Read file with specific encoding"""
    try:
        with open(filename, "r", encoding=encoding) as file:
            return file.read()
    except UnicodeDecodeError:
        print(f"Error decoding file with encoding {encoding}")
        return None
    except FileNotFoundError:
        print(f"File '{filename}' not found")
        return None

print("\nFile handling examples demonstrated above.")
print("In actual usage, replace example filenames with real file paths.")
