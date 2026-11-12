import rules

############# 大運與流年的直接關係 ############# 
# 大運與流年天干五合
def luck_annual_stem_five(luck_pillar, annual_pillar):
    return rules.stem_five_relation(luck_pillar[0], annual_pillar[0])

# 大運與流年地支六沖
def luck_annual_branch_six_clash(luck_pillar, annual_pillar):
    return rules.branch_six_clash_relation(luck_pillar[1], annual_pillar[1])

# 大運與流年地支六合
def luck_annual_branch_six_combine(luck_pillar, annual_pillar):
    return rules.branch_six_combine_relation(luck_pillar[1], annual_pillar[1])

# 大運與流年地支六害
def luck_annual_branch_six_harm(luck_pillar, annual_pillar):
    return rules.branch_six_harm_relation(luck_pillar[1], annual_pillar[1])

# 大運與流年地支六破
def luck_annual_branch_six_break(luck_pillar, annual_pillar):
    return rules.branch_six_break_relation(luck_pillar[1], annual_pillar[1])

# 大運與流年地支相刑
def luck_annual_branch_punishment(luck_pillar, annual_pillar):
    luck_branch = luck_pillar[1]
    annual_branch = annual_pillar[1]
    branches = [luck_branch, annual_branch]
    return rules.branch_punishment(branches)

# 大運與流年地支半合
def luck_annual_branch_half_combine(luck_pillar, annual_pillar):
    return rules.branch_half_combine_relation(luck_pillar[1], annual_pillar[1])

# 大運與流年地支半會
def luck_annual_branch_half_meeting(luck_pillar, annual_pillar):
    return rules.branch_half_meeting_relation(luck_pillar[1], annual_pillar[1])


############# 原局、大運、流年的三方關係 #############
# 原局, 大運, 流年三合
def three_layer_combine(four_pillars, luck_pillar, annual_pillar):
        luck_branch = luck_pillar[1]
        annual_branch = annual_pillar[1]
        results = []
        for pillar, (_, branch) in four_pillars.items():
            if rules.branch_three_combine_relation(branch, luck_branch, annual_branch):
                results.append(pillar)
        return results

# 原局, 大運, 流年三會
def three_layer_meeting(four_pillars, luck_pillar, annual_pillar):
    luck_branch = luck_pillar[1]
    annual_branch = annual_pillar[1]
    results = []
    for pillar, (_, branch) in four_pillars.items():
        if rules.branch_three_meeting_relation(branch, luck_branch, annual_branch):
            results.append(pillar)
    return results


# 原局, 大運, 流年三刑
def three_layer_punishment(four_pillars, luck_pillar, annual_pillar):
    luck_branch = luck_pillar[1]
    annual_branch = annual_pillar[1]
    results = []
    for pillar in four_pillars:
        original_branch = four_pillars[pillar][1]
        branches = [original_branch, luck_branch, annual_branch]
        punishments = rules.branch_punishment(branches) ## 只考慮寅巳申, 丑未戌
        for punishment in punishments:
            if punishment == "寅巳申" or punishment == "丑未戌":
                results.append(pillar)
    return results


############# 特殊歲運關係 #############
# 歲運並臨, 大運與流年的天干, 地支完全相同
def annual_luck_parallel(annual_pillar, luck_pillar):
    return annual_pillar == luck_pillar

# 伏吟: 兩柱的天干, 地支完全相同
def fuyin(pillar_a, pillar_b):
    return pillar_a == pillar_b

# 反吟：兩柱天干相剋，而且地支六沖
def fanyin(pillar_a, pillar_b):
    stem_relation = rules.stem_element_relation(pillar_a[0], pillar_b[0])
    if abs(stem_relation) != 2:
        return False
    branch_clash = rules.branch_six_clash_relation(pillar_a[1], pillar_b[1])
    return branch_clash

    


