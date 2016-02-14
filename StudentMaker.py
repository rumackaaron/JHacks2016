from ClassData import *
import urllib2
import json
import random

def getClasses():
    school = 'UMCP'
    url = 'http://hackathon.bookholders.com/classdata/v1/s16/' + school

    response = urllib2.urlopen(url)
    data = str(response.read())

    response_json = json.loads(data)

    def getDept(json_elt): return json_elt['department']
    depts = map(getDept, response_json)

    courses = []
    dict_out = {}
    count = 0
    for dept in depts:
        count += 1
        print '%d-%d' % (count, len(depts))
        base_url = 'http://hackathon.bookholders.com/classdata/v1/s16/%s/%s' % (school, dept)
        response = urllib2.urlopen(base_url)
        data = str(response.read())
        response_json = json.loads(data)

        for course_elt in response_json:
            course = Course(course_elt)
            courses.append(course)

            url = '%s/%s' % (base_url, course.course)
            response = urllib2.urlopen(url)
            data = str(response.read())
            response_json = json.loads(data)

            for elt in response_json:
                if 'starttime' in elt:
                    course.sections.append(Section(elt))

            dict_out[course.course] = {'course': course.course, 'sections': map(Section.to_dict, course.sections)}

        json_out = json.dumps(dict_out)
        with open('coursedata.txt', 'w') as output:
            output.write(json_out)
        output.close()

    courses_json_out = json.dumps(dict_out)

    with open('coursedata.txt', 'w') as output:
        output.write(courses_json_out)
    output.close()


def schedule_from_file():
    students = []
    schedule = []

    with open('schedule.txt', 'r') as inp2:
        data = json.load(inp2)
        for student_dict in data['students']:
            student = Student()
            student.set_vals(student_dict)
            students.append(student)

        schedule = data['schedule']
    inp2.close()

    return students, schedule


def getStudents(num):
    students = []
    courses = {}
    course_objs = {}

    with open('coursedata.txt', 'r') as inp:
        courses = json.load(inp)
    inp.close()

    course_names = courses.keys()
    course_names.sort()

    for name in course_names:
        course_objs[name] = Course({'class': name})

    for dicti in courses.values():
        for sect in dicti['sections']:
            course_objs[dicti['course']].sections.append(Section(sect))

    for n in range(num):
        student = Student()
        student.id = n

        schedule = []

        idxs = random.sample(range(len(course_names)), 3)
        idxs.append(idxs[0] - 1)
        idxs.append(idxs[0] - 2)
        idxs.append(idxs[1] - 1)
        idxs.append(idxs[2] - 1)

        num_classes = random.choice([4,5,5])
        attempt = 0

        while len(schedule) < num_classes and attempt < 7:
            if idxs[attempt] < 0:
                attempt += 1
                continue
            for sect in courses[course_names[idxs[attempt]]]['sections']:
                no_add = False
                for s in schedule:
                    if s.start.split(':')[0] == sect['starttime'].split(':')[0]:
                        no_add = True
                        break

                if not no_add:
                    schedule.append(Section(sect))
                    course_objs[sect['class']].students.append(n)

            attempt += 1

        def assign_diff(s): return s, random.choice(range(1, 6))
        schedule = map(assign_diff, schedule)
        student.courses = schedule

        conflicts = []
        population = range(0, 20)
        slots = random.sample(population, random.choice(range(0, 4)))
        for i in slots:
            conflict = (i, random.choice(range(1,6)))
            conflicts.append(conflict)

        preferences = [random.choice(range(-5,6)), random.choice(range(1,6)), random.choice(range(1,6)), conflicts]
        student.preferences = preferences

        students.append(student)

    return students, course_objs

schedule_from_file()