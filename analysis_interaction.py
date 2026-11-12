import interaction_rules
import rules
import constant
import analysis_five_elements

# 大運與流年的干支關係
def luck_annual_interactions(luck_pillar, annual_pillar):
    return {
        "天干五合": interaction_rules.luck_annual_stem_five(luck_pillar, annual_pillar),
        "地支六沖": interaction_rules.luck_annual_branch_six_clash(luck_pillar, annual_pillar),
        "地支六合": interaction_rules.luck_annual_branch_six_combine(luck_pillar, annual_pillar),
        "地支六害": interaction_rules.luck_annual_branch_six_harm(luck_pillar, annual_pillar),
        "地支六破": interaction_rules.luck_annual_branch_six_break(luck_pillar, annual_pillar),
        "地支相刑": interaction_rules.luck_annual_branch_punishment(luck_pillar, annual_pillar),
        "地支半合": interaction_rules.luck_annual_branch_half_combine(luck_pillar, annual_pillar),
        "地支半會": interaction_rules.luck_annual_branch_half_meeting(luck_pillar, annual_pillar)
    }

# 原局, 大運, 流年的三層關係
def three_layer_interactions(four_pillars, luck_pillar, annual_pillar):
    return {
        "地支三合": interaction_rules.three_layer_combine(four_pillars, luck_pillar, annual_pillar),
        "地支三會": interaction_rules.three_layer_meeting(four_pillars, luck_pillar, annual_pillar),
        "地支三刑": interaction_rules.three_layer_punishment(four_pillars, luck_pillar, annual_pillar)
    }

# 特殊歲運關係
def special_interactions(luck_pillar, annual_pillar):
    return {
        "歲運並臨": interaction_rules.annual_luck_parallel(annual_pillar, luck_pillar),
        "伏吟": interaction_rules.fuyin(luck_pillar, annual_pillar),
        "反吟": interaction_rules.fanyin(luck_pillar, annual_pillar)
    }

# 原局與大運的伏吟, 反吟
def original_luck_special(four_pillars, luck_pillar):
    fuyin_results = []
    fanyin_results = []
    for pillar in four_pillars:
        original_pillar = four_pillars[pillar]
        if interaction_rules.fuyin(original_pillar, luck_pillar):
            fuyin_results.append(pillar)
        if interaction_rules.fanyin(original_pillar, luck_pillar):
            fanyin_results.append(pillar)
    return {"伏吟": fuyin_results, "反吟": fanyin_results}

# 原局與流年的伏吟, 反吟
def original_annual_special(four_pillars, annual_pillar):
    fuyin_results = []
    fanyin_results = []
    for pillar in four_pillars:
        original_pillar = four_pillars[pillar]
        if interaction_rules.fuyin(original_pillar, annual_pillar):
            fuyin_results.append(pillar)
        if interaction_rules.fanyin(original_pillar, annual_pillar):
            fanyin_results.append(pillar)
    return {"伏吟": fuyin_results, "反吟": fanyin_results}

# 大運, 流年的天干五合, 地支六合五行判斷
def luck_annual_combination_elements(luck_pillar, annual_pillar):
    luck_stem, luck_branch = luck_pillar
    annual_stem, annual_branch = annual_pillar
    return {
        "天干五合五行": rules.stem_five_element(luck_stem, annual_stem),
        "地支六合五行": rules.branch_six_combine_element(luck_branch, annual_branch)
    }

# 大運, 流年的地支半合, 地支半會五行判斷
def luck_annual_half_elements(luck_pillar, annual_pillar):
    luck_branch = luck_pillar[1]
    annual_branch = annual_pillar[1]
    half_combine_element = None
    half_meeting_element = None
    # 半合五行
    if rules.branch_half_combine_relation(luck_branch, annual_branch):
        half_combine_element = rules.branch_three_combine_group_element(luck_branch)
    # 半會五行
    if rules.branch_half_meeting_relation(luck_branch, annual_branch):
        for branch in constant.twelve_branches:
            element = rules.branch_three_meeting_element(luck_branch, annual_branch, branch)
            if element is not None:
                half_meeting_element = element
                break
    return {"地支半合五行": half_combine_element, "地支半會五行": half_meeting_element}

# 根據原局判斷指定五行的喜忌（通用函數）
def element_favourability(four_pillars, element):
    if element is None:
        return None
    favourable = analysis_five_elements.favourable_relations(four_pillars)
    if not favourable:
        return None
    day_element = constant.stems_elements(four_pillars["day"][0])
    relation = rules.element_relation(day_element, element)
    action = constant.five_element_actions[relation + 2]
    return action in favourable

# 大運與流年的合局喜忌
def luck_annual_combination_favourability(four_pillars, luck_pillar, annual_pillar):
    elements = luck_annual_combination_elements(luck_pillar, annual_pillar)
    half = luck_annual_half_elements(luck_pillar, annual_pillar)
    return {
        "天干五合喜忌": element_favourability(four_pillars, elements["天干五合五行"]),
        "地支六合喜忌": element_favourability(four_pillars, elements["地支六合五行"]),
        "地支半合喜忌": element_favourability(four_pillars, half["地支半合五行"]),
        "地支半會喜忌": element_favourability(four_pillars, half["地支半會五行"])
    }

# 原局、大運、流年的三合及三會五行
def three_layer_elements(four_pillars, luck_pillar, annual_pillar):
    luck_branch = luck_pillar[1]
    annual_branch = annual_pillar[1]
    combinations = three_layer_interactions(four_pillars, luck_pillar, annual_pillar)
    combine_elements = []
    meeting_elements = []
    for pillar in combinations["地支三合"]:
        branch = four_pillars[pillar][1]
        element = rules.branch_three_combine_element(branch, luck_branch, annual_branch)
        if element not in combine_elements:
            combine_elements.append(element)
    for pillar in combinations["地支三會"]:
        branch = four_pillars[pillar][1]
        element = rules.branch_three_meeting_element(branch, luck_branch, annual_branch)
        if element not in meeting_elements:
            meeting_elements.append(element)
    return {"地支三合五行": combine_elements, "地支三會五行": meeting_elements}


# 原局、大運、流年的三合及三會喜忌
def three_layer_favourability(four_pillars, luck_pillar, annual_pillar):
    elements = three_layer_elements(four_pillars, luck_pillar, annual_pillar)
    combine_results = []
    meeting_results = []
    for element in elements["地支三合五行"]:
        combine_results.append(element_favourability(four_pillars, element))
    for element in elements["地支三會五行"]:
        meeting_results.append(element_favourability(four_pillars, element))
    return {"地支三合喜忌": combine_results, "地支三會喜忌": meeting_results}

# 原局、大運、流年交互分析總結
def interaction_basic_analysis(four_pillars, luck_pillar, annual_pillar):
    return {"大運流年關係": luck_annual_interactions(luck_pillar, annual_pillar),
        "大運流年合局五行": luck_annual_combination_elements(luck_pillar, annual_pillar),
        "大運流年半合半會五行": luck_annual_half_elements(luck_pillar, annual_pillar),
        "大運流年合局喜忌": luck_annual_combination_favourability(four_pillars, luck_pillar, annual_pillar),
        "三層關係": three_layer_interactions(four_pillars, luck_pillar, annual_pillar),
        "三層合局五行": three_layer_elements(four_pillars, luck_pillar, annual_pillar),
        "三層合局喜忌": three_layer_favourability(four_pillars, luck_pillar, annual_pillar),
        "歲運特殊關係": special_interactions(luck_pillar, annual_pillar),
        "原局大運特殊關係": original_luck_special(four_pillars, luck_pillar),
        "原局流年特殊關係": original_annual_special(four_pillars, annual_pillar)}
