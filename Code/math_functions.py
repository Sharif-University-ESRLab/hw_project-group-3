def calc_sd(temps):
    n = len(temps)
    mean = sum(temps) / n
    deviations = [(x - mean) ** 2 for x in temps]

    return mean, deviations

def find_complement(l, sub_l):
    comp_l = []
    for item in l:
        if item not in sub_l:
            comp_l.append(item)

    return comp_l
