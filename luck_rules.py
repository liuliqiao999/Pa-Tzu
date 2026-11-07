import constant
import calendar
import datetime
import rules
from itertools import combinations
import shensha_three_combine
import shensha_year
import shensha_month
import shensha_stem
import shensha_day

pillars = ["year", "month", "day", "hour"]

########### 大運 ###########
# 出生年干 陽干男順女逆，陰干男逆女順
# define 男 = 1, 女 = 0
def luck_direction(year_stem, gender):
    YamYeung = constant.stem_YamYeung(year_stem)  # 陰陽判斷，陽1陰0
    if YamYeung == gender:
        return 1
    else:
        return -1

# 起運歲數，三日一歲
def luck_start_age(birth_datetime, direction):
    jie_term = calendar.get_nearest_solar_term(birth_datetime, direction, calendar.jie_terms)
    term_datetime = jie_term[1]
    difference = abs(term_datetime - birth_datetime)
    age = difference.total_seconds() / (3 * 24 * 3600)
    return age

# 大運干支的推算
def luck_pillars(month_pillar, direction, count): # 1 count就是10年左右
    if not isinstance(count, int) or count <= 0:
        raise ValueError()
    if direction not in (1, -1):
        raise ValueError()
    month_stem, month_branch = month_pillar[0], month_pillar[1]
    x, y = constant.ten_stems.index(month_stem), constant.twelve_branches.index(month_branch)
    result = []
    for i in range(1, count + 1):
        a =  (x + i * direction) % 10
        b =  (y + i * direction) % 12
        result.append((constant.ten_stems[a], constant.twelve_branches[b]))
    return result

def get_luck_cycles(four_pillars, birth_datetime, gender, count):
    if not isinstance(count, int) or count <= 0:
        raise ValueError()
    if gender not in (0, 1):
        raise ValueError()
    year_stem = four_pillars["year"][0]
    direction = luck_direction(year_stem, gender)
    start_age = luck_start_age(birth_datetime, direction)
    month_pillar = four_pillars["month"]
    cycle = luck_pillars(month_pillar, direction, count)
    result = []
    for i in range(count):
        result.append({"pillar": cycle[i], 
                       "start_age": start_age + i * 10, 
                       "end_age": start_age + (i + 1) * 10})
    return result

# 公曆氣運時間, 將起運歲數換算成實際交運時間
def luck_start_date(birth_datetime, start_age):
    if start_age < 0:
        raise ValueError("")
    # 三日一歲換算出的年齡，先轉成傳統月份
    total_months = start_age * 12
    whole_months = int(total_months)
    remaining_days = (total_months - whole_months) * 30
    # 加上整數月份
    year = birth_datetime.year + (birth_datetime.month - 1 + whole_months) // 12
    month = (birth_datetime.month - 1 + whole_months) % 12 + 1
    # 處理目標月份可能沒有出生日期的情況
    if month == 12:
        next_month = datetime.datetime(year + 1, 1, 1)
    else:
        next_month = datetime.datetime(year, month + 1, 1)
    last_day = (next_month - datetime.timedelta(days=1)).day
    day = min(birth_datetime.day, last_day)
    start_datetime = birth_datetime.replace(year = year, month = month, day = day)
    return start_datetime + datetime.timedelta(days = remaining_days)

# 查詢指定日期所處的大運
def get_luck_pillar_at_date(luck_cycles, birth_datetime, target_date):
    if not luck_cycles:
        return None
    if isinstance(target_date, datetime.date) and not isinstance(target_date, datetime.datetime):
        target_date = datetime.datetime.combine(target_date, datetime.time.min)
    start_age = luck_cycles[0]["start_age"]
    first_start = luck_start_date(birth_datetime, start_age)
    if target_date < first_start:
        return None
    for i, cycle in enumerate(luck_cycles):
        start_year = first_start.year + 10 * i
        end_year = first_start.year + 10 * (i + 1)
        # 處理 2 月 29 日在非閏年的情況
        try:
            start = first_start.replace(year=start_year)
        except ValueError:
            start = first_start.replace(year=start_year, day=28)
        try:
            end = first_start.replace(year=end_year)
        except ValueError:
            end = first_start.replace(year=end_year, day=28)
        if start <= target_date < end:
            return cycle["pillar"]
    return None

def luck_stem_ten_god(four_pillars, luck_pillar):
    day_stem = four_pillars["day"][0]
    luck_stem = luck_pillar[0]
    return rules.ten_god(day_stem, luck_stem)


def luck_hidden_ten_gods(four_pillars, luck_pillar):
    day_stem = four_pillars["day"][0]
    luck_branch = luck_pillar[1]
    hidden_stems = constant.hidden_stems(luck_branch)
    return [rules.ten_god(day_stem, stem) for stem in hidden_stems]

# 大運天干五合
def luck_stem_five_relations(four_pillars, luck_pillar):
    luck_stem = luck_pillar[0]
    results = []
    for pillar in pillars:
        stem = four_pillars[pillar][0]
        if rules.stem_five_relation(luck_stem, stem):
            results.append(pillar)
    return results

# 大運地支六沖
def luck_branch_six_clash(four_pillars, luck_pillar):
    luck_branch = luck_pillar[1]
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if rules.branch_six_clash_relation(luck_branch, branch):
            results.append(pillar)
    return results

# 大運地支六合
def luck_branch_six_combine(four_pillars, luck_pillar):
    luck_branch = luck_pillar[1]
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if rules.branch_six_combine_relation(luck_branch, branch):
            results.append(pillar)
    return results

# 大運地支六害
def luck_branch_six_harm(four_pillars, luck_pillar):
    luck_branch = luck_pillar[1]
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if rules.branch_six_harm_relation(luck_branch, branch):
            results.append(pillar)
    return results

# 大運地支六破
def luck_branch_six_break(four_pillars, luck_pillar):
    luck_branch = luck_pillar[1]
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if rules.branch_six_break_relation(luck_branch, branch):
            results.append(pillar)
    return results

# 大運地支三合
def luck_branch_three_combine(four_pillars, luck_pillar):
    luck_branch = luck_pillar[1]
    results = []
    for pillar_a, pillar_b in combinations(pillars, 2):
            branch_a, branch_b = four_pillars[pillar_a][1], four_pillars[pillar_b][1]
            if rules.branch_three_combine_relation(luck_branch, branch_a, branch_b):
                results.append((pillar_a, pillar_b))
    return results

# 大運地支三會
def luck_branch_three_meeting(four_pillars, luck_pillar):
    luck_branch = luck_pillar[1]
    results = []
    for pillar_a, pillar_b in combinations(pillars, 2):
            branch_a, branch_b = four_pillars[pillar_a][1], four_pillars[pillar_b][1]
            if rules.branch_three_meeting_relation(luck_branch, branch_a, branch_b):
                results.append((pillar_a, pillar_b))
    return results

# 大運地支相刑
def luck_branch_punishment(four_pillars, luck_pillar):
    luck_branch = luck_pillar[1]
    original_branches = [four_pillars[pillar][1] for pillar in pillars]
    original_punishments = rules.branch_punishment(original_branches)
    luck_branches = original_branches + [luck_branch]
    luck_punishments = rules.branch_punishment(luck_branches)
    results = []
    for punishment in luck_punishments:
            if punishment not in original_punishments:
                results.append(punishment)
    return results

# 大運地支半合
def luck_branch_half_combine(four_pillars, luck_pillar):
    luck_branch = luck_pillar[1]
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if rules.branch_half_combine_relation(luck_branch, branch):
            results.append(pillar)
    return results

# 大運地支半會
def luck_branch_half_meeting(four_pillars, luck_pillar):
    luck_branch = luck_pillar[1]
    results = []
    for pillar in pillars:
        branch = four_pillars[pillar][1]
        if rules.branch_half_meeting_relation(luck_branch, branch):
            results.append(pillar)
    return results

##### 神煞 #####
def luck_three_combine_shensha(four_pillars, luck_pillar):
    luck_branch = luck_pillar[1]
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
        if luck_branch in target_branches:
            results.append(name)
    return results


def luck_year_shensha(four_pillars, luck_pillar):
    luck_branch = luck_pillar[1]
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
        if luck_branch == target_branch:
            results.append(name)
    return results

def luck_month_shensha(four_pillars, luck_pillar):
    luck_stem, luck_branch = luck_pillar
    month_branch = four_pillars["month"][1]
    results = []
    tin_dak = shensha_month.Tin_Dak(month_branch)
    if luck_stem == tin_dak or luck_branch == tin_dak:
        results.append("天德貴人")
    yuet_tak = shensha_month.Yuet_Tak(month_branch)
    if luck_stem == yuet_tak:
        results.append("月德貴人")
    tin_ji = shensha_month.Tin_Ji(month_branch)
    if luck_branch == tin_ji:
        results.append("天醫")
    dak_sau = shensha_month.Dak_Sau(month_branch)
    if luck_stem in dak_sau["德"]:
        results.append("德")
    if luck_stem in dak_sau["秀"]:
        results.append("秀")
    return results

def luck_stem_shensha(four_pillars, luck_pillar):
    luck_branch = luck_pillar[1]
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
        if luck_branch in target_branches:
            results.append(name)
    return results

def luck_day_shensha(four_pillars, luck_pillar):
    luck_branch = luck_pillar[1]
    day_stem = four_pillars["day"][0]
    day_branch = four_pillars["day"][1]
    results = []
    hung_mong = shensha_day.Hung_Mong(day_stem, day_branch)
    if luck_branch in hung_mong:
        results.append("空亡")
    return results
