import constant

# 判斷兩個五行之間的關係 （a, b）
#  0 = 同
# +1 = a 生 b
# +2 = a 剋 b
# -1 = b 生 a
# -2 = b 剋 a
def element_relation(element_a, element_b):
    if element_a == element_b:
        return 0
    if constant.element_generate(element_a) == element_b: #a 生 b
        return 1
    if constant.element_consume(element_a) == element_b:  #a 剋 b
        return 2
    if constant.element_generate(element_b) == element_a: #b 生 a
        return -1
    if constant.element_consume(element_b) == element_a:  #b 剋 a
        return -2

# 判斷兩個天干的五行關係
def stem_element_relation(stem_a, stem_b):
    element_a = constant.stems_elements(stem_a)
    element_b = constant.stems_elements(stem_b)
    return element_relation(element_a, element_b)

# 判斷兩個天干的陰陽關係
# 0 = 同陰陽
# 1 = 異陰陽
def stem_YamYeung_relation(stem_a, stem_b):
    YamYeung_a = constant.stem_YamYeung(stem_a)
    YamYeung_b = constant.stem_YamYeung(stem_b)
    return (YamYeung_a + YamYeung_b) % 2

########## 十神 ##########
# 十神以日干（日主）為基準，判斷其他天干與日干之間的關係
# 十神由兩層關係決定：五行關係，陰陽關係
#
#    五行生剋關係
#    element_rel 使用以下定義：
#     0 = 同我  -> 比劫
#    +1 = 我生  -> 食傷
#    +2 = 我剋  -> 財星
#    -2 = 剋我  -> 官殺
#    -1 = 生我  -> 印星
#
#    五行關係先決定十神所屬的五個大類：
#
#    比劫 = 比肩 + 劫財
#    食傷 = 食神 + 傷官
#    財星 = 偏財 + 正財
#    官殺 = 七殺（偏官）+ 正官
#    印星 = 偏印 + 正印
#
#    五行關係 + 陰陽關係共同決定具體十神：
#
#    同陰陽 (0)      異陰陽 (1)
#      比肩             劫財
#      食神             傷官
#      偏財             正財
#      七殺             正官
#      偏印             正印
#
# 五行關係 -> 決定十神大類
# 陰陽關係 -> 決定該大類中的具體十神
def ten_god_group(day_stem, target_stem):
    element_rel = stem_element_relation(day_stem, target_stem)
    if element_rel == 0:
        return "比劫"
    if element_rel == 1:
        return "食傷"
    if element_rel == 2:
        return "財星"
    if element_rel == -2:
        return "官殺"
    if element_rel == -1:
        return "印星"
    return None

def ten_god(day_stem, target_stem):
    god_group = ten_god_group(day_stem, target_stem)  #五大類
    YamYeung_rel = stem_YamYeung_relation(day_stem, target_stem)  #陰陽關係
    if god_group == "比劫":
        return "比肩" if YamYeung_rel == 0 else "劫財"
    if god_group == "食傷":
        return "食神" if YamYeung_rel == 0 else "傷官"
    if god_group == "財星"       :
        return "偏財" if YamYeung_rel == 0 else "正財"
    if god_group == "官殺":
        return "七殺" if YamYeung_rel == 0 else "正官"
    if god_group == "印星":
        return "偏印" if YamYeung_rel == 0 else "正印"
    return None

########## 天干五合 ##########
# 天干五合：
# 甲己合土
# 乙庚合金
# 丙辛合水
# 丁壬合木
# 戊癸合火
#
# 天干順序：甲 乙 丙 丁 戊 己 庚 辛 壬 癸
# 表示兩個天干相合
def stem_five_relation(stem_a, stem_b):
    index_a = constant.ten_stems.index(stem_a)
    index_b = constant.ten_stems.index(stem_b)
    return (index_b - index_a) % 10 == 5 #天干五合的規則是兩個天干的位置相差5

# 返回天干五合所對應的五行
# 甲己 -> 土
# 乙庚 -> 金
# 丙辛 -> 水
# 丁壬 -> 木
# 戊癸 -> 火
def stem_five_element(stem_a, stem_b):
    if not stem_five_relation(stem_a, stem_b): #如果兩個天干不五合，返回 None
        return None
    index = constant.ten_stems.index(stem_a)
    # five_elements = ["木", "火", "土", "金", "水"]
    element_index = (index % 5 + 2) % 5
    return constant.five_elements[element_index]

########### 地支六沖 ###########
# 地支六沖：
# 子午相沖
# 丑未相沖
# 寅申相沖
# 卯酉相沖
# 辰戌相沖
# 巳亥相沖
#
# 子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥
# 相沖的兩個地支在十二地支循環中相距 6 位，
def branch_six_clash_relation(branch_a, branch_b):
    index_a = constant.twelve_branches.index(branch_a)
    index_b = constant.twelve_branches.index(branch_b)
    return (index_b - index_a) % 12 == 6 #地支六沖的規則是兩個地支的位置相差6


############ 地支六合 ###########
# 地支六合：
# 子丑合土
# 寅亥合木
# 卯戌合火
# 辰酉合金
# 巳申合水
# 午未合土
def branch_six_combine_relation(branch_a, branch_b):
    index_a = constant.twelve_branches.index(branch_a)
    index_b = constant.twelve_branches.index(branch_b)
    return (index_b + index_a) % 12 == 1

def branch_six_combine_element(branch_a, branch_b):
    if not branch_six_combine_relation(branch_a, branch_b):
        return None
    if branch_a in ["子", "丑", "午", "未"]:
        return "土"
    if branch_a in ["寅", "亥"]:
        return "木"
    if branch_a in ["卯", "戌"]:
        return "火"
    if branch_a in ["辰", "酉"]:
        return "金"
    if branch_a in ["巳", "申"]:
        return "水"

########## 地支三合 ##########
# 申子辰合水
# 亥卯未合木
# 寅午戌合火
# 巳酉丑合金
# 沒有土
#
# 十二地支順序：
# 子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥
#
# 每一组三合中的三個地支，在十二地支循環中位置相差 4
# 完整三合需要三個不同的地支全部出現
# 只有其中兩個時屬於三合中的兩支，不等於完整三合
def branch_three_combine_relation(branch_a, branch_b, branch_c):
    if len({branch_a, branch_b, branch_c}) != 3:
        return False
    index_a = constant.twelve_branches.index(branch_a)
    index_b = constant.twelve_branches.index(branch_b)
    index_c = constant.twelve_branches.index(branch_c)
    return (index_a % 4 == index_b % 4 == index_c % 4) #三合的三個地支在十二地支循環中每隔4位出現，因此 index % 4 相同

def branch_three_combine_element(branch_a, branch_b, branch_c):
    # 根據三合的地支返回五行
    # 申子辰 -> 水
    # 亥卯未 -> 木
    # 寅午戌 -> 火
    # 巳酉丑 -> 金
    if not branch_three_combine_relation(branch_a, branch_b, branch_c):
        return None
    index = constant.twelve_branches.index(branch_a)
    # 接下來根據 index % 4 判斷：0 -> 水, 1 -> 金, 2 -> 火, 3 -> 木
    if index % 4 == 0:
        return "水"
    elif index % 4 == 1:
        return "金"
    elif index % 4 == 2:
        return "火"
    else:
        return "木"

########## 地支三會 ##########
# 地支三會：
# 寅卯辰會木
# 巳午未會火
# 申酉戌會金
# 亥子丑會水
#
# 子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥
#
# 因此三個地支必須互不相同，
# 並且能在十二地支循環中排列成連續三個位置。
def branch_three_meeting_relation(branch_a, branch_b, branch_c):
    if len({branch_a, branch_b, branch_c}) != 3:
        return False
    index_a = constant.twelve_branches.index(branch_a)
    index_b = constant.twelve_branches.index(branch_b)
    index_c = constant.twelve_branches.index(branch_c)
    indices = sorted([index_a, index_b, index_c])
    # 亥子丑：11, 0, 1
    if indices == [0, 1, 11]:
        return True
    #三會的三個地支在十二地支循環中連續排列，因此排序後相鄰的兩個索引差為1
    return (indices[1] - indices[0] == 1) and (indices[2] - indices[1] == 1) 

def branch_three_meeting_element(branch_a, branch_b, branch_c):
    if not branch_three_meeting_relation(branch_a, branch_b, branch_c):
        return None
    # 寅卯辰 -> 木
    # 巳午未 -> 火
    # 申酉戌 -> 金
    # 亥子丑 -> 水
    if branch_a in ["寅", "卯", "辰"]:
        return "木"
    elif branch_a in ["巳", "午", "未"]:
        return "火"
    elif branch_a in ["申", "酉", "戌"]:
        return "金"
    else:
        return "水"

########## 地支六害 ##########
# 地支六害：
# 子未相害
# 丑午相害
# 寅巳相害
# 卯辰相害
# 申亥相害
# 酉戌相害
#
# 子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥
# 0  1  2  3  4  5  6  7  8  9  10 11
# 六害的 index 之和：
# 子未：0 + 7  = 7
# 丑午：1 + 6  = 7
# 寅巳：2 + 5  = 7
# 卯辰：3 + 4  = 7
# 申亥：8 + 11 = 19
# 酉戌：9 + 10 = 19
# 19 % 12 = 7，

def branch_six_harm_relation(branch_a, branch_b):
    index_a = constant.twelve_branches.index(branch_a)
    index_b = constant.twelve_branches.index(branch_b)
    return (index_a + index_b) % 12 == 7

########## 地支六破 ##########
# 地支六破：
# 子酉相破
# 丑辰相破
# 寅亥相破
# 卯午相破
# 巳申相破
# 未戌相破
def branch_six_break_relation(branch_a, branch_b):
    break_pairs = [{"子", "酉"}, {"丑", "辰"}, {"寅", "亥"}, {"卯", "午"}, {"巳", "申"}, {"未", "戌"}]
    return {branch_a, branch_b} in break_pairs


########## 地支相刑 ##########
# 地支相刑：
# 1. 寅巳申三刑（無恩之刑） 寅、巳、申三支構成三刑
# 2. 丑未戌三刑（恃勢之刑） 丑、未、戌三支構成三刑
# 3. 子卯相刑  （無禮之刑） 子、卯互刑
# 4. 自刑                辰辰,午午,酉酉,亥亥
def branch_punishment(branches):
    punishments = []  # 可能有子卯、自刑同時存在的情況
    branch_set = set(branches)
    if {"寅", "巳", "申"}.issubset(branch_set):
        punishments.append("寅巳申")
    if {"丑", "未", "戌"}.issubset(branch_set):
        punishments.append("丑未戌")
    if {"子", "卯"}.issubset(branch_set):
        punishments.append("子卯")
    for branch in ["辰", "午", "酉", "亥"]:
        if branches.count(branch) >= 2:
            punishments.append(branch + "自刑")
    return punishments