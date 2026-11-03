import annual_rules
import rules
import constant
import analysis_five_elements

# 流年天干五行關係
def annual_stem_element_relation(four_pillars, solar_date):
    day_stem = four_pillars["day"][0]
    annual_stem = annual_rules.annual_pillar(solar_date)[0]
    return rules.stem_element_relation(day_stem, annual_stem)

# 流年地支五行關係
def annual_branch_element_relation(four_pillars, solar_date):
    day_stem = four_pillars["day"][0]
    annual_branch = annual_rules.annual_pillar(solar_date)[1]
    day_element = constant.stems_elements(day_stem)
    branch_element = constant.branches_elements(annual_branch)
    return rules.element_relation(day_element, branch_element)

# 流年天干喜忌
def annual_stem_favourability(four_pillars, solar_date):
    relation = annual_stem_element_relation(four_pillars, solar_date)
    favourable = analysis_five_elements.favourable_relations(four_pillars)
    if not favourable:
        return None
    action = constant.five_element_actions[relation + 2]
    return action in favourable


# 流年地支喜忌
def annual_branch_favourability(four_pillars, solar_date):
    relation = annual_branch_element_relation(four_pillars, solar_date)
    favourable = analysis_five_elements.favourable_relations(four_pillars)
    if not favourable:
        return None
    action = constant.five_element_actions[relation + 2]
    return action in favourable

# 流年地支藏干喜忌
def annual_hidden_stems_favourability(four_pillars, solar_date):
    annual_branch = annual_rules.annual_pillar(solar_date)[1]
    hidden_stems = constant.hidden_stems(annual_branch)
    day_stem = four_pillars["day"][0]
    favourable = analysis_five_elements.favourable_relations(four_pillars)
    results = []
    for stem in hidden_stems:
        relation = rules.stem_element_relation(day_stem, stem)
        action = constant.five_element_actions[relation + 2]
        if not favourable:
            results.append(None)
        else:
            results.append(action in favourable)
    return results

# 流年五行喜忌加權統計
def annual_favourability_summary(four_pillars, solar_date):
    stem = annual_stem_favourability(four_pillars, solar_date)
    hidden = annual_hidden_stems_favourability(four_pillars, solar_date)
    results = [stem] + hidden
    weights = [3] + [3, 2, 1][:len(hidden)]
    summary = [0, 0, 0]  # [喜, 忌, 未定]
    for result, weight in zip(results, weights):
        if result is True:
            summary[0] += weight
        elif result is False:
            summary[1] += weight
        else:
            summary[2] += weight
    return summary


# 流年與原局的干支關係
def annual_interactions(four_pillars, solar_date):
    return {
        "天干五合": annual_rules.annual_stem_five_relations(four_pillars, solar_date),
        "地支六沖": annual_rules.annual_branch_six_clash(four_pillars, solar_date),
        "地支六合": annual_rules.annual_branch_six_combine(four_pillars, solar_date),
        "地支六害": annual_rules.annual_branch_six_harm(four_pillars, solar_date),
        "地支六破": annual_rules.annual_branch_six_break(four_pillars, solar_date),
        "地支三合": annual_rules.annual_branch_three_combine(four_pillars, solar_date),
        "地支三會": annual_rules.annual_branch_three_meeting(four_pillars, solar_date),
        "地支相刑": annual_rules.annual_branch_punishment(four_pillars, solar_date),
        "地支半合": annual_rules.annual_branch_half_combine(four_pillars, solar_date),
        "地支半會": annual_rules.annual_branch_half_meeting(four_pillars, solar_date),
    }

# 流年三合局五行
def annual_three_combine_element(four_pillars, solar_date):
    annual_branch = annual_rules.annual_pillar(solar_date)[1]
    combinations_found = annual_rules.annual_branch_three_combine(four_pillars, solar_date)
    results = []
    for pillar_a, pillar_b in combinations_found:
        branch_a = four_pillars[pillar_a][1]
        branch_b = four_pillars[pillar_b][1]
        element = rules.branch_three_combine_element(annual_branch, branch_a, branch_b)
        if element not in results:
            results.append(element)
    return results

# 流年三會局五行
def annual_three_meeting_element(four_pillars, solar_date):
    annual_branch = annual_rules.annual_pillar(solar_date)[1]
    combinations_found = annual_rules.annual_branch_three_meeting(four_pillars, solar_date)
    results = []
    for pillar_a, pillar_b in combinations_found:
        branch_a = four_pillars[pillar_a][1]
        branch_b = four_pillars[pillar_b][1]
        element = rules.branch_three_meeting_element(annual_branch, branch_a, branch_b)
        if element not in results:
            results.append(element)
    return results

# 流年三合局的喜忌判斷
def annual_three_combine_favourability(four_pillars, solar_date):
    three_combine_elements = annual_three_combine_element(four_pillars, solar_date)
    if not three_combine_elements:
        return []
    favourable = analysis_five_elements.favourable_relations(four_pillars)
    if not favourable:
        return [None] 
    day_stem = four_pillars["day"][0]
    day_element = constant.stems_elements(day_stem)
    results = []
    for element in three_combine_elements:
        relation = rules.element_relation(day_element, element)
        action = constant.five_element_actions[relation + 2]
        results.append(action in favourable)
    return results

# 流年三會局的喜忌判斷
def annual_three_meeting_favourability(four_pillars, solar_date):
    three_meeting_elements = annual_three_meeting_element(four_pillars, solar_date)
    if not three_meeting_elements:
        return []
    favourable = analysis_five_elements.favourable_relations(four_pillars)
    if not favourable:
        return [None]
    day_stem = four_pillars["day"][0]
    day_element = constant.stems_elements(day_stem)
    results = []
    for element in three_meeting_elements:
        relation = rules.element_relation(day_element, element)
        action = constant.five_element_actions[relation + 2]
        results.append(action in favourable)
    return results

# 流年天干五合所對應的五行
def annual_stem_five_element(four_pillars, solar_date):
    annual_stem = annual_rules.annual_pillar(solar_date)[0]
    combined_pillars = annual_rules.annual_stem_five_relations(four_pillars, solar_date)
    results = []
    for pillar in combined_pillars:
        stem = four_pillars[pillar][0]
        element = rules.stem_five_element(stem, annual_stem)
        if element not in results:
            results.append(element)
    return results

# 流年地支六合所對應的五行
def annual_branch_six_combine_element(four_pillars, solar_date):
    annual_branch = annual_rules.annual_pillar(solar_date)[1]
    combinations_found = annual_rules.annual_branch_six_combine(four_pillars, solar_date)
    results = []
    for pillar in combinations_found:
        branch = four_pillars[pillar][1]
        element = rules.branch_six_combine_element(annual_branch, branch)
        if element not in results:
            results.append(element)
    return results

# 流年天干五合的喜忌判斷
def annual_stem_five_favourability(four_pillars, solar_date):
    five_element = annual_stem_five_element(four_pillars, solar_date)
    if not five_element:
        return []
    favourable = analysis_five_elements.favourable_relations(four_pillars)
    if not favourable:
        return [None]
    day_stem = four_pillars["day"][0]
    day_element = constant.stems_elements(day_stem)
    results = []
    for element in five_element:
        relation = rules.element_relation(day_element, element)
        action = constant.five_element_actions[relation + 2]
        results.append(action in favourable)
    return results

# 流年地支六合喜忌
def annual_branch_six_combine_favourability(four_pillars, solar_date):
    six_combine_elements = annual_branch_six_combine_element(four_pillars, solar_date)
    if not six_combine_elements:
        return []
    favourable = analysis_five_elements.favourable_relations(four_pillars)
    if not favourable:
        return [None]
    day_stem = four_pillars["day"][0]
    day_element = constant.stems_elements(day_stem)
    results = []
    for element in six_combine_elements:
        relation = rules.element_relation(day_element, element)
        action = constant.five_element_actions[relation + 2]
        results.append(action in favourable)
    return results

# 整合流年神煞
def annual_shensha_summary(four_pillars, solar_date):
    return {
        "三合神煞": annual_rules.annual_three_combine_shensha(four_pillars, solar_date),
        "年支神煞": annual_rules.annual_year_shensha(four_pillars, solar_date),
        "月支神煞": annual_rules.annual_month_shensha(four_pillars, solar_date),
        "日干神煞": annual_rules.annual_stem_shensha(four_pillars, solar_date),
        "日柱神煞": annual_rules.annual_day_shensha(four_pillars, solar_date)
    }

# 整合流年基礎分析
def annual_basic_analysis(four_pillars, solar_date):
    return {
        "流年干支": annual_rules.annual_pillar(solar_date),
        "流年天干十神": annual_rules.annual_stem_ten_god(four_pillars, solar_date),
        "流年藏干十神": annual_rules.annual_hidden_ten_gods(four_pillars, solar_date),
        "流年天干喜忌": annual_stem_favourability(four_pillars, solar_date),
        "流年地支喜忌": annual_branch_favourability(four_pillars, solar_date),
        "流年藏干喜忌": annual_hidden_stems_favourability(four_pillars, solar_date),
        "流年喜忌加權": annual_favourability_summary(four_pillars, solar_date),
        "刑沖合害": annual_interactions(four_pillars, solar_date),
        "天干五合五行": annual_stem_five_element(four_pillars, solar_date),
        "天干五合喜忌": annual_stem_five_favourability(four_pillars, solar_date),
        "地支六合五行": annual_branch_six_combine_element(four_pillars, solar_date),
        "地支六合喜忌": annual_branch_six_combine_favourability(four_pillars, solar_date),
        "地支三合五行": annual_three_combine_element(four_pillars, solar_date),
        "地支三合喜忌": annual_three_combine_favourability(four_pillars, solar_date),
        "地支三會五行": annual_three_meeting_element(four_pillars, solar_date),
        "地支三會喜忌": annual_three_meeting_favourability(four_pillars, solar_date),
        "流年神煞": annual_shensha_summary(four_pillars, solar_date)
    }

import datetime
import pprint

x_pillars = {
    "year": ("癸", "未"),
    "month": ("乙", "丑"),
    "day": ("庚", "寅"),
    "hour": ("壬", "午")
}
test_date = datetime.date(2026, 6, 1)
result = annual_basic_analysis(x_pillars, test_date)
pprint.pp(result, sort_dicts=False)