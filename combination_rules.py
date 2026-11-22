import constant
import rules
import analysis_five_elements
import analysis_relations
from itertools import combinations

pillars = ["year", "month", "day", "hour"]

# 判斷天干五合的柱位距離 0 = 緊貼合, 1 = 隔一柱, 2 = 隔兩柱
def combination_stem_distance(pillar_a, pillar_b):
    index_a = pillars.index(pillar_a)
    index_b = pillars.index(pillar_b)
    return abs(index_a - index_b) - 1


# 地支合局的預設優先級, 三會 > 三合 > 六合 僅用於重疊合局的排序，不代表必然合化成功
def combination_branch_priority(combination_type):
    priorities = {"地支三會": 3, "地支三合": 2, "地支六合": 1}
    return priorities.get(combination_type, 0)


# 綜合評估化神條件
def combination_condition_status(seasonal_state, exposed, rooted, obstructed):
    if seasonal_state in ["旺", "相"] and (exposed or rooted) and not obstructed:
        return 1 #"條件較充分"
    if seasonal_state in ["死", "囚"] and not exposed and not rooted:
        return -1 #"條件不足"
    return 0 #"有待判定"

# 判斷化神五行在月令中的旺相休囚死
def combination_seasonal_state(four_pillars, element):
    month_branch = four_pillars["month"][1]
    month_element = constant.branches_elements(month_branch)
    relation = rules.element_relation(element, month_element)
    relation_state_index = [0, 3, 4, 2, 1]
    return constant.seasonal_states[relation_state_index[relation + 2]]

# 天干五合的化神透干判斷
# 逐組檢查五合, 判斷化神五行是否在其他天干透出, 排除參與五合的兩個天干, 避免將合干本身視為額外透干
def combination_stem_five_exposed(four_pillars):
    results = []
    for pillar_a, pillar_b in combinations(pillars, 2):
        stem_a = four_pillars[pillar_a][0]
        stem_b = four_pillars[pillar_b][0]
        if not rules.stem_five_relation(stem_a, stem_b):
            continue
        element = rules.stem_five_element(stem_a, stem_b)
        exposed = False
        for pillar in pillars:
            if pillar in [pillar_a, pillar_b]:
                continue
            stem = four_pillars[pillar][0]
            if constant.stems_elements(stem) == element:
                exposed = True
                break
        results.append((pillar_a, pillar_b, element, exposed)) #(柱位1, 柱位2, 化神五行, 是否透干)
    return results


# 天干五合的化神通根判斷, 判斷化神五行是否在四柱地支藏干中出現
def combination_stem_five_rooted(four_pillars):
    results = []
    for pillar_a, pillar_b, element in analysis_relations.analyse_stem_combinations(four_pillars):
        rooted = False
        for pillar in ["year", "month", "day", "hour"]:
            branch = four_pillars[pillar][1]
            for hidden_stem in constant.hidden_stems(branch):
                if constant.stems_elements(hidden_stem) == element:
                    rooted = True
                    break
            if rooted:
                break
        results.append((pillar_a, pillar_b, element, rooted))
    return results


# 天干五合的化神受剋判斷, 排除參與五合的兩個天干, 檢查其餘天干是否剋制化神
def combination_stem_five_restrained(four_pillars):
    results = []
    for pillar_a, pillar_b, element in analysis_relations.analyse_stem_combinations(four_pillars):
        restrained = False
        for pillar in ["year", "month", "day", "hour"]:
            if pillar in [pillar_a, pillar_b]:
                continue
            stem = four_pillars[pillar][0]
            stem_element = constant.stems_elements(stem)
            if constant.element_consume(stem_element) == element:
                restrained = True
                break
        results.append((pillar_a, pillar_b, element, restrained))
    return results


# 判斷地支合局是否受到其他地支六沖, 返回是否存在外部地支沖擊合局
def combination_branch_clashed(four_pillars, combined_pillars): # combined_pillars：參與合局的柱位
    for pillar in combined_pillars:
        branch = four_pillars[pillar][1]
        for other_pillar in ["year", "month", "day", "hour"]:
            if other_pillar in combined_pillars:
                continue
            other_branch = four_pillars[other_pillar][1]
            if rules.branch_six_clash_relation(branch, other_branch):
                return True
    return False


# 判斷地支合局的化神是否透干
def combination_branch_exposed(four_pillars, element):
    for pillar in pillars:
        stem = four_pillars[pillar][0]
        if constant.stems_elements(stem) == element:
            return True
    return False


# 判斷指定化神五行是否在四柱地支藏干中通根
def combination_element_rooted(four_pillars, element):
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        for hidden_stem in constant.hidden_stems(branch):
            if constant.stems_elements(hidden_stem) == element:
                return True
    return False

# 地支合局的化神條件, 適用於六合、三合、三會
def combination_branch_conditions(four_pillars, combined_pillars, element):
    season = combination_seasonal_state(four_pillars, element)
    exposed = combination_branch_exposed(four_pillars, element)
    rooted = combination_element_rooted(four_pillars, element)
    clashed = combination_branch_clashed(four_pillars, combined_pillars)
    return {
        "月令": season,
        "透干": exposed,
        "通根": rooted,
        "受沖": clashed
    }# 返回：月令狀態、是否透干、是否通根、是否受外部六沖

# 天干五合的化神條件
# 返回每組五合的月令、透干、通根、受剋情況
def combination_stem_conditions(four_pillars):
    results = []
    exposed_results = combination_stem_five_exposed(four_pillars)
    rooted_results = combination_stem_five_rooted(four_pillars)
    restrained_results = combination_stem_five_restrained(four_pillars)
    for i, (pillar_a, pillar_b, element, exposed) in enumerate(exposed_results):
        results.append({
            "柱位": (pillar_a, pillar_b),
            "化神": element,
            "月令": combination_seasonal_state(four_pillars, element),
            "透干": exposed,
            "通根": rooted_results[i][3],
            "受剋": restrained_results[i][3]
        })
    return results
