import shensha_stem

pillars = ["year", "month", "day", "hour"]

def analyse_day_stem_shensha(four_pillars, shensha_function): # shensha_function 是一個函數，根據日干返回對應的神煞地支列表
    # 分析以日干為基準的神煞所在柱位
    # 對多數神煞，日干是唯一的參考點，但有些神煞可能會使用年干作為參考點，這時候可以傳入不同的函數來處理
    day_stem = four_pillars["day"][0]
    shensha_branches = shensha_function(day_stem)
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if branch in shensha_branches:
            results.append(pillar)
    return results

def analyse_lok_san(four_pillars):
    # 分析祿神所在柱位
    return analyse_day_stem_shensha(four_pillars, shensha_stem.Lok_San)

def analyse_yeung_jan(four_pillars):
    # 分析羊刃所在柱位
    return analyse_day_stem_shensha(four_pillars, shensha_stem.Yeung_Jan)

def analyse_tin_yuet(four_pillars, apply_year_stem = False):
    # 分析天乙貴人所在柱位
    # 不同流派對天乙貴人的計算方式不同，有些流派使用日干，有些流派一起使用年干日干
    # 默認只使用日干
    day_stem = four_pillars["day"][0]
    if apply_year_stem:
        year_stem = four_pillars["year"][0] #年干
        tin_yuet = shensha_stem.Tin_Yuet(year_stem) + shensha_stem.Tin_Yuet(day_stem)
    else:
        tin_yuet = shensha_stem.Tin_Yuet(day_stem)
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if branch in tin_yuet:
            results.append(pillar)
    return results

def analyse_man_cheung(four_pillars, apply_year_stem = False):
    # 分析文昌貴人所在柱位
    # 不同流派對文昌貴人的計算方式不同，有些流派使用日干，有些流派一起使用年干日干
    # 默認只使用日干
    day_stem = four_pillars["day"][0]
    if apply_year_stem:
        year_stem = four_pillars["year"][0] #年干
        man_cheung = shensha_stem.Man_Cheung(year_stem) + shensha_stem.Man_Cheung(day_stem)
    else:
        man_cheung = shensha_stem.Man_Cheung(day_stem)
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if branch in man_cheung:
            results.append(pillar)
    return results

def analyse_gam_jyu(four_pillars):
    # 分析金輿所在柱位
    return analyse_day_stem_shensha(four_pillars, shensha_stem.Gam_Jyu)

def analyse_hok_tong(four_pillars):
    # 分析學堂所在柱位
    return analyse_day_stem_shensha(four_pillars, shensha_stem.Hok_Tong)
    

def analyse_ci_gun(four_pillars):
    # 分析詞館所在柱位
    return analyse_day_stem_shensha(four_pillars, shensha_stem.Ci_Gun)

def analyse_taai_gik(four_pillars):
    # 分析太極貴人所在柱位
    return analyse_day_stem_shensha(four_pillars, shensha_stem.Taai_Gik)

def analyse_gwok_yan(four_pillars):
    # 分析國印貴人所在柱位
    return analyse_day_stem_shensha(four_pillars, shensha_stem.Gwok_Yan)

def analyse_tin_cyu(four_pillars):
    # 分析天廚貴人所在柱位
    return analyse_day_stem_shensha(four_pillars, shensha_stem.Tin_Cyu)

def analyse_fuk_sing(four_pillars):
    # 分析福星貴人所在柱位
    return analyse_day_stem_shensha(four_pillars, shensha_stem.Fuk_Sing)
