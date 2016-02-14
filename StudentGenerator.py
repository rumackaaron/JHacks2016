import ClassData
import random
import urllib2
import json

list_of_preferences = ['Time of tests', 'Spread out harder tests', 'Spread out all tests', 'Avoid certain slots']
#preferences[0] will be number -5 (early tests) to 5 (later tests)
#preferences[1:3] will be number 1 to 5
#preferences[3] will be an array of tuples - (slot number, importance)


def StudentGenerator(n):
    """Creates n number of students"""
    students = []
    sectionsandcourses = SectionList()
    print 'Starting loop'
    for x in range(n):
        print 'In loop'
        studentid = x
        sections = random.sample(sectionsandcourses[0].values(), random.choice([4,5]))
        slot_conflict = SlotConflict()
        preferences = [random.choice(range(-5, 6)), random.choice(range(1,6)), random.choice(range(1,6)), slot_conflict]
        data = {'id':studentid, 'courses':sections, 'preferences':preferences}
        student = ClassData.Student(data)
        students.append(student)
        courses = sectionsandcourses[1]
        for section in sections:
            courses[section.name].students.append(student)
    return students

def SlotConflict():
    #use random.sample
    conflicts = []
    population = range(1,21)
    slots = random.sample(population, random.choice(range(1,4)))
    for i in slots:
        conflict = (i, random.choice(range(1,6)))
        conflicts.append(conflict)
    return conflicts

def SectionList():
    school = 'UMCP'
    
    url = "http://hackathon.bookholders.com/classdata/v1/s16/"+school
    response = urllib2.urlopen(url)
    data = response.read()
    
    response_json = json.loads(data)
    
    departments = []
    for each_department in response_json:
        departments.append(each_department["department"])
    
    for department in departments:
        url = "http://hackathon.bookholders.com/classdata/v1/s16/"+school+'/'+department
        response = urllib2.urlopen(url)
        data = response.read()
    
        response_json = json.loads(data)
        
        classes = []
        courses = {}
        for each_class in response_json:
            course = ClassData.Course(each_class)
            courses[course.course] = course
            classes.append(each_class["class"])
            
        for each_class in classes:
            url = "http://hackathon.bookholders.com/classdata/v1/s16/"+school+'/'+department+'/'+each_class
            response = urllib2.urlopen(url)
            data = response.read()
        
            response_json = json.loads(data)
            if type(response_json) == list:
                sections = {}
                for each_section in response_json:
                    section = ClassData.Section(each_section)
                    sections[section.name+section.section] = section
                    courses[section.name].sections.append(section)
    return (sections, courses)
        
if __name__ == '__main__':
    list_of_students = StudentGenerator(5)
    print list_of_students[0].courses
                    
                    
                
                
    
    



