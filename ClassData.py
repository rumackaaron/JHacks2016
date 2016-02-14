class Course:

    def __init__(self, data):
        self.department = data['department']
        self.course = data['class']
        self.semester = data['semester']
        self.title = data['title']
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
        self.preferences = data['preferences']