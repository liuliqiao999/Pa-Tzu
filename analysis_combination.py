import combination_rules
import analysis_relations

pillars = ["year", "month", "day", "hour"]

# 分析原局天干五合及其合化條件
def analyse_stem_five_combinations(four_pillars):
    results = []
    combinations = combination_rules.combination_stem_conditions(four_pillars)
    for combination in combinations:
        status = combination_rules.combination_condition_status(
            combination["月令"],
            combination["透干"],
            combination["通根"],
            combination["受剋"]
        )
        results.append({**combination,"距離": combination_rules.combination_stem_distance(*combination["柱位"]),"合化條件": status})
    return results

# 分析原局地支六合、三合、三會及其合化條件
def analyse_branch_combinations(four_pillars):
    results = {}
    combination_types = {
        "地支六合": analysis_relations.analyse_branch_combinations,
        "地支三合": analysis_relations.analyse_branch_three_combinations,
        "地支三會": analysis_relations.analyse_branch_three_meetings
    }
    for name, analyse_function in combination_types.items():
        results[name] = []
        for *combined_pillars, element in analyse_function(four_pillars):
            conditions = combination_rules.combination_branch_conditions(four_pillars, combined_pillars, element)
            status = combination_rules.combination_condition_status(conditions["月令"],conditions["透干"], conditions["通根"], conditions["受沖"])
            results[name].append({"柱位": tuple(combined_pillars),"化神": element, **conditions, "合化條件": status})
    return results

# 檢查地支合局是否共用柱位, 返回互相重疊的合局及其共用柱位
def analyse_branch_combination_conflicts(four_pillars):
    combinations = analyse_branch_combinations(four_pillars)
    groups = []
    for name, results in combinations.items():
        for result in results:
            groups.append((name, result))
    conflicts = []
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            name_a, group_a = groups[i]
            name_b, group_b = groups[j]
            shared = set(group_a["柱位"]) & set(group_b["柱位"])
            if shared:
                conflicts.append({
                    "合局1": name_a,
                    "合局2": name_b,
                    "柱位1": group_a["柱位"],
                    "柱位2": group_b["柱位"],
                    "共用柱位": tuple(pillar for pillar in pillars if pillar in shared)
                })
    return conflicts



# 地支重疊合局優先級, 先比較合化條件, 再比較合局類型
def analyse_branch_combination_priority(four_pillars):
    conflicts = analyse_branch_combination_conflicts(four_pillars)
    branch_results = analyse_branch_combinations(four_pillars)
    results = []
    for conflict in conflicts:
        type_a = conflict["合局1"]
        type_b = conflict["合局2"]
        group_a = next(group for group in branch_results[type_a] if group["柱位"] == conflict["柱位1"])
        group_b = next(group for group in branch_results[type_b] if group["柱位"] == conflict["柱位2"])
        status_a = group_a["合化條件"]
        status_b = group_b["合化條件"]
        if status_a > status_b:
            preferred = type_a
        elif status_b > status_a:
            preferred = type_b
        elif status_a == 1:
            priority_a = combination_rules.combination_branch_priority(type_a)
            priority_b = combination_rules.combination_branch_priority(type_b)
            if priority_a > priority_b:
                preferred = type_a
            elif priority_b > priority_a:
                preferred = type_b
            else:
                preferred = None
        else:
            preferred = None
        results.append({**conflict, "優先合局": preferred})
    return results

# 檢查天干五合是否共用柱位（爭合候選）
def analyse_stem_combination_conflicts(four_pillars):
    combinations = analyse_stem_five_combinations(four_pillars)
    conflicts = []
    for i in range(len(combinations)):
        for j in range(i + 1, len(combinations)):
            group_a = combinations[i]
            group_b = combinations[j]
            shared = set(group_a["柱位"]) & set(group_b["柱位"])
            if shared:
                conflicts.append({
                    "柱位1": group_a["柱位"],
                    "柱位2": group_b["柱位"],
                    "共用柱位": tuple(pillar for pillar in pillars if pillar in shared)
                })
    return conflicts



# 整合合化條件及合局衝突
# 1 = 條件較充分且無未解決衝突, 0 = 條件待定或存在衝突, -1 = 條件不足
def analyse_combination_final_status(four_pillars):
    stem_results = analyse_stem_five_combinations(four_pillars)
    branch_results = analyse_branch_combinations(four_pillars)
    stem_conflicts = analyse_stem_combination_conflicts(four_pillars)
    # 收集發生爭合的天干組合
    conflicted_stems = set()
    for conflict in stem_conflicts:
        conflicted_stems.add(conflict["柱位1"])
        conflicted_stems.add(conflict["柱位2"])
    # 根據合化條件及優先級，收集需要降級的地支合局
    demoted_branches = set()
    for conflict in analyse_branch_combination_priority(four_pillars):
        group_a = (conflict["合局1"], conflict["柱位1"])
        group_b = (conflict["合局2"], conflict["柱位2"])
        preferred = conflict["優先合局"]
        if preferred == conflict["合局1"]:
            demoted_branches.add(group_b)
        elif preferred == conflict["合局2"]:
            demoted_branches.add(group_a)
        else:
            # 無法決定優先級，兩組均暫時降級
            demoted_branches.add(group_a)
            demoted_branches.add(group_b)
    # 天干五合
    for result in stem_results:
        status = result["合化條件"]
        if status == 1:
            if result["柱位"] in conflicted_stems or result["距離"] > 0:
                status = 0
        result["最終狀態"] = status
    # 地支六合、三合、三會
    for name, groups in branch_results.items():
        for result in groups:
            status = result["合化條件"]
            if status == 1 and (name, result["柱位"]) in demoted_branches:
                status = 0
            result["最終狀態"] = status
    return {"天干五合": stem_results, **branch_results}


# 整合原局合化分析及衝突資訊
def analyse_all_combinations(four_pillars):
    return {
        **analyse_combination_final_status(four_pillars),
        "天干爭合候選": analyse_stem_combination_conflicts(four_pillars),
        "地支合局重疊": analyse_branch_combination_conflicts(four_pillars),
        "地支合局優先級": analyse_branch_combination_priority(four_pillars)
    }


