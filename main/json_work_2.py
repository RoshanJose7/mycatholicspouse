import json
import os
import time
import functools
from datetime import datetime
from django.conf import settings

import openpyxl

# w = openpyxl.load_workbook(settings.BASE_DIR / "17th Dec 2020 MB active cases.xlsx")
# w = w.active
# w = list(map(lambda x: str(int(x.value)), w["B"][:104]))

# print(w)

# json.dump(w, open("search.json", "w"), indent=4)

# reg_id_array = json.load(open("search.json", "r"))
# reg_id_array_list = reg_id_array
# reg_id_array = [{"REGT_ID": x, "STATUS": 0} for x in reg_id_array]


# input()


# def c():
#     time.sleep(1)
#     os.system('cls')


# print("Data Processing Starting...")

# c()
# print("User Data Loaded")
# user = json.load(open(os.path.join("D:\Django Projects\marryacatholic-data",
#                                    "httpcath_catholicm_table_user_table.json"), "r"))

# print("User Basic Infos Loaded")
# user_basic_info = json.load(open(os.path.join("D:\Django Projects\marryacatholic-data",
#                                               "httpcath_catholicm_table_basic_info_religion_table.json"), "rb"))

# print("User Locations Loaded")
# user_loc = json.load(open(os.path.join("D:\Django Projects\marryacatholic-data",
#                                        "httpcath_catholicm_table_contact_location_table.json"), "rb"))

# print("User Edu Data Loaded")
# user_ed = json.load(open(os.path.join("D:\Django Projects\marryacatholic-data",
#                                       "httpcath_catholicm_table_education_table.json"), "rb"))

# print("User Prefs Loaded")
# user_pref = json.load(open(os.path.join("D:\Django Projects\marryacatholic-data",
#                                         "httpcath_catholicm_table_partner_preference.json"), "rb"))

# print("User Regs Loaded")
# user_reg = json.load(open(os.path.join("D:\Django Projects\marryacatholic-data",
#                                        "httpcath_catholicm_table_registration.json"), "rb"))

# print("User Life Data Loaded")
# user_life = json.load(open(os.path.join("D:\Django Projects\marryacatholic-data",
#                                         "httpcath_catholicm_table_life_style_more_about_us_table.json"), "rb"))

# c()
# print("Sorting the data...")
# user_data = list(filter(lambda s: s["STATUS"] in ['0','1'], sorted(
#     user["data"], key=lambda x: int(x["REGT_ID"]))))
# print(len(user_data))
# print(user_data[0])
# input()
# c()
# print("..")
# info_data = sorted(user_basic_info["data"], key=lambda x: int(x["REGT_ID"]))
# c()
# print("....")
# loc_data = sorted(user_loc["data"], key=lambda x: int(x["REGT_ID"]))
# c()
# print("....")
# ed_data = sorted(user_ed["data"], key=lambda x: int(x["REGT_ID"]))
# c()
# print("......")
# pref_data = sorted(user_pref["data"], key=lambda x: int(x["REGT_ID"]))
# c()
# print("........")
# reg_data = sorted(user_reg["data"], key=lambda x: int(x["REGT_ID"]))

# def date_checker(x):
#     before_2018 = datetime.strptime("2018-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
#     try:
#         return datetime.strptime(x["REGT_DATE"], "%Y-%m-%d %H:%M:%S") > before_2018
#     except:
#         return False


# reg_data = list(filter(date_checker, reg_data))

# c()
# print("..........")
# life_data = sorted(user_life["data"], key=lambda x: int(x["REGT_ID"]))
# c()
# print("Sorting Finished")


# print("Data Sizes : ")
# print(list(map(len, [user_data,
#                      info_data,
#                      loc_data,
#                      ed_data,
#                      pref_data,
#                      reg_data,
#                      life_data])))

# input()
# c()

# def sync(table_1: list, table_2: list, sync_no: int) -> list:
#     temp = []
#     j = 0
#     i = 0
#     while i < len(table_1):
#         try:
#             if table_1[i]["REGT_ID"] == table_2[j]["REGT_ID"]:
#                 table_2[j][sync_no] = table_1[i]
#                 j += 1
#                 i += 1
#             else:
#                 if int(table_1[i]["REGT_ID"]) > int(table_2[j]["REGT_ID"]):
#                     j += 1
#                 elif int(table_1[i]["REGT_ID"]) < int(table_2[j]["REGT_ID"]):
#                     i += 1
#         except IndexError:
#             break
#     i = 0
#     while i < len(table_2):
#         try:
#             t = table_2[i][sync_no]
#         except:
#             table_2[i][sync_no] = {}
#         finally:
#             i += 1
#     return table_2

# def final_sync(table_1: list, table_2: list) -> list:
#     temp = []
#     j = 0
#     i = 0
#     z = 0
#     while i < len(table_1):
#         try:
#             if table_1[i]["reg_id"] == table_2[j]["REGT_ID"]:
#                 j += 1
#                 i += 1
#                 z += 1
#             else:
#                 if int(table_1[i]["reg_id"]) > int(table_2[j]["REGT_ID"]):
#                     j += 1
#                 elif int(table_1[i]["reg_id"]) < int(table_2[j]["REGT_ID"]):
#                     i += 1
#         except IndexError:
#             break
#     c()
#     print(f"No. of 's Users : {z}")
#     return temp

# def check_sync(table_1: list, table_2: list, status_no: int) -> list:
#     temp = []
#     j = 0
#     i = 0
#     z = 0
#     while i < len(table_1):
#         try:
#             if table_1[i]["REGT_ID"] == table_2[j]["REGT_ID"]:
#                 table_1[i]["STATUS"] = status_no
#                 j += 1
#                 i += 1
#             else:
#                 if int(table_1[i]["REGT_ID"]) > int(table_2[j]["REGT_ID"]):
#                     j += 1
#                 elif int(table_1[i]["REGT_ID"]) < int(table_2[j]["REGT_ID"]):
#                     i += 1
#         except IndexError:
#             break
#     return table_1

# c()
# print("Syncing Data")

# big_data = sync(reg_data, sync(user_data, sync(ed_data, sync(
#     info_data, sync(pref_data, sync(life_data, loc_data, 0), 1), 2), 3), 4), 5)
# c()

# exception_list = []
# ultra_refined_data = []

# print(f'Size of big_data : {len(big_data)}')
# input("pass")

# i = 0
# while i < len(big_data):
#     try:
#         t = big_data[i][5]["REGT_ID"]
#         ultra_refined_data.append(big_data[i])
#     except:
#         if big_data[i]["REGT_ID"] in reg_id_array_list:
#             ultra_refined_data.append(big_data[i])
#         else:
#             exception_list.append(big_data[i])
#     finally:
#         i += 1

# print("First One Done")

# big_data = []
# i = 0
# while i < len(ultra_refined_data):
#     try:
#         t = ultra_refined_data[i][4]["REGT_ID"]
#         big_data.append(ultra_refined_data[i])
#     except:
#         if ultra_refined_data[i]["REGT_ID"] in reg_id_array_list:
#             big_data.append(ultra_refined_data[i])
#         else:
#             exception_list.append(ultra_refined_data[i])
#     finally:
#         i += 1

# print(f"Final Data List Size : {len(big_data)}")

# print("Saving to disk...")
# json.dump(big_data, open("test.json", "w"), indent=4)
# json.dump(exception_list, open("exception.json", "w"), indent=4)
# print("Operation Finished")
# print("Exiting...")
# c()

# xcel_data = list(json.load(open("final.json", "r")).values())

# reg_id_array = check_sync(reg_id_array, big_data, 1)
# reg_id_array = check_sync(reg_id_array, exception_list, -1)

# json.dump(reg_id_array, open("new_search.json", "w"), indent=4)

#!safas

d = json.load(open("test.json", "rb"))


# def test_field(field_section, field_name):
#     print(set(map(lambda x: x[field_section][field_name], d)))
#     print(functools.reduce(
#         max, list(map(lambda x: len(x[field_section][field_name]), d)), 0))


def work_section():
    print(d[0])

    i = 0

    all_details = {}

    while (i < len(d)):
        t = {}
        t['reg_id'] = d[i]['REGT_ID']
        try:
            t["email"] = d[i]['4']['USER_NAME']
        except:
            pass
        try:
            if d[i]['5']['REGT_STATUS'] in ["Other", "Unmarried"]:
                t["marital_status"] = "Single"
            elif d[i]['5']['REGT_STATUS'] in ["Separated", "Divorced/Annulled", "Divorced", "Annulled"]:
                t["marital_status"] = "Divorced"
            else:
                t["marital_status"] = "Widowed"
            name = d[i]['5']['REGT_NAME'].split('-')
            t["mother_tongue"] = d[i]['5']['REGT_MT']
            t['gender'] = "Male" if d[i]['5']['REGT_GENDER'] == "M" else "Female"
            t["date_of_birth"] = d[i]['5']["REGT_DOB"]
            t["occupation"] = d[i]['5']["REGT_OCCUP"] if d[i]['5']["REGT_OCCUP"] is not None else " "
            ph_no = d[i]['5']['REGT_CONTACT'].split("-")
            t["age"] = int(d[i]['5']['REGT_AGE'])
            edu = d[i]['5']['REGT_EDUCATION']
            t['first_name'] = name[0]
            t['last_name'] = " ".join(name[1:])
            if edu in ["Graduate", "Post Graduate"]:
                t["education_level"] = edu
            elif edu is not None:
                t["education_level"] = "Other"
                t["other_type"] = edu
            else:
                t["education_level"] = "Less Than 10th"
        except:
            pass
        # t["phone_number"] = f"+{ph_no[0]}{ph_no[1]}" if len(
        # ph_no) > 1 else f"+91{ph_no[0]}"
        t["country"] = d[i]['country_id']
        t["state"] = d[i]['state_id']
        t["city"] = d[i]['city_id']

        # TODO Education marks and school
        t["tenth_school"] = d[i]["3"]["edu_ten_name"] if d[i]["3"]["edu_ten_name"] is not None else " "
        t["hs_school"] = d[i]["3"]["edu_pre_univ_name"] if d[i]["3"]["edu_pre_univ_name"] is not None else " "
        t["grad_school"] = d[i]["3"]["edu_pre_grad_name"] if d[i]["3"]["edu_pre_grad_name"] is not None else " "
        t["post_grad_school"] = d[i]["3"]["edu_pre_post_grad_name"] if d[i]["3"]["edu_pre_post_grad_name"] is not None else " "
        t["other_school"] = d[i]["3"]["edu_pre_oth_name"] if d[i]["3"]["edu_pre_oth_name"] is not None else " "

        t["weight"] = float(d[i]['2']['pf_weight']
                            ) if d[i]['2']['pf_weight'] is not None else 0
        t["smoke"] = d[i]['0']['pf_smoke'] if d[i]['0']['pf_smoke'] is not None else "No"
        t["drink"] = d[i]['0']['pf_smoke'] if d[i]['0']['pf_smoke'] is not None else "No"
        t["diet"] = "Vegetarian" if d[i]['0']['pf_diet'] in [
            "Veg", None] else "Non-Vegetarian"
        t["parish_baptized_at"] = d[i]['2']['pf_baptism']
        t["present_parish"] = d[i]['2']['pf_parish'] if d[i]['2']['pf_parish'] is not None else " "
        t["diocese"] = d[i]['2']['pf_diocese'] if d[i]['2']['pf_diocese'] is not None else " "

        t["fathers_name"] = d[i]['0']['pf_father_name'] if d[i]['0']['pf_father_name'] is not None else " "
        t["mothers_name"] = d[i]['0']['pf_mother_name'] if d[i]['0']['pf_mother_name'] is not None else " "
        t["brothers"] = 0
        t["sisters"] = 0
        t["siblings"] = int(d[i]['2']["noof_siblings"]
                            ) if d[i]['2']["noof_siblings"] is not None else 0
        t["about_yourself"] = d[i]['0']["pf_personal_details"]
        t["values"] = d[i]['0']["pf_background_family"] if d[i]['0']["pf_background_family"] in [
            "Liberal", "Moderate", "Traditional"] else "Traditional"
        t["family_members"] = 3 + t["brothers"] + t["sisters"]

        t["rite"] = d[i]['2']["caste_id"] if d[i]['2']["caste_id"] in [
            "Latin", "Syro Malankara", "Syro Malabar"] else "Latin"
        # "REGT_DOB": "1984-06-04"
        # t["annual_income"] = d[i]["pf_income"]
        all_details[i] = t
        i += 1

#     print(all_details[3])

    json.dump(all_details, open("new_reg_data.json", "w"), indent=4)


work_section()
