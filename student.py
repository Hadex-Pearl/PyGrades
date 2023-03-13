# -*- coding: utf-8 -*-
"""
This module contains the student class.

@author: George
"""
class Student:
    """
    Student class definition.
    data members: 
        __roll_num, __name, __marks (from five homework assignments): list of marks 
    Each student does 5 homework assignments
    """

    #method definitions
    def __init__(self, roll_num='',name=''):
        """
        Sets up a Student attributes
        """
        self.__roll_num=roll_num
        self.__name=name
        self.__marks=[]
        
    #getters/accessors
    def get_name(self):
        return self.__name
    def get_roll_num(self):
        return self.__roll_num
    def get_marks(self):
        return self.__marks
    
    #mutators
    def set_name(self,name):
        self.__name=name
    def set_roll_num(self, roll_num):
        self.__roll_num=roll_num
    def set_marks(self, marks):
        """
        Sets up homework scores- a list of 5 values.
        """
        self.__marks=marks

    def add_mark(self, mark):
        """
        Adds a single mark to the list of marks

        """
        self.__marks.append(mark)
        
    def percentage_gen(self):
        """
        computes and returns the percentage score. The percentage is a simple average
        """
        return sum(self.__marks)/5
        
    def grade_gen(self):
        """
        Computes and returns the grade.
        """
        
        #compute the percentage
        percentage=self.percentage_gen()
        #compute the grade
        grade=''
        if percentage>=90:
            grade="A"
        elif percentage>=80:
            grade="B"
        elif percentage>=70:
            grade="C"
        elif percentage>=60:
            grade="D"
        else: 
            grade="E"
        #return the grade
        return grade
            
    def __str__(self):
        """
        Returns a string representation of a Student object
        """
        return f"Name:{self.__name}\nRoll Num:{self.__roll_num}\nMarks:\
            {str(self.__marks)}\nPercentage:{str(self.percentage_gen())}\
                \nGrade:{self.grade_gen()}"
    
    #Student class definition ends here.