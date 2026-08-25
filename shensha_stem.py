import constant
import rules
########## -----天干相關神煞 ----- ##########
# 天干相關神煞以天干作為判斷基準，通常以日干（部分規則也可能使用年干）查找對應的地支。
# 直接根據 reference_stem 找到對應的神煞地支。
# 各神煞的具體取法及使用年干或日干作為基準，在各自的 function 中分別處理。function 接受一個 reference_stem，返回該天干所對應的地支。

########## 祿神 ##########
# 祿神以天干為基準：
# 甲 -> 寅
# 乙 -> 卯
# 丙 -> 巳
# 丁 -> 午
# 戊 -> 巳
# 己 -> 午
# 庚 -> 申
# 辛 -> 酉
# 壬 -> 亥
# 癸 -> 子
def Lok_San(reference_stem):
    index = constant.ten_stems.index(reference_stem)
    element = constant.stems_elements(reference_stem)
    if element == "木":
        return constant.twelve_branches[(index + 2) % 12]  # 甲->寅，乙->卯
    elif element == "火":
        return constant.twelve_branches[(index + 3) % 12]  # 丙->巳，丁->午
    elif element == "土":
        return constant.twelve_branches[(index + 1) % 12]  # 戊->巳，己->午
    elif element == "金":
        return constant.twelve_branches[(index + 2) % 12]  # 庚->申，辛->酉
    elif element == "水":
        return constant.twelve_branches[(index + 3) % 12]  # 壬->亥，癸->子
    return None

########## 羊刃 ##########
# 羊刃以天干為基準：
# 甲 -> 卯
# 乙 -> 寅
# 丙 -> 午
# 丁 -> 巳
# 戊 -> 午
# 己 -> 巳
# 庚 -> 酉
# 辛 -> 申
# 壬 -> 子
# 癸 -> 亥
def Yeung_Jan(reference_stem):
    luck_branch = Lok_San(reference_stem)
    index = constant.twelve_branches.index(luck_branch)
    if constant.stem_YamYeung(reference_stem) == 1:
        return constant.twelve_branches[(index + 1) % 12]  # 陽干：祿神後一位
    else:
        return constant.twelve_branches[(index - 1) % 12]  # 陰干：祿神前一位

########## 天乙貴人 ##########
# 天乙貴人以天干為基準：（返回兩個地支）
# 甲, 戊, 庚 -> 丑, 未
# 乙, 己     -> 子, 申
# 丙, 丁     -> 亥, 酉
# 辛        -> 午, 寅
# 壬, 癸     -> 卯, 巳
def Tin_Yuet(reference_stem):
    if reference_stem in ["甲", "戊", "庚"]:
        return ["丑", "未"]
    elif reference_stem in ["乙", "己"]:
        return ["子", "申"]
    elif reference_stem in ["丙", "丁"]:
        return ["亥", "酉"]
    elif reference_stem == "辛":
        return ["午", "寅"]
    elif reference_stem in ["壬", "癸"]:
        return ["卯", "巳"]
    return None

########## 文昌貴人 ##########
# 文昌貴人以天干為基準：
# 甲 -> 巳
# 乙 -> 午
# 丙 -> 申
# 丁 -> 酉
# 戊 -> 申
# 己 -> 酉
# 庚 -> 亥
# 辛 -> 子
# 壬 -> 寅
# 癸 -> 卯
def Man_Cheung(reference_stem):
    index = constant.ten_stems.index(reference_stem)
    element = constant.stems_elements(reference_stem)
    if element == "木":
        return constant.twelve_branches[(index + 5) % 12]  # 甲->巳，乙->午
    elif element == "火":
        return constant.twelve_branches[(index + 6) % 12]  # 丙->申，丁->酉
    elif element == "土":
        return constant.twelve_branches[(index + 4) % 12]  # 戊->申，己->酉
    elif element == "金":
        return constant.twelve_branches[(index + 5) % 12]  # 庚->亥，辛->子
    elif element == "水":
        return constant.twelve_branches[(index + 6) % 12]  # 壬->寅，癸->卯
    return None

########## 金輿 ##########
# 金輿以天干為基準：
# 甲->辰 乙->巳 丙戊->未 丁己->申 庚->戌 辛->亥 壬->丑 癸->寅
def Gam_Jyu(reference_stem):
    gam_jyu = {
        "甲": "辰", "乙": "巳",
        "丙": "未", "丁": "申",
        "戊": "未", "己": "申",
        "庚": "戌", "辛": "亥",
        "壬": "丑", "癸": "寅"
    }
    return gam_jyu.get(reference_stem)


########## 學堂 ##########
# 學堂以天干五行為基準：
# 木->亥 火->寅 土->申 金->巳 水->申
def Hok_Tong(reference_stem):
    element = constant.stems_elements(reference_stem)
    if element == "木":
        return "亥"
    elif element == "火":
        return "寅"
    elif element == "土":
        return "申"
    elif element == "金":
        return "巳"
    elif element == "水":
        return "申"
    return None

########## 詞館 ##########
# 詞館以天干五行為基準：
# 木->寅 火->巳 土->亥 金->申 水->亥
def Ci_Gun(reference_stem):
    element = constant.stems_elements(reference_stem)
    if element == "木":
        return "寅"
    elif element == "火":
        return "巳"
    elif element == "土":
        return "亥"
    elif element == "金":
        return "申"
    elif element == "水":
        return "亥"
    return None

########## 太極貴人 ##########
# 甲乙 -> 子, 午
# 丙丁 -> 卯, 酉
# 戊己 -> 辰, 戌, 丑, 未
# 庚辛 -> 寅, 亥
# 壬癸 -> 巳, 申
# 返回 list，因為一個天干可能對應多個地支。
def Taai_Gik(reference_stem):
    if reference_stem in ["甲", "乙"]:
        return ["子", "午"]
    elif reference_stem in ["丙", "丁"]:
        return ["卯", "酉"]
    elif reference_stem in ["戊", "己"]:
        return ["辰", "戌", "丑", "未"]
    elif reference_stem in ["庚", "辛"]:
        return ["寅", "亥"]
    elif reference_stem in ["壬", "癸"]:
        return ["巳", "申"]
    return None

########## 國印貴人 ##########
# 國印位於祿神地支往後 4 位：
# 國印index = (祿神index - 4) % 12
def Gwok_Yan(reference_stem):
    lu_branch = Lok_San(reference_stem)
    index = constant.twelve_branches.index(lu_branch)
    return constant.twelve_branches[(index - 4) % 12]

########## 福星貴人 ##########
# 甲丙 -> 寅子 乙癸 -> 卯丑 戊->申 己->未 丁->亥 庚->午 辛->巳 壬->辰
def Fuk_Sing(reference_stem):
    fuk_sing = {
        "甲": ["寅", "子"],
        "乙": ["卯", "丑"],
        "丙": ["寅", "子"],
        "丁": ["亥"],
        "戊": ["申"],
        "己": ["未"],
        "庚": ["午"],
        "辛": ["巳"],
        "壬": ["辰"],
        "癸": ["卯", "丑"]
    }
    return fuk_sing.get(reference_stem)

########## 天廚貴人 ##########
# 天廚 = 食神之祿
# 食神天干： (stem_index + 2) % 10, 再取該食神天干的祿神地支
def Tin_Cyu(reference_stem):
    index = constant.ten_stems.index(reference_stem)
    food_god_stem = constant.ten_stems[(index + 2) % 10]
    return Lok_San(food_god_stem)
