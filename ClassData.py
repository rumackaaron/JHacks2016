FINAL_SLOTS = 20

class Course:

    def __init__(self, data):
        self.course = data['class']
        self.students = []
        self.sections = []


class Section:

    def __init__(self, data):
        self.end = data['endtime']
        self.start = data['starttime']
        self.section = data['section']
        self.days = data['days']
        self.name = data['class']

    def to_dict(self):
        return {'endtime': self.end, 'starttime': self.start, 'section': self.section
                , 'days': self.days, 'class': self.name}


class Student:

    def __init__(self, data):
        self.id = data['id']
        self.courses = data['courses']
        # Courses is a tuple (course, difficulty)
        self.preferences = data['preferences']
        # Preferences is an array of 5 elements
        # Elts 0:3 are integers representing importance
        # Elt 3 is array of tuples (slot #, importance)