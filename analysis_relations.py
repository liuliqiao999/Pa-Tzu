import rules
from itertools import combinations

pillars = ["year", "month", "day", "hour"]

def analyse_stem_combinations(four_pillars):
    # 分析天干五合, 返回：(柱位1, 柱位2, 合化五行)
    results = []
    for pillar_a, pillar_b in combinations(pillars, 2):
        stem_a = four_pillars[pillar_a][0]
        stem_b = four_pillars[pillar_b][0]
        if rules.stem_five_relation(stem_a, stem_b):
            element = rules.stem_five_element(stem_a, stem_b)
            results.append((pillar_a, pillar_b, element))
    return results

def analyse_branch_combinations(four_pillars):
    # 分析地支六合, 返回：(柱位1, 柱位2, 合化五行)
    results = []
    for pillar_a, pillar_b in combinations(pillars, 2):
        branch_a = four_pillars[pillar_a][1]
        branch_b = four_pillars[pillar_b][1]
        if rules.branch_six_combine_relation(branch_a, branch_b):
            element = rules.branch_six_combine_element(branch_a, branch_b)
            results.append((pillar_a, pillar_b, element))
    return results

def analyse_branch_clashes(four_pillars):
    # 分析地支六沖, 返回：(柱位1, 柱位2)
    results = []
    for pillar_a, pillar_b in combinations(pillars, 2):
        branch_a = four_pillars[pillar_a][1]
        branch_b = four_pillars[pillar_b][1]
        if rules.branch_six_clash_relation(branch_a, branch_b):
            results.append((pillar_a, pillar_b))
    return results

def analyse_branch_harms(four_pillars):
    # 分析地支六害, 返回：(柱位1, 柱位2)
    results = []
    for pillar_a, pillar_b in combinations(pillars, 2):
        branch_a = four_pillars[pillar_a][1]
        branch_b = four_pillars[pillar_b][1]
        if rules.branch_six_harm_relation(branch_a, branch_b):
            results.append((pillar_a, pillar_b))
    return results

def analyse_branch_breaks(four_pillars):
    # 分析地支六破, 返回：(柱位1, 柱位2)
    results = []
    for pillar_a, pillar_b in combinations(pillars, 2):
        branch_a = four_pillars[pillar_a][1]
        branch_b = four_pillars[pillar_b][1]
        if rules.branch_six_break_relation(branch_a, branch_b):
            results.append((pillar_a, pillar_b))
    return results

def analyse_branch_three_combinations(four_pillars):
    # 分析地支三合, 返回：(柱位1, 柱位2, 柱位3, 合化五行)
    results = []
    for pillar_a, pillar_b, pillar_c in combinations(pillars, 3):
        branch_a = four_pillars[pillar_a][1]
        branch_b = four_pillars[pillar_b][1]
        branch_c = four_pillars[pillar_c][1]
        if rules.branch_three_combine_relation(branch_a, branch_b, branch_c):
            element = rules.branch_three_combine_element(branch_a, branch_b, branch_c)
            results.append((pillar_a, pillar_b, pillar_c, element))
    return results

def analyse_branch_three_meetings(four_pillars):
    # 分析地支三會, 返回：(柱位1, 柱位2, 柱位3, 合化五行)
    results = []
    for pillar_a, pillar_b, pillar_c in combinations(pillars, 3):
        branch_a = four_pillars[pillar_a][1]
        branch_b = four_pillars[pillar_b][1]
        branch_c = four_pillars[pillar_c][1]
        if rules.branch_three_meeting_relation(branch_a, branch_b, branch_c):
            element = rules.branch_three_meeting_element(branch_a, branch_b, branch_c)
            results.append((pillar_a, pillar_b, pillar_c, element))
    return results

def analyse_branch_punishments(four_pillars):
    branches = [four_pillars[pillar][1] for pillar in pillars]
    punishments = rules.branch_punishment(branches)
    results = []
    for punishment in punishments:
        if punishment.endswith("自刑"):
            target = [punishment[0]] * 2
        else:
            target = list(punishment)
        for positions in combinations(pillars, len(target)):
            selected = [four_pillars[pillar][1] for pillar in positions]
            if sorted(selected) == sorted(target):
                results.append((*positions, punishment))
    return results


