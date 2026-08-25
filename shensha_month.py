import constant
import rules
########## 月令相關神煞 ##########
# 月令相關神煞以出生月支（月令）作為判斷基準。


########## 天德貴人 ##########
# 正丁二坤（申）宮，三壬四辛同，五亥六甲上，七癸八艮（寅）逢，九丙十居乙，子（十一）巳丑（十二）庚中。
# 天德貴人的返回值有時是天干、有時是地支
def Tin_Dak(reference_branch):
    tin_dak = {
        "寅": "丁",
        "卯": "申",
        "辰": "壬",
        "巳": "辛",
        "午": "亥",
        "未": "甲",
        "申": "癸",
        "酉": "寅",
        "戌": "丙",
        "亥": "乙",
        "子": "巳",
        "丑": "庚"
    }
    return tin_dak.get(reference_branch)

########## 月德貴人 ##########
# 月德貴人以月支為基準：
# 寅午戌 -> 火局 -> 丙
# 申子辰 -> 水局 -> 壬
# 亥卯未 -> 木局 -> 甲
# 巳酉丑 -> 金局 -> 庚
# 月德貴人返回天干。
def Yuet_Tak(reference_branch):
    element = rules.branch_three_combine_group_element(reference_branch)
    if element == "火":
        return "丙"
    elif element == "水":
        return "壬"
    elif element == "木":
        return "甲"
    elif element == "金":
        return "庚"
    return None

########## 天醫 ##########
# 天醫以月支為基準
# 寅->丑 卯->寅 辰->卯 巳->辰 午->巳 未->午 申->未 酉->申 戌->酉 亥->戌 子->亥 丑->子
# 即天醫位於月支前一位：(month_branch_index - 1) % 12
def Tin_Ji(reference_branch):
    index = constant.twelve_branches.index(reference_branch)
    return constant.twelve_branches[(index - 1) % 12]

########## 德秀貴人 ##########
# 德秀貴人以月支為基準：
# 寅午戌 -> 德：丙丁；秀：戊癸
# 申子辰 -> 德：壬癸戊己；秀：丙辛甲己
# 巳酉丑 -> 德：庚辛；秀：乙庚
# 亥卯未 -> 德：甲乙；秀：丁壬
def Dak_Sau(reference_branch):
    element = rules.branch_three_combine_group_element(reference_branch)
    if element == "火":
        return {
            "德": ["丙", "丁"],
            "秀": ["戊", "癸"]
        }
    elif element == "水":
        return {
            "德": ["壬", "癸", "戊", "己"],
            "秀": ["丙", "辛", "甲", "己"]
        }
    elif element == "金":
        return {
            "德": ["庚", "辛"],
            "秀": ["乙", "庚"]
        }
    elif element == "木":
        return {
            "德": ["甲", "乙"],
            "秀": ["丁", "壬"]
        }
    return None
