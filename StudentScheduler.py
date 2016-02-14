from ClassData import FINAL_SLOTS

# Negative value means better to change in that direction
earlier = [0 for _ in range(FINAL_SLOTS)]  # in real
later = [0 for _ in range(FINAL_SLOTS)]  # in real
mapping = [0 for _ in range(FINAL_SLOTS)]  # idx to real
inverse = [0 for _ in range(FINAL_SLOTS)]  # real to idx


def studentBadness(student, schedule, mapping, acc):
    for course in student.courses:
        if course[0] not in schedule:
            continue
        slot = mapping[schedule[course[0]]]
        acc[slot] += student.preferences[0] * slot

        # Avoid slots
        for (bad_slot, importance) in student.preferences[3]:
            if bad_slot == slot:
                acc[slot] += importance

    # Spread out
    for i in range(len(student.courses)):
        course1, diff1 = student.courses[i]
        if course1 not in schedule:
            continue
        slot1 = mapping[schedule[course1]]
        for j in range(i + 1, len(student.courses)):
            course2, diff2 = student.courses[j]
            if course2 not in schedule:
                continue
            slot2 = mapping[schedule[course2]]

            dist = max(float(abs(slot1 - slot2)), 1.0)
            diffBadness = float(student.preferences[1]) * float(diff1 + diff2) / dist
            acc[slot1] += diffBadness / 2
            acc[slot2] += diffBadness / 2

            regBadness = float(student.preferences[2]) / dist

            acc[slot1] += regBadness / 2
            acc[slot2] += regBadness / 2
    return acc


def scheduleBadness(students, schedule, mapping):
    badness_slots = [0 for _ in range(FINAL_SLOTS)]
    for student in students:
        badness_slots = studentBadness(student, schedule, mapping, badness_slots)
    return badness_slots


def optimizeSchedule(students, schedule, max_steps, mapp = None):
    if max_steps == 0:
        return mapp

    if mapp is None:
        mapp = []
        for i in range(FINAL_SLOTS):
            mapp.append(i)

    for i in range(len(mapp)):
        inverse[mapp[i]] = i

    newMap = mapp

    badness_arr = scheduleBadness(students, schedule, mapp)
    badness = sum(badness_arr)

    worst_badness = max(badness_arr)
    worst_badness2 = 0
    worst_idx = 0
    worst_idx2 = 0

    for i in range(FINAL_SLOTS):
        if badness_arr[i] == worst_badness:
            worst_idx = i
        if badness_arr[i] > worst_badness2 and badness_arr[i] != worst_badness:
            worst_idx2 = i
            worst_badness2 = badness_arr[i]

    best_badness = badness
    best_map = list(newMap)

    '''for i in range(FINAL_SLOTS):
        temp = list(newMap)
        if i == worst_idx:
            continue

        orig = inverse[worst_idx]
        temp[i] = newMap[orig]
        temp[orig] = newMap[i]

        curr = sum(scheduleBadness(students, schedule, temp))
        if curr < best_badness:
            best_badness = curr
            best_map = list(temp)'''

    for i in range(FINAL_SLOTS):
        for j in range(FINAL_SLOTS):
            temp = list(newMap)
            if i == j:
                continue

            orig = inverse[j]
            temp[i] = newMap[orig]
            temp[orig] = newMap[i]

            curr = sum(scheduleBadness(students, schedule, temp))
            if curr < best_badness:
                best_badness = curr
                best_map = list(temp)

    if best_badness < badness:
        print badness
        print best_map
        return optimizeSchedule(students, schedule, max_steps - 1, best_map)
    else:
        return best_map