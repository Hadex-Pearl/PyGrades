# -*- coding: utf-8 -*-
"""
This module contains the Course class.

@author: George 
@co-author: Hyusuf
"""

#######################################################################
from student import Student
class Course:
    """
    A class that keeps track of course name, semester, TAs and 
    maintains a list of students in the course. 
    
    @author: George
    """
    def __init__(self, course_id='', course_name='',instructor='',semester=''):
        """
        Sets up the instance variables
        __course_id, __course_name,__instructor,__semester: are all strings
        """
        self.__course_id=course_id
        self.__course_name=course_name
        self.__instructor=instructor
        self.__semester=semester
        #these below will be added by methods
        self.__course_tas=[]
        self.__classlist=[]
    #accessors
    def get_course_id(self):
        return self.__course_id
    def get_course_name(self):
        return self.__course_name
    def get_instructor(self):
        return self.__instructor
    def get_semester(self):
        return self.__semester
    def get_course_tas(self):
        return self.__course_tas
    def get_classlist(self):
        return self.__classlist
    
    #mutators
    def set_course_id(self, course_id):
        self.__course_id=course_id
    def set_course_name(self, course_name):
        self.__course_name=course_name
    def set_instructor(self,instructor):
        self.__instructor=instructor
    def set_semester(self,semester):
        self.__semester=semester
    def set_courseTAs(self, course_tas):
        self.__course_tas=course_tas
    def set_classlist(self, classlist):
        self.__classlist=classlist
        
    def add_student(self,student):
        """
        Receives a Student object and adds it to the classlist.
        """
        self.__classlist.append(student)
        
    def add_ta(self,ta_name):
        """
        Receives a TA name and adds it to the list of TAs.
        """
        self.__course_tas.append(ta_name)
        
    def compute_class_average(self):
        """
        Accesses all Student objects, computes each students average
        and then computes the class everage.
        """
        sum=0 #running
        for student in self.__classlist:
            sum+=student.percentage_gen()
            
        return sum/len(self.__classlist)
    

    def add_students_from_file(self, filename):
        """
        #Adds students from file
        Parameters: filename, a file path
        """
        with open(filename) as filereader:#this will use the context manager to ensure open files are properly closed.
            lines=filereader.readlines()
            for line in lines[5:]:
                line=line.strip('\n')
                roll_no,name,*hwk=line.split(':')
                #Convert homework into numbers
                marks=[eval(mark) for mark in hwk]
                #create a student
                student=Student(roll_no,name)
                #set the marks
                student.set_marks(marks)
                #add to list
                self.add_student(student)
                #print(roll_no, name, marks, student)
            #File will be closed properly.

    def add_course_data_from_file(self, filename):
        """
        Add course details from file
        parameters: filename, a file path
        """
        with open(filename) as filereader:#this will use the context manager to ensure open files are properly closed.
            lines=filereader.readlines()
            striped_lines = []
            for line in lines:
                line = line.strip('\n')
                striped_lines.append(line)
            #Assign course details and set them
            course_id = striped_lines[0]
            self.set_course_id(course_id)
            course_name = striped_lines[1]
            self.set_course_name(course_name)
            semester = striped_lines[2]
            self.set_semester(semester)
            instructor = striped_lines[3]
            self.set_instructor(instructor)
            course_tas = striped_lines[4]
            self.set_courseTAs(course_tas)
        #File will be closed properly.

    def print_course_details(self, filename):
        """
        Receives an output file name and outputs course details
        """
        with open(filename,'w') as filewriter:
            filewriter.write(f"{'*'*50}\nCourse ID:{self.__course_id}\
            \nCourse:{self.__course_name}\nInstructor:{self.__instructor}\
            \nSemester:{self.__semester}\nTAs:{self.__course_tas}\n{'*'*50}\n\n")
                
            #Retrieve each student, extract the details, compute the average and grade
            #and output roll_num, name, percentage mark, and grade to file.
            for student in self.__classlist:
                #compute the percentage mark
                percentage=student.percentage_gen()
                #compute grade
                grade=student.grade_gen()
                filewriter.write(f"{student.get_roll_num():8s}{student.get_name():20s}\
                {percentage:8.2f} {grade:3s}\n")
            #Output class average
            filewriter.write(f"\n{'-'*25}\nClass Average:{self.compute_class_average():8.2f}\n{'-'*25}\n")
            
            #context manager will close the file appropriately  
        
    def __str__(self):
        """
        Returns a string representation of a Course object
        """
        return f"{'**'*20}\nCourse:{self.__course_name}\nInstructor:{self.__instructor}\
                \nSemester:{str(self.__semester)}\nTAs:{str(self.__course_tas)}\
                    \n{'**'*20}"
    
#Course class definition ends.

  
#You can uncomment the codes below, run, and examine what happens.
"""
#create student
student=Student() #Initializes the student object with default values.
student.set_roll_num('s1010')
student.set_name('Yam Foo Foo')
student.set_marks([20,60,80,34,90])

#Output student details to console
print(student)

#create course
course=Course()
#add student
course.add_student(student)

#create another student
student2=Student('s1007','Greg Gregory') #Calls the parametrized constructor. 
student2.set_marks([100,100,90,70,80])
#add student
course.add_student(student2)

#Output course details to the console.
print(course)
#Loop through and print each student in the course
list=course.get_classlist()
for student in list:
    print(student)


#Now read the student details from a file and write the course details to a file.
course2=Course() # I have not bothered to specify instructor, semester, tas, course_id and course_name
course2.add_students_from_file('data/course1.txt')
course2.print_course_details('results.txt')
"""

#a = Course()
#a.add_students_from_file('data/course1.txt')
#a.add_course_data_from_file('data/course5.txt')
#print(a)