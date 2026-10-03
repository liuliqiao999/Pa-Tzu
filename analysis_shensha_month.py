import shensha_month

pillars = ["year", "month", "day", "hour"]

def analyse_tin_dak(four_pillars):
    # 分析天德貴人所在柱位
    month_branch = four_pillars["month"][1]
    tin_dak = shensha_month.Tin_Dak(month_branch)
    results = []
    for pillar in pillars:
        stem = four_pillars[pillar][0]
        branch = four_pillars[pillar][1]
        if stem == tin_dak or branch == tin_dak:
            results.append(pillar)
    return results

def analyse_yuet_tak(four_pillars):
    # 分析月德貴人所在柱位
    month_branch = four_pillars["month"][1]
    yuet_tak = shensha_month.Yuet_Tak(month_branch)
    results = []
    for pillar in pillars:
        stem = four_pillars[pillar][0]
        if stem == yuet_tak:
            results.append(pillar)
    return results

def analyse_tin_ji(four_pillars):
    # 分析天醫所在柱位
    month_branch = four_pillars["month"][1]
    tin_ji = shensha_month.Tin_Ji(month_branch)
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if branch == tin_ji:
            results.append(pillar)
    return results

### 德秀貴人
def analyse_dak(four_pillars):
    # 分析德所在柱位
    month_branch = four_pillars["month"][1]
    dak_sau = shensha_month.Dak_Sau(month_branch)
    dak_stems = dak_sau["德"]
    results = []
    for pillar in pillars:
        stem = four_pillars[pillar][0]
        if stem in dak_stems:
            results.append(pillar)
    return results

def analyse_sau(four_pillars):
    # 分析秀所在柱位
    month_branch = four_pillars["month"][1]
    dak_sau = shensha_month.Dak_Sau(month_branch)
    sau_stems = dak_sau["秀"]
    results = []
    for pillar in pillars:
        stem = four_pillars[pillar][0]
        if stem in sau_stems:
            results.append(pillar)
    return results
