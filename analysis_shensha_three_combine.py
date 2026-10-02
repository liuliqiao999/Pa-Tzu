import shensha_three_combine

pillars = ["year", "month", "day", "hour"]

# 三合局主要看日支, 有些流派在部分神煞會 年支/日支一起看
# 默認只看日支
def analyse_day_branch_shensha(four_pillars, shensha_function):
    # 只使用日支
    day_branch = four_pillars["day"][1]
    shensha_branches = shensha_function(day_branch)
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if branch in shensha_branches:
            results.append(pillar)
    return results

def analyse_year_day_branch_shensha(four_pillars, shensha_function, apply_year_branch=False):
    # 同時使用年支和日支，也可以只查日支
    if not apply_year_branch:
        return analyse_day_branch_shensha(four_pillars, shensha_function)
    year_branch = four_pillars["year"][1]
    day_branch = four_pillars["day"][1]
    shensha_branches = (shensha_function(year_branch) + shensha_function(day_branch))
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if branch in shensha_branches:
            results.append(pillar)
    return results

def analyse_tou_faa(four_pillars, apply_year_branch = False):
    return analyse_year_day_branch_shensha(four_pillars, shensha_three_combine.Tou_Faa, apply_year_branch)

def analyse_yik_maa(four_pillars, apply_year_branch = False):
    return analyse_year_day_branch_shensha(four_pillars, shensha_three_combine.Yik_Maa, apply_year_branch)

def analyse_waa_goi(four_pillars, apply_year_branch = False):
    return analyse_year_day_branch_shensha(four_pillars, shensha_three_combine.Waa_Goi, apply_year_branch)

def analyse_zoeng_sing(four_pillars, apply_year_branch = False):
    return analyse_year_day_branch_shensha(four_pillars, shensha_three_combine.Zoeng_Sing, apply_year_branch)

def analyse_gip_saat(four_pillars, apply_year_branch = False):
    return analyse_year_day_branch_shensha(four_pillars, shensha_three_combine.Gip_Saat, apply_year_branch)

def analyse_mong_san(four_pillars, apply_year_branch = False):
    return analyse_year_day_branch_shensha(four_pillars, shensha_three_combine.Mong_San, apply_year_branch)

def analyse_zoi_saat(four_pillars, apply_year_branch = False):
    return analyse_year_day_branch_shensha(four_pillars, shensha_three_combine.Zoi_Saat, apply_year_branch)
