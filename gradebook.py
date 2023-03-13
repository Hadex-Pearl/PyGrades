
"""
@author : <Hyusuf>
@date: Oct. 5, 2022
Description: <This module contains a Gradebook class>
    Has instance variable - courses: an empty dictionary

    Functions associated with the class:
    -get_courses: To access the instance variable

    -read_files: To read filenames from a user and return list of filenames

    -read_courses: To append course objects from <class Course> to the instance variable

    -find: To check if a student is registered in a course

    -find_student: To identify a specific student in a course

    -trnascript: To analyse student transcript

    -print_transcript: To write student transcript in a file

    -all_student: To get rollnumber of all registered students

    -check_passes: To check students that passed all registered courses

    -passes_gen: To write passed students into a file

    -check_referrals: to check students that are referred to a course based on their grades

    -referrrals_gen: To write referred students into a file

    -course_average, class_average: The two fuctions finds the class average for each courses but returns
        output in different format (check function documentation for details)
    
    -total_average: To comute student total average for all registered courses

    -grade_gen: To write all students grades for all courses in a file

    -transcript_gen: To write all students transcript in a file

    -find_course: To find a specific course object

    -registered_course: To write all students registered in a course and their grades in a file
"""
from course import Course
class GradeBook:
    def __init__(self, courses={}):
        self.__courses = courses

    #Accessor
    def get_courses(self):
        return self.__courses

    def read_files(self):
        """
        Allows users to input filename(s) of txt extention
        Return: list of filename(s)
        """
        user_input = list(input('Please enter file names separated by a comma ').split(','))
        files = []
        for string in user_input:
            files.append(string.strip())
        for i in range(len(files)):
            file = files[i]
            if '.txt' in file:                
                continue
            else:               
                file +='.txt'
                files[i] = file          
        #Making the list have unique file names
        set_list = set(files)
        U_files = list(set_list)
        return U_files

    def read_courses(self):
        """
        Uses read_file method to read file name(s)
        Adds course details from file(s) into the instance variable (an empty dictionary)
        Return: A dictionary
            keys: course ids
            values: course objects (from Course class) 
        """
        file_list = self.read_files()
        for file in file_list:
            #Create course object
            course=Course()
            #get course detais
            course.add_course_data_from_file(file)
            #get student details
            course.add_students_from_file(file)
            self.__courses[course.get_course_id()] = course
        
        return self.__courses


    def find(self, roll_num):
        """
        Checks if student is registered in a course

        parameter: roll_num; student rollnumber
        
        Return: True - if student exist or
                False - if student does not exist
        """
        #Creating the list of all registered students rollnumber
        student_list = []
        for value in self.get_courses().values():
            for student in value.get_classlist():
                student_list.append(student.get_roll_num()) 
        #Checking if rollnumber is in the list
        if roll_num in student_list:
            return True
        else:
            return False

    def find_student(self, roll_num, class_list):
        """
        Finds a specific student 

        Parameter: roll_num; student rollnumber
                    class_list; list of student objects(from Student class)
        
        Return: student object for the specific student
        """
        for student in class_list:
            if roll_num == student.get_roll_num():
                return student
        
    def transcript(self, roll_num):
        """
        Evaluates student transcript

        Parameter: roll_num; student rollnumber

        Return: text (if the student is registered); formated text containing student rollnumber, student name, 
                all courses offered by the student, course average and the grades. 
                A statement (if the student is not registered); This is not a registered roll number 
        """
        #Checks if student is registered
        if self.find(roll_num) == True:
            #get course details as a dictionary
            course_dict = self.get_courses()
            #Creating list of course ids
            course_ids = list(self.get_courses().keys())
            #sorting list of course ids
            course_ids = sorted(course_ids)
            #creating list of course objects according to the student id
            course_obj_list = []
            for id in course_ids:
                course_obj = course_dict[id]
                course_obj_list.append(course_obj)
            #Identify the student and get the transcript details
            student = self.find_student(roll_num, course_obj_list[0].get_classlist())
            student_name = student.get_name()
            text=f'Student {roll_num} transcript: \n\n'
            text+='-'*65 + '\n\n'
            text+=f'{roll_num:10s} {student_name}\n\n'
            for i in range(len(course_ids)):
                course_detail = self.find_student(roll_num, course_obj_list[i].get_classlist())
                course_percent = course_detail.percentage_gen()
                course_grade = course_detail.grade_gen()
                course_name = course_obj_list[i].get_course_name()
                text+=f'{course_ids[i]:10s} {course_name:35s} {course_percent:10.1f} {course_grade:10s}\n\n'
            text+='-'*65
            text+='\n\n'
            return text
        else:
            return f"This is not a registered roll number"

    def print_transcript(self, roll_num):
        """
        Writes student transcript details into a file

        Parameter: roll_num; student rollnumber
        """
        with open('results/rollnum_transcript.txt','w') as filewriter:#this will use the context manager to ensure open files are properly closed.
            Student_transcript = self.transcript(roll_num)
            filewriter.write(Student_transcript)
        #File will be closed properly.

    def all_student(self):
        """
        Gets rollnumber of all registered students. it takes no parameter

        Return: roll_nums; a list of student rollnumbers
        """
        #get course details as a dictionary
        course_dict = self.get_courses()
        #get values of the dictionary (course objects) as a list
        course_objs = list(course_dict.values())
        roll_nums = []
        #loop into course objects to get all student rollnumbers and append to the empty list
        for obj in course_objs:
            students = obj.get_classlist()
            for student in students:
                roll_num = student.get_roll_num()
                roll_nums.append(roll_num)
        roll_nums = set(roll_nums)
        roll_nums = (list(roll_nums))
        roll_nums.sort()       
        return roll_nums

    def check_passes(self):
        """
        checks for students that passed all registered courses. It takes no parameter

        Return: roll_num; a list of students that passed
        """
        #get course details as a dictionary
        course_dict = self.get_courses()
        #get values of the dictionary (course objects) as a list
        course_objs = list(course_dict.values())
        #get rollnumber list of all student
        roll_nums = self.all_student()
        #check for students that get an average more that or equal to 60 in all courses
        for obj in course_objs:
            class_list = obj.get_classlist()
            for student in class_list:
                #students that failed are removed from the list of students
                if student.percentage_gen() >= 60:
                    continue
                else:
                    roll_nums.remove(student.get_roll_num())
        return roll_nums

    def passes_gen(self):
        """
        This writes details of student that passed in a file
        """
        with open('results/passes.txt','w') as filewriter:#this will use the context manager to ensure open files are properly closed.
            filewriter.write('List of students who passed all registered courses\n')
            filewriter.write('\n')
            roll_nums = self.check_passes()
            #get course details as a dictionary
            course_dict = self.get_courses()
            #get values of the dictionary (course objects) as a list
            course_objs = list(course_dict.values())
            #get student name and rollnumber and print
            students = course_objs[0].get_classlist()
            for student in students:
                for roll_num in roll_nums:
                    if roll_num == student.get_roll_num():
                        filewriter.write(f'{roll_num:8s} {student.get_name()}\n')    
        #File will be closed properly.


    def check_referrals(self):
        """
        This checks for students that are referred to a course. It takes no parameter
        """
        #get course details as a dictionary
        course_dict = self.get_courses()
        #get values of the dictionary (course objects) as a list
        course_objs = list(course_dict.values())
        #creating an empty dictionary to house referred students
        referred_student = {}
        for obj in course_objs:
            #get the class list for the course object
            class_list = obj.get_classlist()
            for student in class_list:
                #check for students that did not pass
                if student.percentage_gen() < 60:
                    #check if the student detail is already in the dictionary
                    if student.get_roll_num() in referred_student.keys():
                        #append course name to the list of values in the dictionary
                        referred_student[student.get_roll_num()].append(obj.get_course_name())
                    else:
                        #create an empty list as a value and append the course name
                        referred_student[student.get_roll_num()] = []
                        referred_student[student.get_roll_num()].append(obj.get_course_name())
        #sort the the dictionary by key
        referred_student = dict(sorted(referred_student.items()))
        return referred_student

    def referrals_gen(self):
        """
        This write details of referred student into a file
        """
        with open('results/referrals.txt','w') as filewriter:#this will use the context manager to ensure open files are properly closed.
            filewriter.write('List of students who have been referred to course(s)\n')
            filewriter.write('\n')
            #use check_referral method to get the dictionary containing student names and course
            referrals = self.check_referrals()
            #get course details as a dictionary
            course_dict = self.get_courses()
            #get keys of the dictionary (course ids) as a list
            course_ids = list(course_dict.keys())
            #get values of the dictionary (course objects) as a list
            course_objs = list(course_dict.values())
            new_dict = {}
            for i in range(len(course_ids)):
                new_dict[course_ids[i]] = course_objs[i].get_course_name()
            #write student details in a file
            students = course_objs[0].get_classlist()
            for student in students:
                for roll_num in referrals.keys():
                    if roll_num == student.get_roll_num():
                        filewriter.write(f'{roll_num:8s} {student.get_name():18s} \n')
                        for i in range(len(referrals[roll_num])):
                            course_id = [k for k, v in new_dict.items() if v == referrals[roll_num][i]][0]
                            filewriter.write('{:9s}'.format(' '))
                            filewriter.write(f'{course_id} {referrals[roll_num][i]}\n')    
        #File will be closed properly.

    def course_average(self):
        """
        This computes course average for all student and for all courses.

        Return: average_dict; a nested dictionary of the format {course ids: {student rollnumber: [average]}}
        """
        #get course details as a dictionary
        course_dict = self.get_courses()
        #get values of the dictionary (course objects) as a list
        course_objs = list(course_dict.values())
        #create an empty dictionary
        average_dict = {}
        for obj in course_objs:
            #create an empty dictionary as value of the dictionary
            average_dict[obj.get_course_id()] = {}
            student_list = obj.get_classlist()
            for student in student_list:
                #create a list as dictionary value and append student average
                average_dict[obj.get_course_id()][student.get_roll_num()] = []
                average_dict[obj.get_course_id()][student.get_roll_num()].extend([student.get_name(),student.percentage_gen()])
        #sort the dictionary
        average_dict = dict(sorted(average_dict.items()))

        return average_dict

    def class_average(self):
        """
        This collects course average for each student

        Return: cl_average; a dictionary with student rollnumber as key and a list of averages as values
        """
        #get dictionary from course_average method
        average_dict = self.course_average()
        cl_average = {}
        for id,value in average_dict.items():
            for roll_num,value in average_dict[id].items():
                #adding averages and rollnumbers to the list
                if roll_num in cl_average:
                    cl_average[roll_num][1].append(average_dict[id][roll_num][1])
                else:
                    cl_average[roll_num] = [average_dict[id][roll_num][0],[]]
                    cl_average[roll_num][1].append(average_dict[id][roll_num][1])

        return cl_average

    def total_average(self):
        """
        This computes the total average score for each student

        Return: student_average; a dictionary with student rollnumber as key and student total average as value
        """
        #get student average for all courses
        student_average = self.class_average()
        for roll_num,averages in student_average.items():
            #compute total average
            average = sum(averages[1])/len(averages[1])
            student_average[roll_num] = average

        return student_average

    def grades_gen(self):
        """
        This writes all students grades for all courses and the total average and determines the best student
        """
        with open('results/grades.txt','w') as filewriter: #this will use the context manager to ensure open files are properly closed.
            #get student average for each course
            average_dict = self.course_average()
            #get student average for all the course
            class_average = self.class_average()
            #get student total average
            student_average = self.total_average()
            #write grade details into a file
            filewriter.write(f'Students\' grades: \n\n')
            filewriter.write('{:10s} {:24s} '.format('Rollnum', 'Name'))
            for id in average_dict.keys():
                filewriter.write(f'{id:12s}')
            filewriter.write('{:10s} \n'.format('Avg'))
            filewriter.write('-'*100 + '\n\n')
            for roll_num,ave_list in class_average.items():
                filewriter.write(f'{roll_num:10s} {ave_list[0]:18s}')
                for i in range(len(ave_list[1])):
                    filewriter.write(f'{ave_list[1][i]:12.2f}')
                filewriter.write(f'{student_average[roll_num]:10.2f}')
                filewriter.write('\n\n')

            #determine the best student and write in the file
            best_ave = max(list(student_average.values()))
            best_student = list(student_average.values()).index(best_ave)
            best_student_num = list(student_average.keys())[best_student]
            filewriter.write(f'Best Student: {best_student_num}, {class_average[best_student_num][0]}')
        #File will be closed properly.

    def transcript_gen(self):
        """
        This writes all student transcript in a file (results/transcripts.txt)
        """
        with open('results/transcripts.txt','w') as filewriter: #this will use the context manager to ensure open files are properly closed.
            #get all the student rollnumber and loop in it
            all_student_num = self.all_student()
            for student in all_student_num:
                #get individual student transcripts and write in a file
                student_transcript = self.transcript(student)
                filewriter.write(student_transcript)
        #File will be closed properly.

    def find_course(self, course_id, course_dict):
        """
        This finds a specific course offered in the school

        Parameter: course_id; a string
                    course_dict; a dictionary containing course details

        Return: obj; a course object (from the Course class)
        """
        for id,obj in course_dict.items():
            if course_id == id:
                return obj
    
    def registered_students(self, course_id):
        """
        This writes all student details for a specific course into a file (results/courseid_grades.txt)

        Parameter: course_id; a string
        """
        with open('results/courseid_grades.txt','w') as filewriter: #this will use the context manager to ensure open files are properly closed.
            #get course details as a dictionary
            course_dict = self.get_courses()
            #find the course details for the course id
            course_obj = self.find_course(course_id, course_dict)
            #get the classlist for the course
            students = course_obj.get_classlist()
            #write student details into the file
            filewriter.write(f'Student Grades for {course_id}: {course_obj.get_course_name()} \n\n')
            filewriter.write('{:10s} {:26s} {:15s} \n'.format('Rollnum', 'Name', 'Avg Grade'))
            filewriter.write('-'*65 + '\n\n')
            for student in students:
                filewriter.write(f'{student.get_roll_num():10s} {student.get_name():16s} {student.percentage_gen():15.2f} {student.grade_gen():10s}\n\n')
        #File will be closed properly.


##########################################################################

def test_grade_book():
    """
    Your code to initiate GradeBook and generate the required output files.
    """
    gradebook =GradeBook()
    gradebook.read_courses()
    roll_num = input('Please enter a student roll number: ')
    course_id = input('Please enter a course ID: ')
    gradebook.passes_gen()
    gradebook.referrals_gen()
    gradebook.transcript_gen()
    gradebook.grades_gen()
    gradebook.registered_students(course_id)
    gradebook.print_transcript(roll_num)
    


def main():
    test_grade_book()

if __name__=="__main__":
    main()

