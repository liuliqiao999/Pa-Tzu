import analysis_shensha_stem
import analysis_shensha_three_combine
import analysis_shensha_year
import analysis_shensha_month
import analysis_shensha_combined
import shensha_day

def remove_empty(results):
    return {name: value for name, value in results.items() if value}

def analyse_all_stem_shensha(four_pillars):
    results = {}
    results["祿神"] = analysis_shensha_stem.analyse_lok_san(four_pillars)
    results["羊刃"] = analysis_shensha_stem.analyse_yeung_jan(four_pillars)
    results["天乙貴人"] = analysis_shensha_stem.analyse_tin_yuet(four_pillars)
    results["文昌"] = analysis_shensha_stem.analyse_man_cheung(four_pillars)
    results["金輿"] = analysis_shensha_stem.analyse_gam_jyu(four_pillars)
    results["學堂"] = analysis_shensha_stem.analyse_hok_tong(four_pillars)
    results["詞館"] = analysis_shensha_stem.analyse_ci_gun(four_pillars)
    results["太極貴人"] = analysis_shensha_stem.analyse_taai_gik(four_pillars)
    results["國印貴人"] = analysis_shensha_stem.analyse_gwok_yan(four_pillars)
    results["福星貴人"] = analysis_shensha_stem.analyse_fuk_sing(four_pillars)
    results["天廚貴人"] = analysis_shensha_stem.analyse_tin_cyu(four_pillars)
    return remove_empty(results)


def analyse_all_three_combine_shensha(four_pillars):
    results = {}
    results["桃花"] = analysis_shensha_three_combine.analyse_tou_faa(four_pillars)
    results["驛馬"] = analysis_shensha_three_combine.analyse_yik_maa(four_pillars)
    results["華蓋"] = analysis_shensha_three_combine.analyse_waa_goi(four_pillars)
    results["將星"] = analysis_shensha_three_combine.analyse_zoeng_sing(four_pillars)
    results["劫煞"] = analysis_shensha_three_combine.analyse_gip_saat(four_pillars)
    results["亡神"] = analysis_shensha_three_combine.analyse_mong_san(four_pillars)
    results["災煞"] = analysis_shensha_three_combine.analyse_zoi_saat(four_pillars)
    return remove_empty(results)

def analyse_all_year_shensha(four_pillars):
    results = {}
    results["紅鸞"] = analysis_shensha_year.analyse_hung_luen(four_pillars)
    results["天喜"] = analysis_shensha_year.analyse_tin_hei(four_pillars)
    results["孤辰"] = analysis_shensha_year.analyse_gu_san(four_pillars)
    results["寡宿"] = analysis_shensha_year.analyse_gwa_suk(four_pillars)
    results["喪門"] = analysis_shensha_year.analyse_sang_mun(four_pillars)
    results["弔客"] = analysis_shensha_year.analyse_diu_haak(four_pillars)
    results["歲破"] = analysis_shensha_year.analyse_seoi_po(four_pillars)
    results["披麻"] = analysis_shensha_year.analyse_pei_maa(four_pillars)
    results["官符"] = analysis_shensha_year.analyse_gun_fu(four_pillars)
    results["白虎"] = analysis_shensha_year.analyse_baak_fu(four_pillars)
    return remove_empty(results)

def analyse_all_month_shensha(four_pillars):
    results = {}
    results["天德貴人"] = analysis_shensha_month.analyse_tin_dak(four_pillars)
    results["月德貴人"] = analysis_shensha_month.analyse_yuet_tak(four_pillars)
    results["天醫"] = analysis_shensha_month.analyse_tin_ji(four_pillars)
    results["德"] = analysis_shensha_month.analyse_dak(four_pillars)
    results["秀"] = analysis_shensha_month.analyse_sau(four_pillars)
    return remove_empty(results)

## 在shensha_day提到的空亡需要特殊處理
def analyse_hung_mong(four_pillars):
    day_stem = four_pillars["day"][0]
    day_branch = four_pillars["day"][1]
    hung_mong = shensha_day.Hung_Mong(day_stem, day_branch)
    results = []
    for pillar in ["year", "month", "day", "hour"]:
        branch = four_pillars[pillar][1]
        if branch in hung_mong:
            results.append(pillar)
    return results

def analyse_all_day_shensha(four_pillars):
    results = {}
    day_stem = four_pillars["day"][0]
    day_branch = four_pillars["day"][1]
    if shensha_day.Fui_Gong(day_stem, day_branch):
        results["魁罡"] = ["day"]
    if shensha_day.Yam_Caa_Yeung_Co(day_stem, day_branch):
        results["陰差陽錯"] = ["day"]
    if shensha_day.Sap_Ok_Daai_Baai(day_stem, day_branch):
        results["十惡大敗"] = ["day"]
    if shensha_day.Gu_Luen(day_stem, day_branch):
        results["孤鸞"] = ["day"]
    if shensha_day.Baat_Zyun(day_stem, day_branch):
        results["八專"] = ["day"]
    if shensha_day.Gau_Cau(day_stem, day_branch):
        results["九醜"] = ["day"]
    hung_mong = analyse_hung_mong(four_pillars)
    if hung_mong:
        results["空亡"] = hung_mong
    return results

def analyse_all_combined_shensha(four_pillars):
    results = {}
    if analysis_shensha_combined.analyse_tin_se(four_pillars):
        results["天赦"] = ["day"]
    if analysis_shensha_combined.analyse_sei_fai(four_pillars):
        results["四廢"] = ["day"]
    return results

def analyse_all_shensha(four_pillars):
    results = {}
    results.update(analyse_all_stem_shensha(four_pillars))
    results.update(analyse_all_three_combine_shensha(four_pillars))
    results.update(analyse_all_year_shensha(four_pillars))
    results.update(analyse_all_month_shensha(four_pillars))
    results.update(analyse_all_day_shensha(four_pillars))
    results.update(analyse_all_combined_shensha(four_pillars))
    return results

