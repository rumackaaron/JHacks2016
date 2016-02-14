from ClassData import *
import urllib2
import json

def getClasses():
    school = 'UMCP'
    url = 'http://hackathon.bookholders.com/classdata/v1/s16/' + school

    response = urllib2.urlopen(url)
    data = str(response.read())

    response_json  = json.loads(data)

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

getClasses()

