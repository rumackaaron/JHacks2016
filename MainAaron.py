import StudentMaker
import ClassData
import Scheduler
import StudentScheduler
import json

def main():
    students, schedule = StudentMaker.schedule_from_file()
    schedule = Scheduler.postProcess(schedule)

    final_mapping = [4, 19, 12, 17, 0, 7, 1, 13, 8, 5, 10, 2, 11, 14, 9, 15, 16, 3, 18, 6]

    mapping = []
    for i in range(ClassData.FINAL_SLOTS):
        mapping.append(i)

    #print sum(StudentScheduler.scheduleBadness(students, schedule, mapping))

    #mapp = StudentScheduler.optimizeSchedule(students, schedule, 10)

    #print sum(StudentScheduler.scheduleBadness(students, schedule, mapp))

    id = 1463
    print len(students)


main()