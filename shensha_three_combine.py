import constant
import rules

########## -----三合局相關神煞----- ##########
# 桃花,驛馬,華蓋,將星,劫煞,亡神,災煞都可以根據 reference_branch 所屬的三合局判斷。
# 十二地支 index(0~11)：子 丑 寅 卯 辰 巳 午 未 申 酉 戌 亥
# 三合局可以根據地支 index % 4 分組, group = index % 4
# group0 -> 申子辰 -> 水局, group1 -> 巳酉丑 -> 金局, group2 -> 寅午戌 -> 火局, group3 -> 亥卯未 -> 木局
# 四種神煞與三合局的對應：
#             水    金    火   木
# 桃花         酉    午    卯   子
# 驛馬         寅    亥    申   巳
# 華蓋         辰    丑    戌   未
# 將星         子    酉    午   卯
# 劫煞         巳    寅    亥   申
# 亡神         亥    申    巳   寅
# 災煞         午    卯    子   酉
#
# 如果令 g = reference_branch_index % 4，
# 則四種神煞的地支 index 都可以表示為同一種模 12 線性形式：
#     shensha_index = (k - 3 * g) % 12， 不同神煞只需要使用不同的初始值 k：
# 桃花：k = 9
#     peach_index = (9 - 3 * g) % 12
#     -> 9, 6, 3, 0 -> 酉, 午, 卯, 子
# 驛馬：k = 2
#     horse_index = (2 - 3 * g) % 12
#     -> 2, 11, 8, 5 -> 寅, 亥, 申, 巳
# 華蓋：k = 4
#     canopy_index = (4 - 3 * g) % 12
#     -> 4, 1, 10, 7 -> 辰, 丑, 戌, 未
# 將星：k = 0
#     general_star_index = (0 - 3 * g) % 12
#     -> 0, 9, 6, 3 -> 子, 酉, 午, 卯
# 劫煞：k = 5
#     robbery_index = (5 - 3 * g) % 12
#     -> 5, 2, 11, 8 -> 巳, 寅, 亥, 申
# 亡神：k = 11
#     death_index = (11 - 3 * g) % 12
#     -> 11, 8, 5, 2 -> 亥, 申, 巳, 寅
# 災煞：k = 6
#     disaster_index = (6 - 3 * g) % 12
#     -> 6, 3, 0, 9 -> 午, 卯, 子, 酉

#通用函數
def three_combine_shensha(reference_branch, k):
    index = constant.twelve_branches.index(reference_branch)
    group = index % 4
    shensha_index = (k - 3 * group) % 12
    return constant.twelve_branches[shensha_index]

#桃花 
def Tou_Faa(reference_branch):
    return three_combine_shensha(reference_branch, 9)
#驛馬 
def Yik_Maa(reference_branch):
    return three_combine_shensha(reference_branch, 2)
#華蓋
def Waa_Goi(reference_branch):
    return three_combine_shensha(reference_branch, 4)
#將星 
def Zoeng_Sing(reference_branch):
    return three_combine_shensha(reference_branch, 0)
#劫煞
def Gip_Saat(reference_branch):
    return three_combine_shensha(reference_branch, 5)
#亡神
def Mong_San(reference_branch):
    return three_combine_shensha(reference_branch, 11)
#災煞
def Zoi_Saat(reference_branch):
    return three_combine_shensha(reference_branch, 6)
