class Course:

    def __init__(self, data):
        self.department = data['department']
        self.course = data['class']
        self.semester = data['semester']
        self.title = data['title']
        self.students = []
        self.sections = []
        return self


class Section:

    def __init__(self, data):
        self.end = data['endtime']
        self.start = data['starttime']
        self.section = data['section']
        self.room = data['room']
        self.days = data['days']
        self.building = data['building']
        self.date = data['date']
        self.semester = data['semester']
        self.open = data['open']
        self.name = data['class']
        self.professor = data['professor']
        self.seats = data['seats']


class Student:

    def __init__(self, data):
        self.id = data['id']
        self.courses = data['courses']
        # Courses is a tuple (course, difficulty)
        self.preferences = data['preferences']
        # Preferences is an array of 5 elements
        # Elts 0:3 are integers representing importance
        # Elt 3 is array of tuples (slot #, importance)