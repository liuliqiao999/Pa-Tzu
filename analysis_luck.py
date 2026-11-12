import rules
import constant
import analysis_five_elements
import luck_rules

# 大運天干五行關係
def luck_stem_element_relation(four_pillars, luck_pillar):
    day_stem = four_pillars["day"][0]
    luck_stem = luck_pillar[0]
    return rules.stem_element_relation(day_stem, luck_stem)

# 大運地支五行關係
def luck_branch_element_relation(four_pillars, luck_pillar):
    day_stem = four_pillars["day"][0]
    luck_branch = luck_pillar[1]
    element1, element2 = constant.stems_elements(day_stem), constant.branches_elements(luck_branch)
    return rules.element_relation(element1, element2)

# 大運天干喜忌
def luck_stem_favourability(four_pillars, luck_pillar):
    relation = luck_stem_element_relation(four_pillars, luck_pillar)
    favourable = analysis_five_elements.favourable_relations(four_pillars)
    if not favourable:
        return None
    action = constant.five_element_actions[relation + 2]
    return action in favourable

# 大運地支喜忌
def luck_branch_favourability(four_pillars, luck_pillar):
    relation = luck_branch_element_relation(four_pillars, luck_pillar)
    favourable = analysis_five_elements.favourable_relations(four_pillars)
    if not favourable:
        return None
    action = constant.five_element_actions[relation + 2]
    return action in favourable

# 大運地支藏干喜忌
def luck_hidden_stems_favourability(four_pillars, luck_pillar):
    luck_branch = luck_pillar[1]
    hidden_stems = constant.hidden_stems(luck_branch)
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

# 大運五行喜忌加權統計
def luck_favourability_summary(four_pillars, luck_pillar):
    stem = luck_stem_favourability(four_pillars, luck_pillar)
    hidden = luck_hidden_stems_favourability(four_pillars, luck_pillar)
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

# 大運與原局的干支關係
def luck_interactions(four_pillars, luck_pillar):
    return {
        "天干五合": luck_rules.luck_stem_five_relations(four_pillars, luck_pillar),
        "地支六沖": luck_rules.luck_branch_six_clash(four_pillars, luck_pillar),
        "地支六合": luck_rules.luck_branch_six_combine(four_pillars, luck_pillar),
        "地支六害": luck_rules.luck_branch_six_harm(four_pillars, luck_pillar),
        "地支六破": luck_rules.luck_branch_six_break(four_pillars, luck_pillar),
        "地支三合": luck_rules.luck_branch_three_combine(four_pillars, luck_pillar),
        "地支三會": luck_rules.luck_branch_three_meeting(four_pillars, luck_pillar),
        "地支相刑": luck_rules.luck_branch_punishment(four_pillars, luck_pillar),
        "地支半合": luck_rules.luck_branch_half_combine(four_pillars, luck_pillar),
        "地支半會": luck_rules.luck_branch_half_meeting(four_pillars, luck_pillar),
    }

# 大運三合局五行
def luck_three_combine_element(four_pillars, luck_pillar):
    luck_branch = luck_pillar[1]
    combinations_found = luck_rules.luck_branch_three_combine(four_pillars, luck_pillar)
    results = []
    for pillar_a, pillar_b in combinations_found:
        branch_a = four_pillars[pillar_a][1]
        branch_b = four_pillars[pillar_b][1]
        element = rules.branch_three_combine_element(luck_branch, branch_a, branch_b)
        if element not in results:
            results.append(element)
    return results

# 大運三會局五行
def luck_three_meeting_element(four_pillars, luck_pillar):
    luck_branch = luck_pillar[1]
    combinations_found = luck_rules.luck_branch_three_meeting(four_pillars, luck_pillar)
    results = []
    for pillar_a, pillar_b in combinations_found:
        branch_a = four_pillars[pillar_a][1]
        branch_b = four_pillars[pillar_b][1]
        element = rules.branch_three_meeting_element(luck_branch, branch_a, branch_b)
        if element not in results:
            results.append(element)
    return results

# 大運三合局的喜忌判斷
def luck_three_combine_favourability(four_pillars, luck_pillar):
    three_combine_elements = luck_three_combine_element(four_pillars, luck_pillar)
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

# 大運三會局的喜忌判斷
def luck_three_meeting_favourability(four_pillars, luck_pillar):
    three_meeting_elements = luck_three_meeting_element(four_pillars, luck_pillar)
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

# 大運天干五合所對應的五行
def luck_stem_five_element(four_pillars, luck_pillar):
    luck_stem = luck_pillar[0]
    combined_pillars = luck_rules.luck_stem_five_relations(four_pillars, luck_pillar)
    results = []
    for pillar in combined_pillars:
        stem = four_pillars[pillar][0]
        element = rules.stem_five_element(stem, luck_stem)
        if element not in results:
            results.append(element)
    return results

# 大運地支六合所對應的五行
def luck_branch_six_combine_element(four_pillars, luck_pillar):
    luck_branch = luck_pillar[1]
    combinations_found = luck_rules.luck_branch_six_combine(four_pillars, luck_pillar)
    results = []
    for pillar in combinations_found:
        branch = four_pillars[pillar][1]
        element = rules.branch_six_combine_element(luck_branch, branch)
        if element not in results:
            results.append(element)
    return results

# 大運天干五合的喜忌判斷
def luck_stem_five_favourability(four_pillars, luck_pillar):
    five_element = luck_stem_five_element(four_pillars, luck_pillar)
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

# 大運地支六合喜忌
def luck_branch_six_combine_favourability(four_pillars, luck_pillar):
    six_combine_elements = luck_branch_six_combine_element(four_pillars, luck_pillar)
    if not six_combine_elements:
        return []
    favourable = analysis_five_elements.favourable_relations(four_pillars)
    if not favourable:
        return [None] * len(six_combine_elements)
    day_stem = four_pillars["day"][0]
    day_element = constant.stems_elements(day_stem)
    results = []
    for element in six_combine_elements:
        relation = rules.element_relation(day_element, element)
        action = constant.five_element_actions[relation + 2]
        results.append(action in favourable)
    return results

# 整合大運神煞
def luck_shensha_summary(four_pillars, luck_pillar):
    return {
        "三合神煞": luck_rules.luck_three_combine_shensha(four_pillars, luck_pillar),
        "年支神煞": luck_rules.luck_year_shensha(four_pillars, luck_pillar),
        "月支神煞": luck_rules.luck_month_shensha(four_pillars, luck_pillar),
        "日干神煞": luck_rules.luck_stem_shensha(four_pillars, luck_pillar),
        "日柱神煞": luck_rules.luck_day_shensha(four_pillars, luck_pillar)
    }

# 整合大運基礎分析
def luck_basic_analysis(four_pillars, luck_pillar):
    return {
        "大運干支": luck_pillar,
        "大運天干十神": luck_rules.luck_stem_ten_god(four_pillars, luck_pillar),
        "大運藏干十神": luck_rules.luck_hidden_ten_gods(four_pillars, luck_pillar),
        "大運天干喜忌": luck_stem_favourability(four_pillars, luck_pillar),
        "大運地支喜忌": luck_branch_favourability(four_pillars, luck_pillar),
        "大運藏干喜忌": luck_hidden_stems_favourability(four_pillars, luck_pillar),
        "大運喜忌加權": luck_favourability_summary(four_pillars, luck_pillar),
        "刑沖合害": luck_interactions(four_pillars, luck_pillar),
        "天干五合五行": luck_stem_five_element(four_pillars, luck_pillar),
        "天干五合喜忌": luck_stem_five_favourability(four_pillars, luck_pillar),
        "地支六合五行": luck_branch_six_combine_element(four_pillars, luck_pillar),
        "地支六合喜忌": luck_branch_six_combine_favourability(four_pillars, luck_pillar),
        "地支三合五行": luck_three_combine_element(four_pillars, luck_pillar),
        "地支三合喜忌": luck_three_combine_favourability(four_pillars, luck_pillar),
        "地支三會五行": luck_three_meeting_element(four_pillars, luck_pillar),
        "地支三會喜忌": luck_three_meeting_favourability(four_pillars, luck_pillar),
        "大運神煞": luck_shensha_summary(four_pillars, luck_pillar)
    }
