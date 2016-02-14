from StudentMaker import getStudents
import Scheduler
def main():

    students, course_obj_dict = getStudents(1000)
    print 'Created students'
    all_courses = course_obj_dict.values()

    tentSchedule = Scheduler.initializeSchedule(all_courses)
    count = 0
    for course in Scheduler.initialFinalsSchedule[0]:
        count += 1
        if count < 20:
            print course.course
        else:
            break
    print Scheduler.conflictsBySlot

main()