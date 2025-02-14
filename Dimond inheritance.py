
from functools import reduce
from operator import mul

def make_class(attributes, base_class=None):
    """
    Create a new class represented as a dispatch dictionary.

    Args:
        attributes (dict): A dictionary containing the attributes and methods of the class.
        base_class (list, optional): A list of base classes (dispatch dictionaries) to inherit from.

    Returns:
        dict: A dispatch dictionary representing the class.
    """

    def get_value(name):
        """Retrieve an attribute or method, checking base classes if necessary."""
        if name in attributes:
            return attributes[name]
        elif base_class is not None:
            for base in base_class:
                if base['get'](name):
                    return base['get'](name)

    def set_value(name, value):
        """Set an attribute or method in the class."""
        attributes[name] = value

    def new(*args):
        """Create a new instance of the class and initialize it."""
        return init_instance(cls, *args)

    cls = {'get': get_value, 'set': set_value, 'new': new}
    return cls

def init_instance(cls, *args):
    """
    Create a new object instance of type cls and initialize it with args.

    Args:
        cls (dict): The dispatch dictionary representing the class.
        *args: Arguments to pass to the '__init__' method if it exists.

    Returns:
        dict: A dispatch dictionary representing the instance.
    """
    instance = make_instance(cls)
    init = cls['get']('__init__')
    if init:
        init(instance, *args)
    return instance

def make_instance(cls):
    """
    Create a new object instance, represented as a dispatch dictionary.

    Args:
        cls (dict): The dispatch dictionary representing the class.

    Returns:
        dict: A dispatch dictionary representing the instance.
    """
    attributes = {}

    def get_value(name):
        """Retrieve an attribute or method, checking the class if necessary."""
        if name in attributes:
            return attributes[name]
        else:
            method_name = cls['get'](name)
            return bind_method(method_name, instance)

    def set_value(name, value):
        """Set an attribute or method in the instance."""
        attributes[name] = value

    instance = {'get': get_value, 'set': set_value}
    return instance

def bind_method(method_name, instance):
    """
    Bind a method to an instance if it is callable.

    Args:
        method_name (callable or any): A method or attribute retrieved from the class.
        instance (dict): The dispatch dictionary representing the instance.

    Returns:
        callable or any: A bound method if `method_name` is callable, otherwise the original value.
    """
    if callable(method_name):
        def method(*args):
            return method_name(instance, *args)

        return method
    else:
        return method_name



def MyDate():
    """
      Creates a new class representing a date with day, month, and year attributes.
      Supports getting and setting these attributes with validation.

      Methods:
          - __init__(day, month, year): Initializes the date.
          - __repr__(): Returns a string representation of the object.
          - __str__(): Returns a formatted string in dd.mm.yyyy format.
          - getDay(): Returns the day.
          - getMonth(): Returns the month.
          - getYear(): Returns the year.
          - setDay(day): Sets the day if within valid range (1-30).
          - setMonth(month): Sets the month if within valid range (1-12).
          - setYear(year): Sets the year if within valid range (1900-2100).
      """

    def __init__(self, day, month, year=2020):
        """Initializes a MyDate instance with day, month, and year."""

        self['set']('day', day)
        self['set']('month', month)
        self['set']('year', year)

    def __repr__(self):
        """Returns a string representation of the date object."""
        return 'MyDate({0}, {1}, {2})'.format(self.day, self.month, self.year)

    def __str__(self):
        """Returns the date formatted as dd.mm.yyyy."""
        return f'{str(getDay(self))}.{str(getMonth(self))}.{str(getYear(self))}'

    def getDay(self):
        """Returns the day value."""
        return self['get']('day')

    def getMonth(self):
        """Returns the month value."""
        return self['get']('month')

    def getYear(self):
        """Returns the year value."""
        return self['get']('year')

    def setDay(self, day):
        """Sets the day if within the valid range (1-30)."""
        if 1 <= day <= 30:
            self['set']('day', day)

    def setMonth(self, month):
        """Sets the month if within the valid range (1-12)."""
        if 1 <= month <= 12:
            self['set']('month', month)

    def setYear(self, year):
        """Sets the year if within the valid range (1900-2100)."""
        if 1900 <= year <= 2100:
            self['set']('year', year)

    return make_class({'__init__': __init__, 'str': __str__, '__repr__': __repr__, 'getDay': getDay, 'getMonth': getMonth, 'getYear': getYear,
                       'setDay': setDay, 'setMonth': setMonth, 'setYear': setYear})
Date = MyDate()

def Person():
    """
        Creates a new class representing a person with first name, last name, birth date, and ID.
        Supports getting and setting these attributes.

        Methods:
            - __init__(firstName, lastName, date, id): Initializes a person.
            - __repr__(): Returns a string representation of the person.
            - __str__(): Returns a formatted string with person's details.
            - getFirstName(): Returns the first name.
            - getLastName(): Returns the last name.
            - getDate(): Returns the formatted birth date.
            - getId(): Returns the ID.
            - setFirstName(firstName): Sets the first name.
            - setLastName(lastName): Sets the last name.
            - setDate(date): Sets the birth date.
            - setId(id): Sets the ID if positive.
        """

    def __init__(self, firstName, lastName, date, id):
        """Initializes a Person instance with first name, last name, date, and ID."""

        self['set']('firstName', firstName)
        self['set']('lastName', lastName)
        self['set']('date', date)
        self['set']('id', id)

    def __repr__(self):
        """Returns a string representation of the person."""

        return 'Person({0}, {1}, {2}, {3})'.format(getFirstName(self), getLastName(self), getDate(self), getId(self))

    def __str__(self):
        """Returns a string representation of the person."""
        return strAttributes(self)

    def getAttributes(self):
        return '{0}, {1}, {2}, {3}'.format(getFirstName(self), getLastName(self), getDate(self), getId(self))

    def strAttributes(self):
        return f'name: {str(getFirstName(self))} {str(getLastName(self))}\nDoB: {str(getDate(self))} \nID: {str(getId(self))}'

    def getFirstName(self):
        """Returns the first name."""
        return self['get']('firstName')

    def getLastName(self):
        """Returns the last name."""
        return self['get']('lastName')

    def getDate(self):
        """Returns the formatted birth date."""
        return self['get']('date')['get']('str')()

    def getId(self):
        """Returns the ID."""
        return self['get']('id')

    def setFirstName(self, firstName):
        """Sets the first name."""
        self['set']('firstName', firstName)

    def setLastName(self, lastName):
        """Sets the last name."""
        self['set']('lastName', lastName)

    def setDate(self, date):
        """Sets the birth date."""
        self['set']('date', date)

    def setId(self, id):
        """Sets the ID if positive."""
        if id > 0:
            self['set']('id', id)

    return make_class({'__init__': __init__, 'str': __str__, 'repr': __repr__, 'getFirstName': getFirstName,  'getLastName': getLastName,  'getId': getId, 'getDate':getDate,
                       'setFirstName': setFirstName, 'setLastName': setLastName, 'setDate': setDate, 'setId': setId, 'getAttributes': getAttributes, 'strAttributes':strAttributes})
Person = Person()

def Student():
    """
    Return the Student class, which represents a student with personal and academic information.
    The class provides methods to access and modify the student's details, including:
    - First name, last name, ID, and date of birth (inherited from Person class)
    - Faculty, grades, and seniority (specific to the student)

    Methods include getter and setter methods for these attributes, as well as string representations.
    """

    def __init__(self, firstName, lastName, date, id, faculty, grades, seniority):
        """
        Initialize a new student with the provided information.

        Args:
            firstName (str): The student's first name.
            lastName (str): The student's last name.
            date (Date): The student's date of birth.
            id (int): The student's ID number.
            faculty (str): The student's faculty.
            grades (float): The student's average grades.
            seniority (int): The student's year of study (e.g., 1st, 2nd, 3rd year).
        """
        Person['get']('__init__')(self, firstName, lastName, date, id)  # Initialize the parent class (Person)
        self['set']('faculty', faculty)
        self['set']('grades', grades)
        self['set']('seniority', seniority)

    def __repr__(self):
        """
        Returns a string representation of the Student object for debugging and inspection.
        Combines attributes from the Person class and student-specific attributes.
        Combines attributes from the Person class and student-specific attributes.

        Returns:
            str: A string representation of the Student object.
        """
        return f'Student({Person["get"]("getAttributes")(self)}, {getAttributes(self)})'

    def __str__(self):
        """
        Returns a user-friendly string representation of the Student object.

        Returns:
            str: A string representation of the Student object.
        """
        return Person['get']('str')(self) + strAttributes(self)

    def getAttributes(self):
        """
        Returns a formatted string with the student's academic information.

        Returns:
            str: A string containing the student's faculty, grades, and seniority.
        """
        return '{0}, {1}, {2}'.format(getFaculty(self), getGrades(self), getSeniority(self))

    def strAttributes(self):
        """
        Returns a string containing the student's academic details in a human-readable format.

        Returns:
            str: A string representing the student's academic details.
        """
        return f'\nLearning: {str(getFaculty(self))} \nAvg: {str(getGrades(self))}\nSeniority: {str(getSeniority(self))}'

    def getFaculty(self):
        """
        Getter method for the student's faculty.

        Returns:
            str: The student's faculty.
        """
        return self['get']('faculty')

    def getGrades(self):
        """
        Getter method for the student's grades.

        Returns:
            float: The student's average grades.
        """
        return self['get']('grades')

    def getSeniority(self):
        """
        Getter method for the student's seniority.

        Returns:
            int: The student's year of study (e.g., 1st year, 2nd year).
        """
        return self['get']('seniority')

    def setFaculty(self, faculty):
        """
        Setter method for the student's faculty.

        Args:
            faculty (str): The new faculty for the student.
        """
        self['set']('faculty', faculty)

    def setGrades(self, grades):
        """
        Setter method for the student's grades.

        Args:
            grades (float): The new average grades for the student.
        """
        self['set']('grades', grades)

    def setSeniority(self, seniority):
        """
        Setter method for the student's seniority.

        Args:
            seniority (int): The new year of study for the student.
        """
        self['set']('seniority', seniority)

    return make_class({
        '__init__': __init__,
        'str': __str__,
        'repr': __repr__,
        'getFaculty': getFaculty,
        'getGrades': getGrades,
        'getSeniority': getSeniority,
        'setFaculty': setFaculty,
        'setGrades': setGrades,
        'setSeniority': setSeniority,
        'getAttributes': getAttributes,
        'strAttributes': strAttributes
    }, [Person])
Student = Student()

def Faculty ():
    """
    Creates a Faculty class by extending the Person class with additional attributes for teaching, salary, and seniority.
    """

    def __init__(self, firstName, lastName, date, id, teaching, salary, seniority):
        """
        Initializes a new faculty member with given details.
        """
        Person['get']('__init__')(self, firstName, lastName, date, id)
        self['set']('teaching', teaching)  # Set the teaching attribute
        self['set']('salary', salary)  # Set the salary attribute
        self['set']('seniority', seniority)  # Set the seniority attribute

    def __repr__(self):
        """
        Returns a string representation of the Faculty object.
        """
        return f"Faculty({Person['get']('getAttributes')(self)}, {getAttributes(self)})"

    def __str__(self):
        """
        Returns a string version of the Faculty object.
        """
        return Person['get']('str')(self) + strAttributes(self)

    def getAttributes(self):
        """
        Returns the combined attributes of the Faculty member.
        """
        return '{0}, {1}, {2}'.format(getTeaching(self), getSalary(self), getSeniority(self))

    def strAttributes(self):
        """
        Returns formatted teaching, salary, and seniority details.
        """
        return f'\nTeaching: {str(getTeaching(self))} \nSalary: {str(getSalary(self))}\nSeniority: {str(getSeniority(self))}'

    def getTeaching(self):
        """
        Gets the teaching subject of the faculty member.
        """
        return self['get']('teaching')

    def getSalary(self):
        """
        Gets the salary of the faculty member.
        """
        return self['get']('salary')

    def getSeniority(self):

        """
        Gets the seniority level of the faculty member.
        """
        return self['get']('seniority')

    def setTeaching(self, teaching):
        """
        Sets the teaching subject for the faculty member.
        """
        self['set']('teaching', teaching)

    def setSalary(self, salary):
        """
        Sets the salary for the faculty member.
        """
        self['set']('salary', salary)

    def setSeniority(self, seniority):
        """
        Sets the seniority level for the faculty member.
        """
        self['set']('seniority', seniority)

    # Returns a new Faculty class by creating a class using the make_class method, extending the Person class.
    return make_class({'__init__': __init__, 'str': __str__, 'repr': __repr__, 'getTeaching': getTeaching,  'getSalary': getSalary,  'getSeniority': getSeniority,
                       'setTeaching': setTeaching, 'setSalary': setSalary, 'setSeniority': setSeniority, 'getAttributes': getAttributes, 'strAttributes':strAttributes}, [Person])
Faculty = Faculty()  # Instantiate the Faculty class

def TA ():
    """
    Creates a Teaching Assistant (TA) class that combines attributes of both Student and Faculty classes.
    """

    def __init__(self, firstName, lastName, date, id, faculty, grades, s_seniority, teaching, salary, f_seniority):
        """
        Initializes a new Teaching Assistant (TA) by combining attributes of Student and Faculty classes.
        """
        Student['get']('__init__')(self, firstName, lastName, date, id, faculty, grades, s_seniority)
        Faculty['get']('__init__')(self, firstName, lastName, date, id, teaching, salary, f_seniority)

    def __repr__(self):
        """
        Returns a string representation of the TA object, combining attributes of Student and Faculty.
        """
        return f"TA({Person['get']('getAttributes')(self)}, {Student['get']('getAttributes')(self)}, {Faculty['get']('getAttributes')(self)})"

    def __str__(self):
        """
        Returns a string version of the TA object, combining string representations of Student and Faculty.
        """
        return Student['get']('str')(self) + Faculty['get']('strAttributes')(self)

    def getStudentSeniority(self):
        """
        Gets the seniority level of the Student.
        """
        return Student['get']('getSeniority')(self)

    def getFacultySeniority(self):
        """
        Gets the seniority level of the Faculty.
        """
        return Faculty['get']('getSeniority')(self)

    def setStudentSeniority(self, seniority):
        """
        Sets the seniority level for the Student.
        """
        Student['get']('setSeniority')(self, seniority)

    def setFacultySeniority(self, seniority):
        """
        Sets the seniority level for the Faculty.
        """
        Faculty['get']('setSeniority')(self, seniority)

    # Returns a new TA class by creating a class using the make_class method, inheriting from both Student and Faculty classes.
    return make_class({'__init__': __init__, 'str': __str__, 'repr': __repr__, 'getStudentSeniority':getStudentSeniority, 'getFacultySeniority':getFacultySeniority,
                       'setStudentSeniority':setStudentSeniority, 'setFacultySeniority':setFacultySeniority}, [Student, Faculty] )
TA = TA()  # Instantiate the TA class


