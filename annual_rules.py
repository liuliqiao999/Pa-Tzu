import calendar
import rules
import constant
from itertools import combinations
import shensha_three_combine
import shensha_year
import shensha_month
import shensha_stem
import shensha_day


pillars = ["year", "month", "day", "hour"]

## 流年
def annual_pillar(solar_date):
    return calendar.get_year_gz(solar_date) ## 得到流年的天干地支

def annual_stem_ten_god(four_pillars, solar_date):
    day_stem = four_pillars["day"][0]
    annual_stem = annual_pillar(solar_date)[0]
    return rules.ten_god(day_stem, annual_stem)

def annual_hidden_ten_gods(four_pillars, solar_date):
    day_stem = four_pillars["day"][0]
    annual_branch = annual_pillar(solar_date)[1]
    hidden_stems = constant.hidden_stems(annual_branch)
    return [rules.ten_god(day_stem, stem) for stem in hidden_stems]

def annual_stem_five_relations(four_pillars, solar_date): ## 天干五合
    annual_stem = annual_pillar(solar_date)[0]
    results = []
    for pillar in pillars:
        stem = four_pillars[pillar][0]
        if rules.stem_five_relation(annual_stem, stem):
            results.append(pillar)
    return results

def annual_branch_six_clash(four_pillars, solar_date): ##地支六沖
    annual_branch = annual_pillar(solar_date)[1]
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if rules.branch_six_clash_relation(annual_branch, branch):
            results.append(pillar)
    return results

def annual_branch_six_combine(four_pillars, solar_date): ##地支六合
    annual_branch = annual_pillar(solar_date)[1]
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if rules.branch_six_combine_relation(annual_branch, branch):
            results.append(pillar)
    return results

def annual_branch_six_harm(four_pillars, solar_date): ##地支六害
    annual_branch = annual_pillar(solar_date)[1]
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if rules.branch_six_harm_relation(annual_branch, branch):
            results.append(pillar)
    return results

def annual_branch_six_break(four_pillars, solar_date): ##地支六破
    annual_branch = annual_pillar(solar_date)[1]
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if rules.branch_six_break_relation(annual_branch, branch):
            results.append(pillar)
    return results

def annual_branch_three_combine(four_pillars, solar_date): ##地支三合，原局兩個地支，流年地支
    annual_branch = annual_pillar(solar_date)[1]
    results = []
    for pillar_a, pillar_b in combinations(pillars, 2):
        branch_a, branch_b = four_pillars[pillar_a][1], four_pillars[pillar_b][1]
        if rules.branch_three_combine_relation(annual_branch, branch_a, branch_b):
            results.append((pillar_a, pillar_b))
    return results

def annual_branch_three_meeting(four_pillars, solar_date): ##地支三會，原局兩個地支，流年地支
    annual_branch = annual_pillar(solar_date)[1]
    results = []
    for pillar_a, pillar_b in combinations(pillars, 2):
        branch_a, branch_b = four_pillars[pillar_a][1], four_pillars[pillar_b][1]
        if rules.branch_three_meeting_relation(annual_branch, branch_a, branch_b):
            results.append((pillar_a, pillar_b))
    return results

## 地支相刑
def annual_branch_punishment(four_pillars, solar_date):
    annual_branch = annual_pillar(solar_date)[1]
    original_branches = [four_pillars[pillar][1] for pillar in pillars]
    original_punishments = rules.branch_punishment(original_branches)
    annual_branches = original_branches + [annual_branch]
    annual_punishments = rules.branch_punishment(annual_branches)
    results = []
    for punishment in annual_punishments:
        if punishment not in original_punishments:
            results.append(punishment)
    return results


# 流年地支半合
def annual_branch_half_combine(four_pillars, solar_date):
    annual_branch = annual_pillar(solar_date)[1]
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if rules.branch_half_combine_relation(annual_branch, branch):
            results.append(pillar)
    return results

# 流年地支半會
def annual_branch_half_meeting(four_pillars, solar_date):
    annual_branch = annual_pillar(solar_date)[1]
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if rules.branch_half_meeting_relation(annual_branch, branch):
            results.append(pillar)
    return results

##### 神煞 #####
def annual_three_combine_shensha(four_pillars, solar_date):
    annual_branch = annual_pillar(solar_date)[1]
    day_branch = four_pillars["day"][1]
    shensha_functions = {
        "桃花": shensha_three_combine.Tou_Faa,
        "驛馬": shensha_three_combine.Yik_Maa,
        "華蓋": shensha_three_combine.Waa_Goi,
        "將星": shensha_three_combine.Zoeng_Sing,
        "劫煞": shensha_three_combine.Gip_Saat,
        "亡神": shensha_three_combine.Mong_San,
        "災煞": shensha_three_combine.Zoi_Saat,
    }
    results = []
    for name in shensha_functions:
        target_branches = shensha_functions[name](day_branch)
        if annual_branch in target_branches:
            results.append(name)
    return results

def annual_year_shensha(four_pillars, solar_date):
    annual_branch = annual_pillar(solar_date)[1]
    year_branch = four_pillars["year"][1]
    shensha_functions = {
        "紅鸞": shensha_year.Hung_Luen,
        "天喜": shensha_year.Tin_Hei,
        "孤辰": shensha_year.Gu_San,
        "寡宿": shensha_year.Gwa_Suk,
        "喪門": shensha_year.Sang_Mun,
        "弔客": shensha_year.Diu_Haak,
        "歲破": shensha_year.Seoi_Po,
        "披麻": shensha_year.Pei_Maa,
        "官符": shensha_year.Gun_Fu,
        "白虎": shensha_year.Baak_Fu,
    }
    results = []
    for name in shensha_functions:
        target_branch = shensha_functions[name](year_branch)
        if annual_branch == target_branch:
            results.append(name)
    return results

def annual_month_shensha(four_pillars, solar_date):
    annual_stem, annual_branch = annual_pillar(solar_date)
    month_branch = four_pillars["month"][1]
    results = []
    tin_dak = shensha_month.Tin_Dak(month_branch)
    if annual_stem == tin_dak or annual_branch == tin_dak:
        results.append("天德貴人")
    yuet_tak = shensha_month.Yuet_Tak(month_branch)
    if annual_stem == yuet_tak:
        results.append("月德貴人")
    tin_ji = shensha_month.Tin_Ji(month_branch)
    if annual_branch == tin_ji:
        results.append("天醫")
    dak_sau = shensha_month.Dak_Sau(month_branch)
    if annual_stem in dak_sau["德"]:
        results.append("德")
    if annual_stem in dak_sau["秀"]:
        results.append("秀")
    return results

def annual_stem_shensha(four_pillars, solar_date):
    annual_branch = annual_pillar(solar_date)[1]
    day_stem = four_pillars["day"][0]
    shensha_functions = {
        "祿神": shensha_stem.Lok_San,
        "羊刃": shensha_stem.Yeung_Jan,
        "天乙貴人": shensha_stem.Tin_Yuet,
        "文昌": shensha_stem.Man_Cheung,
        "金輿": shensha_stem.Gam_Jyu,
        "學堂": shensha_stem.Hok_Tong,
        "詞館": shensha_stem.Ci_Gun,
        "太極貴人": shensha_stem.Taai_Gik,
        "國印貴人": shensha_stem.Gwok_Yan,
        "福星貴人": shensha_stem.Fuk_Sing,
        "天廚貴人": shensha_stem.Tin_Cyu,
    }
    results = []
    for name in shensha_functions:
        target_branches = shensha_functions[name](day_stem)
        if annual_branch in target_branches:
            results.append(name)
    return results

def annual_day_shensha(four_pillars, solar_date):
    annual_branch = annual_pillar(solar_date)[1]
    day_stem = four_pillars["day"][0]
    day_branch = four_pillars["day"][1]
    results = []
    hung_mong = shensha_day.Hung_Mong(day_stem, day_branch)
    if annual_branch in hung_mong:
        results.append("空亡")
    return results
