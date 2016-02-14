import StudentMaker
import ClassData
import Scheduler
import StudentScheduler


def main():
    students, schedule = StudentMaker.schedule_from_file()
    schedule = Scheduler.postProcess(schedule)

    mapping = []
    for i in range(ClassData.FINAL_SLOTS):
        mapping.append(i)

    print sum(StudentScheduler.scheduleBadness(students, schedule, mapping))

    mapp = StudentScheduler.optimizeSchedule(students, schedule, 10)

    print sum(StudentScheduler.scheduleBadness(students, schedule, mapp))


main()