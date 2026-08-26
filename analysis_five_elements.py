import constant
import rules

########## /////----------基礎五行統計----------///// ##########
# 五行統計
def analyse_five_elements(four_pillars):
    counts = [0, 0, 0, 0, 0]  # 木、火、土、金、水
    for pillar in four_pillars.values():
        stem = pillar[0]
        branch = pillar[1]
        stem_element = constant.stems_elements(stem)
        branch_element = constant.branches_elements(branch)
        counts[constant.five_elements.index(stem_element)] += 1
        counts[constant.five_elements.index(branch_element)] += 1
    return counts

# 五行缺失
def elements_missing(four_pillars):
    missing = [] # 可能有多個缺失
    outcome = analyse_five_elements(four_pillars)
    for i in range(len(outcome)):
        if outcome[i] == 0:
            missing.append(i)
    return missing

# 五行數量最多的元素
def elements_most(four_pillars):
    outcome = analyse_five_elements(four_pillars)
    most = [] #可以同時存在多個
    maximum = max(outcome)
    for i in range(len(outcome)):
        if outcome[i] == maximum:
            most.append(i)
    return most

# 每個相應元素
def element_ratio(four_pillars):
    outcome = analyse_five_elements(four_pillars)
    return [count / 8 for count in outcome]

# 藏干五行統計
def analyse_hidden_elements(four_pillars):
    counts = [0, 0, 0, 0, 0]  # 木、火、土、金、水
    for pillar in four_pillars.values():
        branch = pillar[1]
        for stem in constant.hidden_stems(branch):
            element = constant.stems_elements(stem)
            index = constant.five_elements.index(element)
            counts[index] += 1
    return counts

########## /////----------通根分析----------///// ##########
# 通根 ： 某個天干的五行，在四個地支的藏干裡出現過同五行
# 判斷單一天干是否在四柱地支中通根
def stem_has_root(stem, four_pillars):
    stem_element = constant.stems_elements(stem)
    for pillar in four_pillars.values():
        branch = pillar[1]
        for hidden_stem in constant.hidden_stems(branch):
            hidden_element = constant.stems_elements(hidden_stem)
            if hidden_element == stem_element:
                return True
    return False

# 分別判斷年干、月干、日干、時干是否通根
def analyse_roots(four_pillars):
    roots = []
    for pillar in four_pillars.values():
        stem = pillar[0]
        roots.append(stem_has_root(stem, four_pillars))
    return roots

########## 根氣強度 ##########
# 判斷某一天干在四柱地支中的根氣。地支藏干按照 constant.hidden_stems() 的順序：
# 第一藏干（本氣）  -> 3
# 第二藏干（中氣）  -> 2
# 第三藏干（餘氣）  -> 1
# 無同五行藏干     -> 0
# 返回順序：[年支, 月支, 日支, 時支]
def root_strength(stem, four_pillars):
    stem_element = constant.stems_elements(stem)
    strengths = []
    for pillar in four_pillars.values():
        branch = pillar[1]
        hidden = constant.hidden_stems(branch)
        strength = 0
        for i in range(len(hidden)):
            hidden_element = constant.stems_elements(hidden[i])
            if hidden_element == stem_element:
                strength = 3 - i
                break
        strengths.append(strength)
    return strengths

########## 根氣位置加權 ##########
# root_strength() 返回：[年支, 月支, 日支, 時支]
# 位置權重可另外設定
# 加權後再求總和，作為日主得地程度的基礎分數
# PS：這些數值是程式模型的可調參數，並不是固定命理定律
root_position_weights = [0.7, 1.0, 1.0, 0.7] #[年支, 月支, 日支, 時支], 可調整
def weighted_root_strength(stem, four_pillars):
    strengths = root_strength(stem, four_pillars)
    weighted = []
    for i in range(len(strengths)):
        weighted.append(strengths[i] * root_position_weights[i])
    return weighted
def total_weighted_root_strength(stem, four_pillars):
    return sum(weighted_root_strength(stem, four_pillars))

########## 得令 ##########
# 得令以日主五行與月令（月支）五行之間的關係判斷
# 若月令與日主同五行，或月令生日主： -> 得令 True
def has_seasonal_support(four_pillars):
    day_stem = four_pillars["day"][0]
    month_branch = four_pillars["month"][1]
    day_element = constant.stems_elements(day_stem)
    month_element = constant.branches_elements(month_branch)
    relation = rules.element_relation(day_element, month_element)
    return relation in [0, -1] # 0表示同五行，-1表示月令生日主

########## 得地 ##########
# 得地主要看日主是否在四柱地支中有根。
# 若日干在任一地支藏干中找到相同五行，則視為日主得地，返回 True；
# 此處只判斷是否通根
def has_root_support(four_pillars):
    day_stem = four_pillars["day"][0]
    return stem_has_root(day_stem,four_pillars)

########## 整體生扶 ##########
# relation_strength：[官殺, 印星, 比劫, 食傷, 財星]
# 印星 + 比劫為生扶日主的力量；
# 官殺 + 食傷 + 財星為非生扶力量。
def has_overall_support(four_pillars):
    strengths = relation_strength(four_pillars)
    support = strengths[1] + strengths[2]
    non_support = strengths[0] + strengths[3] + strengths[4]
    return support > non_support

########## 得地分數 ##########
# total_weighted_root_strength() 同時考慮：
# 藏干層級：本氣 / 中氣 / 餘氣
# 地支位置：年 / 月 / 日 / 時
# 最大根氣 = 3 * sum(root_position_weights)
# 將結果 normalise 到 0 ~ 1
def root_score(four_pillars):
    day_stem = four_pillars["day"][0]
    raw_score = total_weighted_root_strength(day_stem, four_pillars)
    maximum = 3 * sum(root_position_weights)
    return raw_score / maximum


########## /////----------月令分析----------///// ##########
########## 旺相休囚死 ##########
# 根據日主五行與月令五行的關係，返回日主在月令中的旺相休囚死狀態
# element_relation(day_element, month_element):
#  0  -> 同我      -> 旺
# -1  -> 月令生我   -> 相
# +1  -> 我生月令   -> 休
# +2  -> 我剋月令   -> 囚
# -2  -> 月令剋我   -> 死
def seasonal_state(four_pillars):
    day_stem = four_pillars["day"][0]
    month_branch = four_pillars["month"][1]
    day_element = constant.stems_elements(day_stem)
    month_element = constant.branches_elements(month_branch)
    relation = rules.element_relation(day_element, month_element)
    # relation: -2, -1, 0, +1, +2
    # state:     死, 相, 旺, 休, 囚
    relation_state_index = [0, 3, 4, 2, 1]
    return constant.seasonal_states[relation_state_index[relation + 2]]

seasonal_state_scores = [0.0, 0.25, 0.5, 0.8, 1.0]
########## 得令分數 ##########
def season_score(four_pillars):
    state = seasonal_state(four_pillars)
    index = constant.seasonal_states.index(state)
    return seasonal_state_scores[index]


########## /////----------天干生扶分析----------///// ##########
########## 天干生扶分數 ##########
# 以日主五行為基準，分析其餘三個天干對日主的作用
stem_support_relation_score = [-1.0, 1.0, 1.0, -0.7, -0.5] # [剋我 生我 同我 我生 我剋]
def stem_support_score(four_pillars):
    day_stem = four_pillars["day"][0]
    day_element = constant.stems_elements(day_stem)
    score = 0
    for pillar_name, pillar in four_pillars.items():
        if pillar_name == "day":
            continue
        stem_element = constant.stems_elements(pillar[0])
        relation = rules.element_relation(day_element, stem_element)
        score += stem_support_relation_score[relation + 2]
    return score

########## 得勢分數 ##########
# stem_support_score() 只計算：年干、月干、時干
# 每個天干的分數範圍約為 -1 ~ +1，因此三個天干的總分理論範圍約為：-3 ~ +3
# 將其 normalize 到 0 ~ 1：
# -3 -> 0
#  0 -> 0.5
# +3 -> 1
def support_score(four_pillars):
    raw_score = stem_support_score(four_pillars)
    return (raw_score + 3) / 6

########## /////---------- 日主強弱基礎資料 ----------///// ##########
#八字命理中沒有一個「絕對數值」的量化公式
#decision tree，判斷強弱
def day_master_strength(four_pillars):
    season = season_score(four_pillars)
    root = root_score(four_pillars)
    support = support_score(four_pillars)
    # 極強
    if season >= 0.8 and root >= 0.6 and support >= 0.6:
        return constant.strength[4]
    # 極弱
    if season <= 0.25 and root <= 0.15 and support <= 0.4:
        return constant.strength[0]
    # 失令且無根，即使天干有生扶，仍然偏弱
    if season <= 0.25 and root <= 0.15:
        return constant.strength[1]
    # 得令，但完全無根且生扶不足
    if season >= 0.8 and root < 0.15 and support < 0.4:
        return constant.strength[1]
    # 得令，且有根或有天干生扶
    if season >= 0.8 and (root >= 0.35 or support >= 0.6):
        return constant.strength[3]
    # 失令，但根與天干都很強
    if season <= 0.5 and root >= 0.65 and support >= 0.65:
        return constant.strength[3]
    # 根與天干都很強
    if root >= 0.65 and support >= 0.65:
        return constant.strength[3]
    # 失令、根弱、生扶弱
    if season <= 0.5 and root < 0.35 and support < 0.5:
        return constant.strength[1]
    return constant.strength[2]

########## 從弱初步判斷 ##########
# 從弱的第一層條件：日主明顯失令, 日主幾乎無根, 天干印比生扶不足, 整體明面干支亦不以生扶日主為主
# 只判斷是否具備從格傾向, 不區分從財、從官殺、從兒等具體類型
# 就是日主極弱，以及沒有得勢
# 極弱且整體生扶不足 -> 從弱傾向
# 偏弱時必須完全無根，且整體生扶不足
# 中和及以上不考慮從弱
def weak_following_structure(four_pillars):
    strength = day_master_strength(four_pillars)
    if strength == constant.strength[0]:
        return not has_overall_support(four_pillars)
    if strength == constant.strength[1]:
        return (root_score(four_pillars) == 0 and not has_overall_support(four_pillars))
    return False

########## 從格力量 ##########
# 統計其餘七個干支與日主的五行關係
def relation_counts(four_pillars):
    counts = [0, 0, 0, 0, 0] # [剋我, 生我, 同我, 我生, 我剋]
    day_element = constant.stems_elements(four_pillars["day"][0])
    for pillar_name, pillar in four_pillars.items():
        stem_element = constant.stems_elements(pillar[0])
        branch_element = constant.branches_elements(pillar[1])
        if pillar_name != "day":
            stem_relation = rules.element_relation(day_element, stem_element)
            counts[stem_relation + 2] += 1
        branch_relation = rules.element_relation(day_element, branch_element)
        counts[branch_relation + 2] += 1
    return counts

########## 從格力量統計 ##########
# 統計其餘天干及四個地支藏干與日主的五行關係。
# 天干每個計 3 分。
# 地支藏干：本氣 -> 3 中氣 -> 2 餘氣 -> 1
# 日干本身不計入
def relation_strength(four_pillars):
    strengths = [0, 0, 0, 0, 0] # 返回順序：[剋我, 生我, 同我, 我生, 我剋]
    day_element = constant.stems_elements(four_pillars["day"][0]) #日干
    for pillar_name, pillar in four_pillars.items():
        stem, branch = pillar
        # 其餘三個天干
        if pillar_name != "day":
            stem_element = constant.stems_elements(stem)
            relation = rules.element_relation(day_element,stem_element)
            strengths[relation + 2] += 3
        # 地支藏干
        hidden = constant.hidden_stems(branch)
        for i in range(len(hidden)):
            hidden_element = constant.stems_elements(hidden[i])
            relation = rules.element_relation(day_element,hidden_element)
            strengths[relation + 2] += 3 - i
    return strengths

########## 從弱類型 ##########
# 剋我 -> 官殺, 生我 -> 印, 同我 -> 比劫, 我生 -> 食傷, 我剋 -> 財 ###十神五大類
# 日主極弱，只有從官殺，從兒，從財
# 官殺最大 -> 從官殺, 食傷最大 -> 從兒, 財最大 -> 從財
# 可以有多個答案
# 主勢佔三者總力量至少 50%，才判定具體從格
# 若不具備從弱條件返回 None；具備但主勢不明確返回空 list
def weak_following_type(four_pillars):
    if not weak_following_structure(four_pillars):
        return None
    types = []
    strengths = relation_strength(four_pillars)
    indexes = [0, 3, 4]
    string_type = ["從官殺", "從兒", "從財"]
    total = sum(strengths[i] for i in indexes)
    maximum = max(strengths[i] for i in indexes)
    # 防止三種力量全部為 0，同時要求主勢至少佔一半
    if total == 0 or maximum / total < 0.5:
        return []
    for i in range(len(string_type)):
        if strengths[indexes[i]] == maximum:
            types.append(string_type[i])
    return types

########## 從強 / 專旺初步判斷 ##########
# 日主極強，且整體明面干支以生扶日主為主，
# 視為具備從強或專旺的初步條件
def strong_following_structure(four_pillars):
    return (day_master_strength(four_pillars) == constant.strength[4] and has_overall_support(four_pillars))

########## 專旺判斷 ##########
# 日主極強, 比劫力量最強
# 具體類型在constant文件, 已按照五行順序排好
def dominant_structure(four_pillars):
    strengths = relation_strength(four_pillars)
    if not strong_following_structure(four_pillars):
        return None
    # 比劫可以和印星並列，但不能和異黨並列
    if not (strengths[2] >= strengths[1] 
        and strengths[2] > strengths[0]
        and strengths[2] > strengths[3]
        and strengths[2] > strengths[4]):
        return None
    day_element = constant.stems_elements(four_pillars["day"][0])
    index = constant.five_elements.index(day_element)
    return constant.dominant_structures[index]
    
########## 特殊格局 ##########
# 優先判斷專旺, 其次從強, 再判斷極弱從格, 普通命局返回 None
def special_structure(four_pillars):
    dominant = dominant_structure(four_pillars)
    if dominant is not None:
        return [dominant]
    if strong_following_structure(four_pillars):
        return ["從強"]
    if weak_following_structure(four_pillars):
        weak_type = weak_following_type(four_pillars)
        if weak_type:
            return weak_type
        return ["從弱"]  # 有從弱條件，但無明確單一主勢
    return None

########## 喜忌判斷 ##########
#普通身強  -> 喜洩、耗、剋 （偏強，極強）
#普通身弱  -> 喜生、扶。   （偏弱，極弱）
#從弱     -> 喜順從其主勢
#從強/專旺 -> 喜生扶、忌逆勢
#中和     -> 先不強行給單一喜忌
def normal_favourable_relations(four_pillars):  # 只處理普通命局
    special = special_structure(four_pillars)
    if special is not None:
        return None
    strength = day_master_strength(four_pillars)
    if strength in [constant.strength[3], constant.strength[4]]:
        return ["洩", "耗", "剋"]
    elif strength in [constant.strength[0], constant.strength[1]]:
        return ["生", "扶"]
    return []
# 從財, 從兒 -> 喜洩, 耗
# 從官殺     -> 喜耗, 剋
# 從強, 專旺 -> 喜生, 扶
# 多格並存   -> 合併去重
def special_favourable_relations(four_pillars):
    special = special_structure(four_pillars)
    if special is None:
        return None
    favourable = []
    for structure in special:
        if structure in ["從財", "從兒"]:
            relations = ["洩", "耗"]
        elif structure == "從官殺":
            relations = ["耗", "剋"]
        elif structure == "從強" or structure in constant.dominant_structures: #從強, 專旺
            relations = ["生", "扶"]
        elif structure == "從弱":
            return None
        else:
            continue
        for relation in relations: #合併, 去掉重複的
            if relation not in favourable:
                favourable.append(relation)
    return favourable

########## 喜的作用總入口 ##########
# 普通命局 -> normal_favourable_relations()
# 特殊格局 -> special_favourable_relations()
# 中和返回 []
# 無法判斷喜用的特殊格局返回 None
def favourable_relations(four_pillars):
    if special_structure(four_pillars) is None:
        return normal_favourable_relations(four_pillars)

    return special_favourable_relations(four_pillars)


# 喜的作用具體五行
# relation 0  → 扶 
# relation 1  → 洩 
# relation 2  → 耗 
# relation -2 → 剋 
# relation -1 → 生 
def favourable_elements(four_pillars):
    favours = favourable_relations(four_pillars)
    if favours is None:
        return None
    day_element = constant.stems_elements(four_pillars["day"][0])
    elements = []
    for element in constant.five_elements:
        relation = rules.element_relation(day_element, element)
        action = constant.five_element_actions[relation + 2]
        if action in favours:
            elements.append(element)
    return elements

## 忌
## 除了中和，喜忌完全互補
def unfavourable_relations(four_pillars):
    favours = favourable_relations(four_pillars)
    if favours is None:
        return None
    if favours == []:
        return []
    return [action for action in constant.five_element_actions if action not in favours]

def unfavourable_elements(four_pillars):
    unfavours = unfavourable_relations(four_pillars)
    if unfavours is None:
        return None
    day_element = constant.stems_elements(four_pillars["day"][0])
    elements = []
    for element in constant.five_elements:
        relation = rules.element_relation(day_element, element)
        action = constant.five_element_actions[relation + 2]
        if action in unfavours:
            elements.append(element)
    return elements
