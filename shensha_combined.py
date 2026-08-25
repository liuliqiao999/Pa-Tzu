import constant
import rules
########## -----複合條件神煞----- ##########
# 此類神煞不能只依靠單一天干、地支或日柱判斷，
# 需要同時使用月令（季節）和完整日柱。

########## 季節 ##########
# 根據月支判斷四季：
# 寅卯辰 -> 春 巳午未 -> 夏 申酉戌 -> 秋 亥子丑 -> 冬
# 春夏秋冬，1234
def season(reference_month_branch):
    index = constant.twelve_branches.index(reference_month_branch)
    return ((index - 2) % 12) // 3 + 1

########## 天赦 ##########
# 天赦以季節 + 日柱判斷：
# 春 -> 戊寅
# 夏 -> 甲午
# 秋 -> 戊申
# 冬 -> 甲子
def Tin_Se(reference_month_branch, day_stem, day_branch):
    current_season = season(reference_month_branch)
    day_pillar = day_stem + day_branch
    if current_season == 1:
        return day_pillar == "戊寅"
    elif current_season == 2:
        return day_pillar == "甲午"
    elif current_season == 3:
        return day_pillar == "戊申"
    elif current_season == 4:
        return day_pillar == "甲子"

########## 四廢 ##########
# 春庚申辛酉，夏壬子癸亥，秋甲寅乙卯，冬丙午丁巳
# 四廢以季節 + 日柱判斷：
# 春 -> 庚申、辛酉
# 夏 -> 壬子、癸亥
# 秋 -> 甲寅、乙卯
# 冬 -> 丙午、丁巳
def Sei_Fai(reference_month_branch, day_stem, day_branch):
    current_season = season(reference_month_branch)
    day_pillar = day_stem + day_branch
    if current_season == 1:
        return day_pillar in ["庚申", "辛酉"]
    elif current_season == 2:
        return day_pillar in ["壬子", "癸亥"]
    elif current_season == 3:
        return day_pillar in ["甲寅", "乙卯"]
    elif current_season == 4:
        return day_pillar in ["丙午", "丁巳"]
