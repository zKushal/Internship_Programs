StudentDetailsList = []
CourseDetailsList = []
SemesterDetailsList = []
TeacherDetailsList = []

class StudentDetails:
    
    def __init__(self, StudentID, firstName, lastName, age, address, contactNumber ):
        self.StudentID = StudentID
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
        self.address = address
        self.contactNumber = contactNumber
        self.courses = []

        
    def getStudentDetails(self):
       self.StudentID = int(input("Enter Student ID: "))
       self.firstName = input("Enter First Name: ")
       while True:
           if self.firstName.isalpha():
                break
           else:
                print("Please enter a valid name")
       self.lastName = input("Enter Last Name: ")
       self.age = int(input("Enter Age: "))
       self.address = input("Enter Address: ")
       self.contactNumber = input("Enter Contact Number: ")
        
    def displayStudentDetails(self):
        print(f"Student ID: {self.StudentID}")
        print(f"First Name: {self.firstName}")
        print(f"Last Name: {self.lastName}")
        print(f"Age: {self.age}")
        print(f"Address: {self.address}")
        print(f"Phone Number: {self.contactNumber}")

        if self.courses:
            print(f"Enrolled Courses: {', '.join(course[1] for course in self.courses)}")
        else:
            print("Enrolled Courses: None")
        
class CourseDetails:
    
    def __init__(self):
        course1 = [1, "BCA", 4]
        course2 = [2, "BBA", 4]
        course3 = [3, "MCA", 2]
        course4 = [4, "MBA", 2]
        CourseDetailsList.append(course1)
        CourseDetailsList.append(course2)
        CourseDetailsList.append(course3)
        CourseDetailsList.append(course4)
    def displayCourseDetails(self):
        print("Course ID\tCourse Name\tCourse Duration")
        for course in CourseDetailsList:
            print(f"{course[0]}\t\t{course[1]}\t\t{course[2]} years")
            
    def EnrollCourse(self):
        StdID = int(input("Enter Student ID: "))
        courseID = int(input("Enter Course ID to enroll: "))
        StdId = next((stId for stId in  StudentDetailsList if stId.StudentID == StdID), None)
        courseId = next((cId for cId in CourseDetailsList if cId[0] == courseID), None)
        
        if StdId and courseId:
            if courseId not in StdId.courses:
                StdId.courses.append(courseId)  
                print(f"Student {StdId.firstName} {StdId.lastName} has been enrolled in {courseId[1]} course.")
            else:
                print(f"Student {StdId.firstName} {StdId.lastName} is already enrolled in {courseId[1]} course.")
        else:
            print("Invalid Student ID or Course ID. Please try again.")
        
            
        
class TeacherDetails:
    
    def __init__(self, TeacherID, firstName, lastName, age, address, contactNumber, specialization):
        self.TeacherID = TeacherID
        self.firstName = firstName
        self.lastName = lastName
        self.age = age
        self.address = address
        self.contactNumber = contactNumber
        self.specialization = specialization
        
        
    def getTeacherDetails(self):
        self.TeacherID = int(input("Enter Teacher ID: "))
        self.firstName = input("Enter First Name: ")
        self.lastName = input("Enter Last Name: ")
        self.age = int(input("Enter Age: "))
        self.address = input("Enter Address: ")
        self.contactNumber = input("Enter Contact Number: ")
        self.specialization = input("Enter Specialization: ")
        self.courses = []
        
    def displayTeacherDetails(self):
           print("Teacher ID\tFirst Name\tLast Name \tAge\tAddress\tContact Number\tSpecialization\tCourses")
           print(f"{self.TeacherID}\t\t{self.firstName}\t\t{self.lastName}\t\t{self.age}\t{self.address}\t{self.contactNumber}\t{self.specialization}\t{', '.join(course[1] for course in self.courses) if self.courses else 'None'}")
         

    def assignCourse(self):
        teacherID = int(input("Enter Teacher ID: "))
        courseId = int(input("Enter Course ID to assign: "))
        tId = next((tId for tId in  TeacherDetailsList if tId.TeacherID == teacherID), None)
        cId = next((cId for cId in CourseDetailsList if cId[0] == courseId), None)

        if tId and cId:
            if cId not in tId.courses:
                tId.courses.append(cId)
                print(f"Teacher {tId.firstName} {tId.lastName} has been assigned to {cId[1]} course.")
            else:
                print(f"Teacher {tId.firstName} {tId.lastName} is already assigned to {cId[1]} course.")
        else:
            print("Invalid Teacher ID or Course ID. Please try again.")



while True:
    print("\nStudent Management System")
    print("1. Add Student Details")
    print("2. Display Student Details")
    print("3. Display Course Details")
    print("4. Enroll in a Course")
    print("5. Add Teacher Details")
    print("6. Display Teacher Details")
    print("7. Assign Course to Teacher")
    print("8. Exit")

    choice = int(input("Enter your choice: "))

    match choice:
        case 1:
            n = int(input("Enter the number of students you want to add: "))
            for i in range(n):
                print(f"\nEnter Student Details {i+1}: ")
                student = StudentDetails(0, "", "", 0, "", "")
                student.getStudentDetails()
                StudentDetailsList.append(student)
            print("Student details added successfully.")

        case 2:

            searchStudentID = int(input("Enter Student ID to search: "))
            print(f"Student with ID {searchStudentID}:")
            student = next((s for s in StudentDetailsList if s.StudentID == searchStudentID), None)
            if student:
                student.displayStudentDetails()
            else:
                print("Student not found.")

        case 3:
            course = CourseDetails()
            print("Course details are as follows: ")
            course.displayCourseDetails()


        case 4:
            course = CourseDetails()
            course.EnrollCourse()

        case 5:

            n = int(input("Enter the number of teachers you want to add: "))
            for i in range(n):
                print(f"\nEnter Teacher Details {i+1}: ")
                teacher = TeacherDetails(0, "", "", 0, "", "", "")

                teacher.getTeacherDetails()
                TeacherDetailsList.append(teacher)
            print("Teacher details added successfully.")


        case 6:
            searchTeacherID = int(input("Enter Teacher ID to search: "))
            print(f"Teacher with ID {searchTeacherID}:")
            teacher = next((t for t in TeacherDetailsList if t.TeacherID == searchTeacherID), None)
            if teacher:
                teacher.displayTeacherDetails()
            else:
                print("Teacher not found.")


        case 7:
            teacher.assignCourse()

        case 8:
            print("Exiting the program. Goodbye!")
            break
        case _:
            print("Invalid choice. Please try again.")

