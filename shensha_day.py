import constant
import rules
########## -----日柱相關神煞----- ##########
# 這類神煞以日柱（日干 + 日支）或日柱中的特定部分作為判斷基準。
# 日柱相關神煞可能需要完整的 reference_stem + reference_branch。

########## 魁罡 ##########
# 魁罡日：庚辰, 庚戌, 壬辰, 戊戌
def Fui_Gong(day_stem, day_branch):
    day_pillar = day_stem + day_branch
    return day_pillar in [
        "庚辰",
        "庚戌",
        "壬辰",
        "戊戌"
    ]


########## 陰差陽錯 ##########
# 陰差陽錯日：丙子, 丁丑, 戊寅, 辛卯, 壬辰, 癸巳, 丙午, 丁未, 戊申, 辛酉, 壬戌, 癸亥
def Yam_Caa_Yeung_Co(day_stem, day_branch):
    day_pillar = day_stem + day_branch
    return day_pillar in [
        "丙子", "丁丑", "戊寅",
        "辛卯", "壬辰", "癸巳",
        "丙午", "丁未", "戊申",
        "辛酉", "壬戌", "癸亥"
    ]


########## 十惡大敗 ##########
# 十惡大敗日：甲辰, 乙巳, 丙申, 丁亥, 戊戌, 己丑, 庚辰, 辛巳, 壬申, 癸亥
def Sap_Ok_Daai_Baai(day_stem, day_branch):
    day_pillar = day_stem + day_branch
    return day_pillar in [
        "甲辰", "乙巳", "丙申", "丁亥", "戊戌",
        "己丑", "庚辰", "辛巳", "壬申", "癸亥"
    ]

########## 空亡（旬空） ##########
# 空亡以完整日柱為基準。
# 六旬：
# 甲子旬 -> 戌亥空
# 甲戌旬 -> 申酉空
# 甲申旬 -> 午未空
# 甲午旬 -> 辰巳空
# 甲辰旬 -> 寅卯空
# 甲寅旬 -> 子丑空

# 若日干 index = stem_index，日支 index = branch_index，
# 則該日柱所在旬的「甲日地支」為： xun_start = (branch_index - stem_index) % 12
# 每旬共有十個干支，因此剩下的兩個地支即為空亡：
# void_1 = (xun_start - 2) % 12, void_2 = (xun_start - 1) % 12
def Hung_Mong(day_stem, day_branch):
    stem_index = constant.ten_stems.index(day_stem)
    branch_index = constant.twelve_branches.index(day_branch)
    xun_start = (branch_index - stem_index) % 12
    void_1 = (xun_start - 2) % 12
    void_2 = (xun_start - 1) % 12
    return [
        constant.twelve_branches[void_1],
        constant.twelve_branches[void_2]
    ]

########## 孤鸞 ##########
# 孤鸞日：甲寅、乙巳、丙午、丁巳、戊午、戊申、辛亥、壬子
# 注：孤鸞的取法不同資料存在少量差異，
# 此處採用以上八日版本。
def Gu_Luen(day_stem, day_branch):
    day_pillar = day_stem + day_branch
    return day_pillar in ["甲寅", "乙巳", "丙午", "丁巳",
        "戊午", "戊申", "辛亥", "壬子"]


########## 八專 ##########
# 八專日：甲寅、乙卯、丁未、己未、庚申、辛酉、戊戌、癸丑
def Baat_Zyun(day_stem, day_branch):
    day_pillar = day_stem + day_branch
    return day_pillar in [
        "甲寅", "乙卯", "丁未", "己未",
        "庚申", "辛酉", "戊戌", "癸丑"]


########## 九醜 ##########
# 九醜日：壬子, 壬午, 戊子, 戊午, 己酉, 己卯, 乙卯, 辛酉, 辛卯
def Gau_Cau(day_stem, day_branch):
    day_pillar = day_stem + day_branch
    return day_pillar in ["壬子", "壬午", "戊子", "戊午",
        "己酉", "己卯", "乙卯", "辛酉", "辛卯"]