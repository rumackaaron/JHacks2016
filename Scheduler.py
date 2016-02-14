import ClassData

#conflictsBySlot represents the total number of existing conflicts per time slot. Ideally it would all be zeros.
conflictsBySlot = []
#initialFinalsSchedule represents a finals schedule which will minimize the number of student conflicts with
#multiple finals in the same time slot
initialFinalsSchedule = []
#numTimeSlots is the number of time slots in which finals are being offered
numTimeSlots = 20

#add a course to the schedule based on it's start time
def addByTime(crs):
    pass

#add a course to the schedule based on the minumul conflict slot
def addByConflict(crs):
    bestTimeSlot = 0
    numberOfConflicts = num_conflicts()
    for i in range(0,numTimeSlots):
        if crs.
        

#Add all classes with only one section to the finals schedule based on their starting time
#Then add all remaining classes to minimize conflicts
def initializeSchedule(oneSections,multiSections):
    for crsOne in oneSections:
        addByTime(crsOne)
    for crsMany in multiSections:
        addByConflict(crsMany)

#takes in a list of lists of courses. The index of the first list represents the time slot of the final. The list at index
#i contains all courses who's final will be given at index i
def scheduler(max_steps, finalsTime):
    #a marker for which time slot we want to minimize. After we minimize that slot go to the next slot that might have a conflict
    marker = 0
    for i in range(max_steps):
        #if there are no conflicts then we are done. Yay!
        if sum(conflictsBySlot) == 0:
            break
        else:
            #pick the first course in the list, and see if it should be moved. If yes then move it, put it at the end of that list
            #Otherwise put it at the end of the list
            curCourse = finalsTime[marker][0]
            #marker is gauranteed to be pointing to a slot which has at least two courses.
            curConflicts = num_conflicts(curCourse, finalsTime[marker][1])
            tmpTimeSlot = marker
            #go through first section, will go through second section later
            for j in range(0,marker):
                #if we found a better slot, put it there
                newConflicts = num_conflicts(curCourse,finalsTime[j])
                if newConflicts < curConflicts:
                    curConflicts = newConflicts
                    tmpTimeSlot = j
            #go through the second section
            for k in range(0,marker):
                #if we found a better slot, put it there
                newConflicts = num_conflicts(curCourse,finalsTime[k])
                if newConflicts < curConflicts:
                    curConflicts = newConflicts
                    tmpTimeSlot = k
            #if it shouldn't be moved, put it at the end
            if tmpTimeSlot == marker:
                finalsTime[marker].append(curCourse)
                finalsTime[marker].pop(0)
            #otherwise put it at the end of the better timeslot and update conflicts array
            else:
                finalsTime[tmpTimeSlot].append(curCourse)
                finalsTime[marker].pop(0)
                #check the old slot, which might have gone down or be zero
                if len(finalsTime[marker] > 1):
                    conflictsBySlot[marker] = num_conflicts(finalsTime[marker][0],finalsTime[marker][1:])
                else:
                    conflictsBySlot[marker] = 0
                #check the new slot, which might have gone up or stayed the same
                if len(finalsTime[tmpTimeSlot] > 1):
                    conflictsBySlot[tmpTimeSlot] = num_conflicts(finalsTime[marker][0],finalsTime[marker][1:])
            #move the marker to the next place that has a conflict
            marker = (marker + 1)%len(finalsTime)
            while len(courses[marker] <= 1):
                marker = (marker + 1)%len(finalsTime)
    
    return finalsTime
    
    
#takes as input the a list of courses and a course to add to that courselist. Returns the
#number of conflicts that list of courses would create if their finals were all offered at the same time.
def num_conflicts(course, courseList):
    numConflicts = 0
    #go though the courses in courseList and check for conflicts
    for crs in courseList:
        for stdnt in course.students:
            if stdnt in crs.students:
                numConflicts += 1
    return num_conflicts
    
#takes in a finals schedule and returns it in the format Aaron wants it
def postProcess(finalsSchedule):
    out = {}
    for i in range(len(finalsSchedule)):
        for crs in finalsSchedule[i]:
            out[crs.title] = i
    return out