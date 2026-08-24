# 10 天干
ten_stems = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 12 地支
twelve_branches = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 五行
five_elements = ["木", "火", "土", "金", "水"]

def stems_elements(stem):
    #根據天干返回五行
    #規則：甲乙屬木，丙丁屬火，戊己屬土，庚辛屬金，壬癸屬水
    for i in range(len(ten_stems)):
        if stem == ten_stems[i]:
            return five_elements[i//2] # 每兩個天干對應一個五行
    return None # 如果輸入的天干不在列表中，返回 None

def branches_elements(branch):
    #根據地支返回五行
    #規則：寅卯屬木，巳午屬火，辰戌丑未屬土，申酉屬金，亥子屬水
    if branch in ["寅", "卯"]:
        return "木"
    elif branch in ["巳", "午"]:
        return "火"
    elif branch in ["辰", "戌", "丑", "未"]:
        return "土"
    elif branch in ["申", "酉"]:
        return "金"
    elif branch in ["亥", "子"]:
        return "水"
    else:
        return None # 如果輸入的地支不在列表中，返回 None

def stems_branches_elements(stem, branch):
    #根據天干和地支返回五行
    stem_element = stems_elements(stem)
    branch_element = branches_elements(branch)
    if stem_element and branch_element:
        return [stem_element, branch_element]
    else:
        return None # 如果天干或地支不在列表中，返回 None

def element_generate(element):
    #五行相生
    #規則：木生火，火生土，土生金，金生水，水生木
    for i in range(len(five_elements)):
        if element == five_elements[i]:
            return five_elements[(i + 1) % len(five_elements)]
    return None # 如果輸入的五行不在列表中，返回 None

def element_consume(element):
    #五行相剋
    #規則：木剋土，土剋水，水剋火，火剋金，金剋木
    for i in range(len(five_elements)):
        if element == five_elements[i]:
            return five_elements[(i + 2) % len(five_elements)]
    return None # 如果輸入的五行不在列表中，返回 None

# define 陽 = 1, 陰 = 0
def stem_YamYeung(stem):
    #天干陰陽
    #規則：甲丙戊庚壬為陽，乙丁己辛癸為陰
    for i in range(len(ten_stems)):
        if stem == ten_stems[i]:
            return 1 if i % 2 == 0 else 0
    return None # 如果輸入的天干不在列表中，返回 None

def branch_YamYeung(branch):
    #地支陰陽
    #規則：子寅辰午申戌為陽，丑卯巳未酉亥為陰
    for i in range(len(twelve_branches)):
        if branch == twelve_branches[i]:
            return 1 if i % 2 == 0 else 0
    return None # 如果輸入的地支不在列表中，返回 None


