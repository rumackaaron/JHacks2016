from ClassData import FINAL_SLOTS

# Negative value means better to change in that direction
earlier = []  # in real
later = []  # in real
mapping = [0 for _ in range(FINAL_SLOTS)]  # idx to real
inverse = [0 for _ in range(FINAL_SLOTS)]  # real to idx


def studentBadness(student, schedule, mapping):
    # TODO: Weight the four difference badness components equally
    badness = 0
    for course in student.courses:
        slot = mapping[schedule[course.name]]
        # Earlier/Later
        badness += student.preferences[0] * slot
        earlier[slot] -= student.preferences[0]
        later[slot] += student.preferences[0]

        # Avoid slots
        for (bad_slot, importance) in student.preferences[3]:
            if bad_slot == slot:
                badness += importance
            if bad_slot == slot - 1:
                earlier[slot] += importance
            if bad_slot == slot + 1:
                later[slot] += importance

    # Spread out
    for i in range(len(student.courses)):
        course1, diff1 = student.courses[i]
        slot1 = mapping[schedule[course1.name]]
        for j in range(i + 1, len(student.courses)):
            course2, diff2 = student.courses[j]
            slot2 = mapping[schedule[course2.name]]

            dist = max(float(abs(slot1 - slot2)), 1.0)
            diffBadness = float(student.preferences[1]) * float(diff1 + diff2) / dist
            badness += diffBadness
            diste1 = max(float(abs(slot1 - 1 - slot2)), 1.0)
            distl1 = max(float(abs(slot1 + 1 - slot2)), 1.0)
            e1l2 = (diffBadness * dist) / diste1
            e2l1 = (diffBadness * dist) / distl1

            earlier[slot1] += e1l2 - diffBadness
            later[slot1] += e2l1 - diffBadness
            earlier[slot2] += e2l1 - diffBadness
            later[slot2] += e1l2 - diffBadness

            regBadness = float(student.preferences[2]) / dist
            e1l2 = (regBadness * dist) / diste1
            e2l1 = (regBadness * dist) / distl1

            earlier[slot1] += diffBadness - e1l2
            later[slot1] += diffBadness - e2l1
            earlier[slot2] += diffBadness - e2l1
            later[slot2] += diffBadness - e1l2

            badness += regBadness

    return badness


def scheduleBadness(students, schedule, mapping):
    badness = 0
    for student in students:
        badness += studentBadness(student, schedule, mapping)
    return badness


def optimizeSchedule(students, schedule, mapp = None, prevBad = 2 ** 50, goodMap = None):
    if mapp is None:
        mapping = []
        for i in range(FINAL_SLOTS):
            mapping[i] = i
    else:
        mapping = map

    for i in range(len(mapping)):
        inverse[mapping[i]] = i

    earlier = [0 for _ in range(FINAL_SLOTS)]
    later = [0 for _ in range(FINAL_SLOTS)]
    newMap = mapp

    badness = scheduleBadness(students, schedule, mapping)
    curr = 1
    prev = 0
    change = False
    while curr < FINAL_SLOTS:
        if earlier[curr] + later[prev] > 0:
            # Swap
            newMap[inverse[curr]] -= 1
            newMap[inverse[prev]] += 1
            curr += 2
            prev += 2
            change = True
        else:
            curr += 1
            prev += 1

    if badness < prevBad:
        return optimizeSchedule(students, schedule, newMap, badness)
    elif change:
        return optimizeSchedule(students, schedule, newMap, prevBad, mapp)
    elif goodMap is None:
        return mapp
    else:
        return goodMap