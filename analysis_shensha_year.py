import shensha_year

pillars = ["year", "month", "day", "hour"]

def analyse_year_branch_shensha(four_pillars, shensha_function):
    # 分析以年支為基準的神煞所在柱位
    year_branch = four_pillars["year"][1]
    shensha_branch = shensha_function(year_branch)
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if branch == shensha_branch:
            results.append(pillar)
    return results

def analyse_hung_luen(four_pillars):
    return analyse_year_branch_shensha(four_pillars, shensha_year.Hung_Luen)

def analyse_tin_hei(four_pillars):
    return analyse_year_branch_shensha(four_pillars, shensha_year.Tin_Hei)

def analyse_gu_san(four_pillars):
    return analyse_year_branch_shensha(four_pillars, shensha_year.Gu_San)

def analyse_gwa_suk(four_pillars):
    return analyse_year_branch_shensha(four_pillars, shensha_year.Gwa_Suk)

def analyse_sang_mun(four_pillars):
    return analyse_year_branch_shensha(four_pillars, shensha_year.Sang_Mun)

def analyse_diu_haak(four_pillars):
    return analyse_year_branch_shensha(four_pillars, shensha_year.Diu_Haak)

def analyse_seoi_po(four_pillars):
    return analyse_year_branch_shensha(four_pillars, shensha_year.Seoi_Po)

def analyse_pei_maa(four_pillars):
    return analyse_year_branch_shensha(four_pillars, shensha_year.Pei_Maa)

def analyse_gun_fu(four_pillars):
    return analyse_year_branch_shensha(four_pillars, shensha_year.Gun_Fu)

def analyse_baak_fu(four_pillars):
    return analyse_year_branch_shensha(four_pillars, shensha_year.Baak_Fu)
