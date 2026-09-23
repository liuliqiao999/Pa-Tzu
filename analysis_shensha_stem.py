import shensha_stem

pillars = ["year", "month", "day", "hour"]

def analyse_lok_san(four_pillars):
    # 分析祿神所在柱位
    day_stem = four_pillars["day"][0]    # 祿神的地支位置是根據日干來決定的，然後檢查四柱中哪些柱的地支與祿神地支匹配
    lok_san = shensha_stem.Lok_San(day_stem)
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if branch in lok_san:
            results.append(pillar)
    return results

def analyse_yeung_jan(four_pillars):
    # 分析羊刃所在柱位
    day_stem = four_pillars["day"][0]     # 羊刃的地支位置是根據日干來決定的，然後檢查四柱中哪些柱的地支與羊刃地支匹配
    yeung_jan = shensha_stem.Yeung_Jan(day_stem)
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if branch in yeung_jan:
            results.append(pillar)
    return results

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
    day_stem = four_pillars["day"][0]
    gam_jyu = shensha_stem.Gam_Jyu(day_stem)
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if branch in gam_jyu:
            results.append(pillar)
    return results

def analyse_hok_tong(four_pillars):
    # 分析學堂所在柱位
    day_stem = four_pillars["day"][0]
    hok_tong = shensha_stem.Hok_Tong(day_stem)
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if branch in hok_tong:
            results.append(pillar)
    return results

def analyse_ci_gun(four_pillars):
    # 分析詞館所在柱位
    day_stem = four_pillars["day"][0]
    ci_gun = shensha_stem.Ci_Gun(day_stem)
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if branch in ci_gun:
            results.append(pillar)
    return results

def analyse_taai_gik(four_pillars):
    # 分析太極貴人所在柱位
    day_stem = four_pillars["day"][0]
    taai_gik = shensha_stem.Taai_Gik(day_stem)
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if branch in taai_gik:
            results.append(pillar)
    return results

def analyse_gwok_yan(four_pillars):
    # 分析國印貴人所在柱位
    day_stem = four_pillars["day"][0]
    gwok_yan = shensha_stem.Gwok_Yan(day_stem)
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if branch in gwok_yan:
            results.append(pillar)
    return results

def analyse_tin_cyu(four_pillars):
    # 分析天廚貴人所在柱位
    day_stem = four_pillars["day"][0]
    tin_cyu = shensha_stem.Tin_Cyu(day_stem)
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if branch in tin_cyu:
            results.append(pillar)
    return results

def analyse_fuk_sing(four_pillars):
    # 分析福星貴人所在柱位
    day_stem = four_pillars["day"][0]
    fuk_sing = shensha_stem.Fuk_Sing(day_stem)
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if branch in fuk_sing:
            results.append(pillar)
    return results
