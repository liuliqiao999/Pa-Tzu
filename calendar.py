import constant
import datetime
import sxtwl

# 日期
def create_solar_date(year, month, day):
    return datetime.date(year, month, day)

# 陽曆轉農曆
def solar_to_lunar(solar_date):
    day = sxtwl.fromSolar(solar_date.year, solar_date.month, solar_date.day)
    return (day.getLunarYear(), day.getLunarMonth(), day.getLunarDay())

########## 年柱 ##########
# 得到年份天干地支（年柱，以立春為界）
def get_year_gz(solar_date):
    day = sxtwl.fromSolar(solar_date.year, solar_date.month, solar_date.day)
    year_gz = day.getYearGZ()
    return (constant.ten_stems[year_gz.tg], constant.twelve_branches[year_gz.dz])

# 年份天干（年干）
def get_year_stem(solar_date):
    return get_year_gz(solar_date)[0]

# 年份地支（年支）
def get_year_branch(solar_date):
    return get_year_gz(solar_date)[1]


########## 月柱 ##########
def get_month_branch(solar_date):
    day = sxtwl.fromSolar(solar_date.year, solar_date.month, solar_date.day)
    month_gz = day.getMonthGZ()
    return constant.twelve_branches[month_gz.dz]

## 當然也可以用constant.ten_stems[month_gz.tg]直接得到月干，但這裡是為了展示五虎遁的計算方法
# 五虎遁：根據年干和月支計算月干
# 口訣： 甲己之年丙作首，乙庚之歲戊為頭，丙辛必定尋庚起，丁壬壬位順行流，若問戊癸何方發，甲寅之上好追求。
# 規則：
# 甲、己年 -> 丙寅起
# 乙、庚年 -> 戊寅起
# 丙、辛年 -> 庚寅起
# 丁、壬年 -> 壬寅起
# 戊、癸年 -> 甲寅起
# 月支從寅開始依次為：
# 寅=0, 卯=1, 辰=2, ..., 丑=11
def month_stem(year_stem, month_branch):
    month_offset = (constant.twelve_branches.index(month_branch) - 2) % 12
    a = constant.ten_stems.index(year_stem)
    index = (2 * a + 2 + month_offset) % 10
    return constant.ten_stems[index]

# 月份天干地支（月柱）
def get_month_gz(solar_date):
    year_stem = get_year_stem(solar_date)
    month_branch = get_month_branch(solar_date)
    return (month_stem(year_stem, month_branch), month_branch)

# 月份天干（月干）
def get_month_stem(solar_date):
    return get_month_gz(solar_date)[0]


########## 日柱 ##########
# 日期天干地支（日柱）
def get_day_gz(solar_date):
    day = sxtwl.fromSolar(solar_date.year, solar_date.month, solar_date.day)
    day_gz = day.getDayGZ()
    return (constant.ten_stems[day_gz.tg], constant.twelve_branches[day_gz.dz])

# 日期天干（日干）
def get_day_stem(solar_date):
    return get_day_gz(solar_date)[0]


# 日期地支（日支）
def get_day_branch(solar_date):
    return get_day_gz(solar_date)[1]


########### 時柱 ##########
# 根據出生時間計算時支
# 子時：23:00 - 00:59
# 丑時：01:00 - 02:59
# 寅時：03:00 - 04:59
# 卯時：05:00 - 06:59
# 辰時：07:00 - 08:59
# 巳時：09:00 - 10:59
# 午時：11:00 - 12:59
# 未時：13:00 - 14:59
# 申時：15:00 - 16:59
# 酉時：17:00 - 18:59
# 戌時：19:00 - 20:59
# 亥時：21:00 - 22:59
def get_hour_branch(birth_time):
    hour = birth_time.hour
    index = ((hour + 1) // 2) % 12
    return constant.twelve_branches[index]


# 根據是否採用「子時換日」規則，
# 決定計算日干時實際使用的日期
# zi_hour_change = True
#   採用子時換日：
#   23:00 起視為翌日
# zi_hour_change = False
#   不採用子時換日：
#   日期於 00:00 正常切換
def get_effective_date(birth_date, birth_time, zi_hour_change = True):
    if zi_hour_change and birth_time.hour == 23:
        return birth_date + datetime.timedelta(days=1)
    return birth_date


# 五鼠遁：根據日干和時支計算時干
# 口訣： 甲己還加甲，乙庚丙作初，丙辛從戊起，丁壬庚子居，戊癸何方發，壬子是真途。
# 規則：
# 甲、己日 -> 甲子起
# 乙、庚日 -> 丙子起
# 丙、辛日 -> 戊子起
# 丁、壬日 -> 庚子起
# 戊、癸日 -> 壬子起
# 將十天干以 0-9 編號：
# 甲=0, 乙=1, 丙=2, ..., 癸=9
# 時支由子開始依次為：
# 子=0, 丑=1, 寅=2, ..., 亥=11
def hour_stem(day_stem, hour_branch):
    a = constant.ten_stems.index(day_stem)
    hour_offset = constant.twelve_branches.index(hour_branch)
    index = (2 * a + hour_offset) % 10
    return constant.ten_stems[index]

# 根據生日、出生時間和子時換日規則取得時柱
def get_hour_gz(birth_date, birth_time, zi_hour_change = True):
    effective_date = get_effective_date(birth_date, birth_time, zi_hour_change)
    day_stem = get_day_stem(effective_date)
    hour_branch = get_hour_branch(birth_time)
    return (hour_stem(day_stem, hour_branch), hour_branch)

# 時辰天干（時干）
def get_hour_stem(birth_date, birth_time, zi_hour_change = True):
    return get_hour_gz(birth_date, birth_time, zi_hour_change)[0]


def get_four_pillars(birth_date, birth_time, zi_hour_change = True):
    return {"year": get_year_gz(birth_date), 
            "month": get_month_gz(birth_date), 
            "day": get_day_gz(get_effective_date(birth_date, birth_time,zi_hour_change)),
            "hour": get_hour_gz(birth_date, birth_time, zi_hour_change)}

