import annual_rules
import analysis_luck
import analysis_annual
import analysis_interaction
import luck_rules
import calendar
import datetime


# 大運、流年及交互關係的綜合分析
def timing_basic_analysis(four_pillars, luck_pillar, solar_date):
    annual_pillar = annual_rules.annual_pillar(solar_date)
    return {
        "大運分析": analysis_luck.luck_basic_analysis(four_pillars, luck_pillar),
        "流年分析": analysis_annual.annual_basic_analysis(four_pillars, solar_date),
        "交互分析": analysis_interaction.interaction_basic_analysis(four_pillars, luck_pillar, annual_pillar)
    }

# 根據出生資料和目標日期，自動選擇大運並進行分析
def timing_auto_analysis(four_pillars, birth_datetime, gender, target_date):
    cycles = luck_rules.get_luck_cycles(four_pillars, birth_datetime, gender, 12)
    luck_pillar = luck_rules.get_luck_pillar_at_date(cycles, birth_datetime, target_date)
    if luck_pillar is None:
        return None
    return timing_basic_analysis(four_pillars, luck_pillar, target_date)

# 完整流年分析（以立春及交運日期分段）
def timing_yearly_analysis(four_pillars, birth_datetime, gender, year):
    start = calendar.get_lichun_datetime(year)
    end = calendar.get_lichun_datetime(year + 1)
    cycles = luck_rules.get_luck_cycles(four_pillars, birth_datetime, gender, 12)
    # 計算各步大運的開始日期
    first_start = luck_rules.luck_start_date(birth_datetime, cycles[0]["start_age"])
    change_dates = []
    for i in range(12):
        change_year = first_start.year + 10 * i
        try:
            change_date = first_start.replace(year=change_year)
        except ValueError:
            change_date = first_start.replace(year=change_year, day=28)
        if start < change_date < end:
            change_dates.append(change_date)
    boundaries = [start] + change_dates + [end] # 按交運日期切分流年
    results = []
    for i in range(len(boundaries) - 1):
        period_start = boundaries[i]
        period_end = boundaries[i + 1]
        luck_pillar = luck_rules.get_luck_pillar_at_date(cycles, birth_datetime, period_start)
        if luck_pillar is None:
            analysis = None
        else:
            analysis = timing_basic_analysis(four_pillars, luck_pillar, period_start)
        results.append({"開始": period_start, "結束": period_end, "大運": luck_pillar, "分析": analysis})
    return results

# 連續流年分析
def timing_years_analysis(
    four_pillars, birth_datetime, gender, start_year, end_year):
    if start_year > end_year:
        raise ValueError("開始年份不能大於結束年份")
    results = {}
    for year in range(start_year, end_year + 1):
        results[year] = timing_yearly_analysis(four_pillars, birth_datetime, gender, year)
    return results
