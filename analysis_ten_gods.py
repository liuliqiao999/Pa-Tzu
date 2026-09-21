import constant
import rules
import analysis_five_elements

########## /////----------十神基礎分析----------///// ##########
# 四柱天干十神, 以日干為基準
# 返回順序：[年干, 月干, 日干, 時干]
def analyse_stem_ten_gods(four_pillars):
    day_stem = four_pillars["day"][0]
    result = []
    for pillar in ["year", "month", "day", "hour"]:
        target_stem = four_pillars[pillar][0]
        god = rules.ten_god(day_stem, target_stem)
        result.append(god)
    return result

# 四柱地支藏干十神，以日干為基準 返回順序：[年支, 月支, 日支, 時支]
# 每個地支返回一個 list [本氣, 中氣, 餘氣]
def analyse_hidden_ten_gods(four_pillars):
    day_stem = four_pillars["day"][0]
    result = []
    for pillar in ["year", "month", "day", "hour"]:
        target_branch = four_pillars[pillar][1]
        hidden_stems = constant.hidden_stems(target_branch)
        hidden_gods = []
        for hidden_stem in hidden_stems:
            god = rules.ten_god(day_stem, hidden_stem)
            hidden_gods.append(god)
        result.append(hidden_gods)
    return result


# 十神出現次數統計
# 日干本身不計入 明干各計 1，地支每個藏干各計 1
def ten_god_counts(four_pillars):
    counts = [0] * len(constant.ten_gods)
    day_stem = four_pillars["day"][0]
    # 計算明干，日干本身不計
    for pillar in ["year", "month", "hour"]:
        stem = four_pillars[pillar][0]
        god = rules.ten_god(day_stem, stem)
        counts[constant.ten_gods.index(god)] += 1
    # 計算地支藏干
    for pillar in ["year", "month", "day", "hour"]:
        branch = four_pillars[pillar][1]
        hidden_stems = constant.hidden_stems(branch)
        for hidden_stem in hidden_stems:
            god = rules.ten_god(day_stem, hidden_stem)
            counts[constant.ten_gods.index(god)] += 1
    return counts

########## 十神力量統計 ##########
# 日干本身不計入
# 明干各計 3
# 地支藏干：本氣 3、中氣 2、餘氣 1
# 返回順序依照 constant.ten_gods
def ten_god_strength(four_pillars):
    strengths = [0] * len(constant.ten_gods)
    day_stem = four_pillars["day"][0]
    # 計算明干，日干本身不計
    for pillar in ["year", "month", "hour"]:
        stem = four_pillars[pillar][0]
        god = rules.ten_god(day_stem, stem)
        strengths[constant.ten_gods.index(god)] += 3
    # 計算地支藏干
    for pillar in ["year", "month", "day", "hour"]:
        branch = four_pillars[pillar][1]
        hidden_stems = constant.hidden_stems(branch)
        for i, hidden_stem in enumerate(hidden_stems):
            god = rules.ten_god(day_stem, hidden_stem)
            strengths[constant.ten_gods.index(god)] += (3 - i)  # 本氣 3、中氣 2、餘氣 1
    return strengths

# 十神組別力量統計
def ten_god_groups_strength(four_pillars):
    strengths = [0] * len(constant.ten_god_groups)
    ten_god_strengths = ten_god_strength(four_pillars)
    for i, strength in enumerate(ten_god_strengths):
        group_index = i // 2  # 每兩個十神屬於同一組
        strengths[group_index] += strength
    return strengths

def strongest_ten_gods(four_pillars):
    ten_god_strengths = ten_god_strength(four_pillars)
    max_strength = max(ten_god_strengths)
    strongest_gods = []
    for i in range(len(ten_god_strengths)):
        if ten_god_strengths[i] == max_strength:
            strongest_gods.append(constant.ten_gods[i])
    return strongest_gods

def strongest_ten_god_group(four_pillars):
    ten_god_group_strengths = ten_god_groups_strength(four_pillars)
    max_strength = max(ten_god_group_strengths)
    strongest_groups = []
    for i in range(len(ten_god_group_strengths)):
        if ten_god_group_strengths[i] == max_strength:
            strongest_groups.append(constant.ten_god_groups[i])
    return strongest_groups

def missing_ten_gods(four_pillars):
    counts = ten_god_counts(four_pillars)
    missing_gods = []
    for i in range(len(counts)):
        if counts[i] == 0:
            missing_gods.append(constant.ten_gods[i])
    return missing_gods

#測試
if __name__ == "__main__":
    x_pillars = {
        "year":  ("癸", "未"),
        "month": ("乙", "丑"),
        "day":   ("庚", "寅"),
        "hour":  ("壬", "午"),
    }

    counts = ten_god_counts(x_pillars)
    strengths = ten_god_strength(x_pillars)

    print("十神出現次數：")
    for god, count in zip(constant.ten_gods, counts):
        print(f"{god}: {count}")

    print("\n十神力量：")
    for god, strength in zip(constant.ten_gods, strengths):
        print(f"{god}: {strength}")

    print("\n十神組別力量：")
    for group, strength in zip(constant.ten_god_groups, ten_god_groups_strength(x_pillars)):
        print(f"{group}: {strength}")

    print("\n最強十神：")
    for god in strongest_ten_gods(x_pillars):
        print(f"{god}")

    print("\n最強十神組別：")
    for group in strongest_ten_god_group(x_pillars):
        print(f"{group}")