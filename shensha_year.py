import constant
import rules
########## -----年支相關神煞----- ##########
# 此類神煞以年支作為 reference_branch。
# 本部分包括：紅鸞,天喜,孤辰,寡宿,喪門,弔客,歲破,披麻,官符,白虎 

########## 紅鸞 ##########
# 紅鸞以年支為基準：
# 子 -> 卯
# 丑 -> 寅
# 寅 -> 丑
# 卯 -> 子
# 辰 -> 亥
# 巳 -> 戌
# 午 -> 酉
# 未 -> 申
# 申 -> 未
# 酉 -> 午
# 戌 -> 巳
# 亥 -> 辰
# 若 reference_branch 的 index = i，則紅鸞所在地支 index 為 (3 - i) % 12
def Hung_Luen(reference_branch):
    index = constant.twelve_branches.index(reference_branch)
    return constant.twelve_branches[(3 - index) % 12]

########## 天喜 ##########
# 天喜以年支為基準。天喜位於紅鸞的對沖位置，即兩者地支 index 相差 6。
# 紅鸞 -> 天喜
# 卯 -> 酉
# 寅 -> 申
# 丑 -> 未
# 子 -> 午
# 亥 -> 巳
# 戌 -> 辰
# 酉 -> 卯
# 申 -> 寅
# 未 -> 丑
# 午 -> 子
# 巳 -> 亥
# 辰 -> 戌
# 因此如果紅鸞所在地支 index = i，則天喜所在地支 index 為： (i + 6) % 12
def Tin_Hei(reference_branch):
    red_branch = Hung_Luen(reference_branch)
    index = constant.twelve_branches.index(red_branch)
    return constant.twelve_branches[(index + 6) % 12]


########## 孤辰、寡宿 ##########
# 孤辰、寡宿以年支為基準：
# 亥子丑 -> 孤辰在寅，寡宿在戌
# 寅卯辰 -> 孤辰在巳，寡宿在丑
# 巳午未 -> 孤辰在申，寡宿在辰
# 申酉戌 -> 孤辰在亥，寡宿在未
# 四組地支按三會的季節順序排列：
# group = 0 -> 寅卯辰, group = 1 -> 巳午未, group = 2 -> 申酉戌, group = 3 -> 亥子丑
# 若 reference_branch 的 index = i，可先計算：group = ((i - 2) % 12) // 3
# 孤辰所在地支 index：(5 + 3 * group) % 12
# 寡宿所在地支 index：(1 + 3 * group) % 12
def Gu_San(reference_branch): #孤辰
    index = constant.twelve_branches.index(reference_branch)
    group = ((index - 2) % 12) // 3
    return constant.twelve_branches[(5 + 3 * group) % 12]

def Gwa_Suk(reference_branch): #寡宿
    index = constant.twelve_branches.index(reference_branch)
    group = ((index - 2) % 12) // 3
    return constant.twelve_branches[(1 + 3 * group) % 12]

########## 喪門、弔客 ##########
# 以年支 index = i：
# 喪門 -> (i + 2) % 12
# 弔客 -> (i - 2) % 12
def Sang_Mun(reference_branch):
    index = constant.twelve_branches.index(reference_branch)
    return constant.twelve_branches[(index + 2) % 12]

def Diu_Haak(reference_branch):
    index = constant.twelve_branches.index(reference_branch)
    return constant.twelve_branches[(index - 2) % 12]


########## 歲破 ##########
# 歲破為年支的六沖位置：index + 6
def Seoi_Po(reference_branch):
    index = constant.twelve_branches.index(reference_branch)
    return constant.twelve_branches[(index + 6) % 12]


########## 披麻 ##########
# 披麻以年支為基準，位於年支後三位：
# index -> (index + 3) % 12
def Pei_Maa(reference_branch):
    index = constant.twelve_branches.index(reference_branch)
    return constant.twelve_branches[(index + 3) % 12]


########## 官符 ##########
# 官符以年支為基準，位於年支前四位：
# index -> (index + 4) % 12
def Gun_Fu(reference_branch):
    index = constant.twelve_branches.index(reference_branch)
    return constant.twelve_branches[(index + 4) % 12]


########## 白虎 ##########
# 白虎以年支為基準，位於年支前八位：
# index -> (index + 8) % 12
def Baak_Fu(reference_branch):
    index = constant.twelve_branches.index(reference_branch)
    return constant.twelve_branches[(index + 8) % 12]
