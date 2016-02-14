from StudentMaker import getStudents
import ClassData
import Scheduler
import json
def main():

    students, course_obj_dict = getStudents(500)
    print 'Created students'
    all_courses = course_obj_dict.values()

    Scheduler.initializeSchedule(all_courses)
    tentSchedule = Scheduler.scheduler(10)

    for i in range(len(tentSchedule)):
        for j in range(len(tentSchedule[i])):
            tentSchedule[i][j] = tentSchedule[i][j].course

    output_dict = {'schedule': tentSchedule}
    output_dict['students'] = map(ClassData.Student.to_dict, students)

    json_obj = json.dumps(output_dict)
    with open('schedule.txt', 'w') as output:
        output.write(json_obj)
    output.close()

    print Scheduler.conflictsBySlot

main()