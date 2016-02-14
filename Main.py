import StudentMaker
import ClassData
import Scheduler
import json


def main():
    students, schedule = StudentMaker.schedule_from_file()
    schedule = Scheduler.postProcess(schedule)

    print schedule['AASP101']

main()