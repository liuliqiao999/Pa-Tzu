import shensha_combined

def analyse_tin_se(four_pillars):
    month_branch = four_pillars["month"][1]
    day_stem = four_pillars["day"][0]
    day_branch = four_pillars["day"][1]
    return shensha_combined.Tin_Se(month_branch, day_stem, day_branch)


def analyse_sei_fai(four_pillars):
    month_branch = four_pillars["month"][1]
    day_stem = four_pillars["day"][0]
    day_branch = four_pillars["day"][1]
    return shensha_combined.Sei_Fai(month_branch, day_stem, day_branch)
