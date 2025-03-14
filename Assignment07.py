# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   RPathak,3/12/2025,Created Script
#
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str  # Hold the choice made by the user.

# Create a Person Class: Data Layer
class Person:
    """
        Represents a generic Person with first name and last name.
        Change Log:  RPathak,3/12/2025,Created Script

        """
    def __init__(self, first_name: str = '', last_name: str = ''):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self):
        return self.__first_name.title()

    """Getter method to return the first name in title case."""

    @first_name.setter
    def first_name(self, value: str):
        if value.isalpha():  # error handling if value is not alphabets
            self.__first_name = value
        else:
            raise ValueError("The first name should not contain numbers.")
    """Setter method to ensure the first name contains only alphabetic characters."""

    @property
    def last_name(self):
        return self.__last_name.title()
    """Getter method to return the last name in title case."""

    @last_name.setter
    def last_name(self, value: str):
        if value.isalpha():  # error handling if value is not alphabets
            self.__last_name = value
        else:
            raise ValueError("The last name should not contain numbers.")
    """Setter method to ensure the last name contains only alphabetic characters."""

    def __str__(self):
        return f'{self.first_name},{self.last_name}'
    """Return formatted 1st and last name."""

#  Create a Student Class; inherits from Person class above; also extends Person class by adding course name: Data Layer
class Student(Person):
    """
        Represents a student enrolled in a course.
        Inherits first and last name properties from Person.
        Change Log:  RPathak,3/12/2025,Created Script

        """

    def __init__(self, first_name: str = '', last_name: str = '', course_name: str = ''):
        super().__init__(first_name=first_name, last_name=last_name)
        self.course_name = course_name

    @property
    def course_name(self):
        return self.__course_name

    @course_name.setter
    def course_name(self, value: str):
        self.__course_name = value

    def __str__(self):
        return f'{self.first_name},{self.last_name},{self.course_name}'


class FileProcessor: # Processing Layer
    """
        Handles file operations related to reading and writing student enrollment data.
        Change Log:  RPathak,3/12/2025,Created Script

        """
    @staticmethod
    def read_data_from_file(file_name: str):

        try:

            file = open(file_name, "r")
            students = json.load(file)
            student_objects = []
            for student in students:
                student_object: Student = Student(first_name=student["FirstName"],
                                                  last_name=student["LastName"],
                                                  course_name=student["CourseName"])
                student_objects.append(student_object)

            file.close()

        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)

        finally:
            if file.closed == False:
                file.close()

        return student_objects

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        try:
            list_of_dictionary_data: list = []
            for student in student_data:  # Convert List of Student objects to list of dictionary rows.
                students: dict \
                    = {"FirstName": student.first_name, "LastName": student.last_name,
                       "CourseName": student.course_name}
                list_of_dictionary_data.append(students)

            file = open(file_name, "w")
            json.dump(list_of_dictionary_data, file)
            file.close()
        except TypeError as e:
            IO.output_error_messages("There was an issue with your JSON file ", e)
        except Exception as e:
            IO.output_error_messages("There was a non-specific error. ", e)
        finally:
            if file.closed == False:
                file.close()


class IO: # Presentation layer
    """
       Handles input and output operations for the course registration program.
        Change Log:  RPathak,3/12/2025,Created Script

        """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
               Handles output error message and error handling
                Change Log:  RPathak,3/12/2025,Created Script
                """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """
                 Shows Menu choices to user .
                Change Log:  RPathak,3/12/2025,Created Script
                 """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """
                Shows Menu choices to user and exception handling .
                Change Log:  RPathak,3/12/2025,Created Script
            """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())

        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        """
            Shows list of all students and rgistered courses .
            Change Log:  RPathak,3/12/2025,Created Script
            """
        print("-" * 50)
        for student in student_data:
            print(f'Student {student.first_name} '
                  f'{student.last_name} is enrolled in {student.course_name}')

        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """
            SAccepts user input for student first and last name and course name
             validations and Exception handling for 1st and last name.
            Change Log:  RPathak,3/12/2025,Created Script
            """
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")
            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")
            course_name = input("Please enter the name of the course: ")

            student: Student = Student(first_name=student_first_name, last_name=student_last_name,
                                       course_name=course_name)

            student_data.append(student)
            print()
            print(f"You have registered {student.first_name} {student.last_name} for {student.course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was the correct type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data

    # Start of main body
    # When the program starts, the contents of the "Enrollments.json" are automatically read into a two-dimensional
    # list of dictionaries rows then converts the data into a list of Student object rows.

students = FileProcessor.read_data_from_file(file_name=FILE_NAME)

# Present and Process the data
while (True):

    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue
    elif menu_choice == "2":
        IO.output_student_and_course_names(students)
        continue
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue
    elif menu_choice == "4":
        break  # out of the loop

print("Program Ended")