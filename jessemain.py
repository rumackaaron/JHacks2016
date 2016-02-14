from StudentMaker import getStudents
import Scheduler
import time
def main():
    
    start = time.time()
    students, course_obj_dict = getStudents(4000)
    print 'Created students'
    
    all_courses = course_obj_dict.values()

    initialThingy = Scheduler.initializeSchedule(all_courses)
    print 'initialized schedule'
    
    tentSchedule = Scheduler.scheduler(1000, initialThingy)
    print 'minimized conflicts in schedule'
    
    postSchedule = Scheduler.postProcess(tentSchedule)
    end = time.time()
    print 'output schedule for preference maximization'

    print Scheduler.conflictsBySlot

    print end-start

main()