import ClassData

# conflictsBySlot represents the total number of existing conflicts per time slot. Ideally it would all be zeros.
conflictsBySlot = [0 for _ in range(ClassData.FINAL_SLOTS)]
# initialFinalsSchedule represents a finals schedule which will minimize the number of student conflicts with
# multiple finals in the same time slot
initialFinalsSchedule = [[] for _ in range(ClassData.FINAL_SLOTS)]
# numTimeSlots is the number of time slots in which finals are being offered
numTimeSlots = ClassData.FINAL_SLOTS

# add a course to the schedule based on minimal conflict
#Complexity - O(l*n^2), where l is number of finals slots and n is number of students in the course
def addByConflict(crs):
    fewestConflicts = num_conflicts(crs, initialFinalsSchedule[0])
    bestTimeslot = 0
    for i in range(1,numTimeSlots):
        curConflicts = num_conflicts(crs,initialFinalsSchedule[i])
        if curConflicts < fewestConflicts:
            fewestConflicts = curConflicts
            bestTimeslot = i
    conflictsBySlot[bestTimeslot] += num_conflicts(crs, initialFinalsSchedule[bestTimeslot])
    initialFinalsSchedule[bestTimeslot].append(crs)

# add a course to the schedule based on the start time
#Complexity - O(1), but a very long O(1)
def addByTime(crs):
    days = crs.sections[0].days.lower()
    start_hour = crs.sections[0].start.split(':')[0]
    # if the class meets on a monday or wednesday or friday
    if 'm' in days or 'w' in days or 'f' in days:
        # if class is in the morning
        if 'am' in crs.sections[0].start:
            # if class is between midnight and 9
            if start_hour < 9:
                initialFinalsSchedule[0].append(crs)
            # if class is between 9 and 10
            elif start_hour < 10:
                initialFinalsSchedule[1].append(crs)
            # if class is between 10 and 11
            elif start_hour < 11:
                initialFinalsSchedule[2].append(crs)
            # if class is between 11 and noon
            else:
                initialFinalsSchedule[3].append(crs)
        # if the class is in the afternoon
        else:
            # if class is between noon and 1
            if start_hour > 11:
                initialFinalsSchedule[4].append(crs)
            # if class is between 1 and 2
            elif start_hour < 2:
                initialFinalsSchedule[5].append(crs)
            # if class is between 2 and 3
            elif start_hour < 3:
                initialFinalsSchedule[6].append(crs)
            # if class is between 3 and 4
            elif start_hour < 4:
                initialFinalsSchedule[7].append(crs)
            # if class is between 4 and 5
            elif start_hour < 5:
                initialFinalsSchedule[8].append(crs)
            # if class is after 5
            else:
                initialFinalsSchedule[9].append(crs)
    # else if the class meets on a tuesday or thursday
    elif 'u' in days or 'h' in days:
        # if class is in the morning
        if 'am' in crs.sections[0].start:
            # if class is between midnight and 9
            if start_hour < 9:
                initialFinalsSchedule[10].append(crs)
            # if class is between 9 and 10
            elif start_hour < 10:
                initialFinalsSchedule[11].append(crs)
            # if class is between 10 and 11
            elif start_hour < 11:
                initialFinalsSchedule[12].append(crs)
            # if class is between 11 and noon
            else:
                initialFinalsSchedule[13].append(crs)
        # if the class is in the afternoon
        else:
            # if class is between noon and 1
            if start_hour > 11:
                initialFinalsSchedule[14].append(crs)
            # if class is between 1 and 2
            elif start_hour < 2:
                initialFinalsSchedule[15].append(crs)
            # if class is between 2 and 3
            elif start_hour < 3:
                initialFinalsSchedule[16].append(crs)
            # if class is between 3 and 4
            elif start_hour < 4:
                initialFinalsSchedule[17].append(crs)
            # if class is between 4 and 5
            elif start_hour < 5:
                initialFinalsSchedule[18].append(crs)
            # if class is after 5
            else:
                initialFinalsSchedule[19].append(crs)

# Add all classes with only one section to the finals schedule based on their starting time
# Then add all remaining classes to minimize conflicts
#Complexity - O(c*n^2), where c is the number of courses, and n is the number of students in the course
def initializeSchedule(courseList):
    for crs in courseList:
        if len(crs.sections) == 1:
            addByTime(crs)
        elif len(crs.sections) > 1:
            addByConflict(crs)
    return initialFinalsSchedule

# takes in a list of lists of courses. The index of the first list represents the time slot of the final. The list at index
# i contains all courses who's final will be given at index i
#Complexity - O(n^2*s) where n is the number of students per course, and s is max_steps 
def scheduler(max_steps, finalsTime = None):
    if finalsTime is None:
        finalsTime = initialFinalsSchedule
    # a marker for which time slot we want to minimize. After we minimize that slot go to the next slot that might have a conflict
    marker = 0
    for i in range(max_steps):
        # if there are no conflicts then we are done. Yay!
        if sum(conflictsBySlot) == 0:
            break
        else:
            # pick the first course in the list, and see if it should be moved. If yes then move it, put it at the end of that list
            # Otherwise put it at the end of the list
            curCourse = finalsTime[marker][0]
            # marker is gauranteed to be pointing to a slot which has at least two courses.
            curConflicts = num_conflicts(curCourse, finalsTime[marker][1])
            tmpTimeSlot = marker
            # go through first section, will go through second section later
            for j in range(0,marker):
                # if we found a better slot, put it there
                newConflicts = num_conflicts(curCourse,finalsTime[j])
                if newConflicts < curConflicts:
                    curConflicts = newConflicts
                    tmpTimeSlot = j
            # go through the second section
            for k in range(0,marker):
                # if we found a better slot, put it there
                newConflicts = num_conflicts(curCourse,finalsTime[k])
                if newConflicts < curConflicts:
                    curConflicts = newConflicts
                    tmpTimeSlot = k
            # if it shouldn't be moved, put it at the end
            if tmpTimeSlot == marker:
                finalsTime[marker].append(curCourse)
                finalsTime[marker].pop(0)
            # otherwise put it at the end of the better timeslot and update conflicts array
            else:
                finalsTime[tmpTimeSlot].append(curCourse)
                finalsTime[marker].pop(0)
                # check the old slot, which might have gone down or be zero
                if len(finalsTime[marker]) > 1:
                    conflictsBySlot[marker] = num_conflicts(finalsTime[marker][0],finalsTime[marker][1:])
                else:
                    conflictsBySlot[marker] = 0
                # check the new slot, which might have gone up or stayed the same
                if len(finalsTime[tmpTimeSlot]) > 1:
                    conflictsBySlot[tmpTimeSlot] = num_conflicts(finalsTime[marker][0],finalsTime[marker][1:])
            # move the marker to the next place that has a conflict
            marker = (marker + 1)%len(finalsTime)
            while len(finalsTime[marker]) <= 1:
                marker = (marker + 1)%len(finalsTime)
    return finalsTime
    
    
# takes as input the a list of courses and a course to add to that courselist. Returns the
# number of conflicts that list of courses would create if their finals were all offered at the same time.
#Complexity - O(n^2) where n is number of students in course. Could be optimized if both were sorted or hashtable
def num_conflicts(course, courseList):
    numConflicts = 0
    # go though the courses in courseList and check for conflicts
    for crs in courseList:
        if len(course.students) < len(crs.students):
            for stdnt in course.students:
                if stdnt in crs.students:
                    numConflicts += 1
        else:
            for stdnt in crs.students:
                if stdnt in course.students:
                    numConflicts += 1
    return numConflicts
    
# takes in a finals schedule and returns it in the format Aaron wants it
#Complexity is O(c), where c is the number of courses
def postProcess(finalsSchedule):
    out = {}
    for i in range(len(finalsSchedule)):
        for crs in finalsSchedule[i]:
            out[crs] = i
    return out