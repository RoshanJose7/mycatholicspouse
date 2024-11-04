import json
import os
import time
import openpyxl
from datetime import datetime


def c():
    time.sleep(1)
    os.system('cls')


data = openpyxl.load_workbook("17th Dec 2020 MB Active cases.xlsx")

s = data.active

our_data = []

for i in range(1, 110):
    temp = {}
    temp["reg_id"] = int(s[f"B{i}"].value)
    name = s[f"C{i}"].value.split(
        "-")[1].split(" ") if "-" in s[f"C{i}"].value else s[f"C{i}"].value.split(" ")
    temp['first_name'] = " ".join(name[0:len(name)-1])
    temp['last_name'] = name[-1]
    temp['email'] = s[f"D{i}"].value
    phone_number = str(s[f"E{i}"].value)
    print(phone_number)
    if phone_number[0] == '+':
        if len(phone_number) == 13:
            temp['phone_number'] = phone_number
    else:
        if len(phone_number) == 10:
            temp['phone_number'] = f'+91{phone_number}'
    if s[f"F{i}"].value is not None:
        temp['gender'] = s[f"F{i}"].value
    date = s[f"G{i}"].value
    if type(date) != str:
        temp['date_of_birth'] = str(date)
    else:
        date = list(map(int, date.split("-")))
        temp['date_of_birth'] = str(datetime(*date))
    temp['mother_tongue'] = s[f"H{i}"].value
    date = s[f"I{i}"].value
    temp['subs_end'] = str(date)
    our_data.append(temp)

json.dump(our_data, open('finalized__data.json', 'w'), indent=4)
print(s)


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
# # print("..")
# # info_data = sorted(user_basic_info["data"], key=lambda x: int(x["REGT_ID"]))
# # c()
# # print("....")
# loc_data = sorted(user_loc["data"], key=lambda x: int(x["REGT_ID"]))
# c()
# # print("....")
# # ed_data = sorted(user_ed["data"], key=lambda x: int(x["REGT_ID"]))
# # c()
# # print("......")
# # pref_data = sorted(user_pref["data"], key=lambda x: int(x["REGT_ID"]))
# # c()
# print("........")
# reg_data = sorted(user_reg["data"], key=lambda x: int(x["REGT_ID"]))
# c()
# # print("..........")
# # life_data = sorted(user_life["data"], key=lambda x: int(x["REGT_ID"]))
# # c()
# print("Sorting Finished")

# #  user_data, ed_data, info_data, pref_data, life_data, reg_data, loc_data

# # print("Data Sizes : ")
# # print(list(map(len, [user_data,
# #                      info_data,
# #                      loc_data,
# #                      ed_data,
# #                      pref_data,
# #                      reg_data,
# #                      life_data])))

# # d = json.load(open("test.json", "rb"))

# # q = []

# # for i in range(len(d)):
# #     if d[i]["3"]["STATUS"] == "1":
# #         q.append(d[i])

# # print(len(q))

# # z = {}

# # def set_z():
# #     #email name dob phone number mother tongue address
# #     i = 0
# #     while i < len(q):
# #         t = {}
# #         t["regt_id"] = q[i]['4']['REGT_ID']
# #         t["name"] = q[i]['4']['REGT_NAME']
# #         t["email"] = q[i]['3']['USER_NAME']
# #         ph_no = q[i]['4']['REGT_CONTACT'].split("-")
# #         t["phone_number"] = f"+{ph_no[0]}{ph_no[1]}" if len(ph_no) > 1 else f"+91{ph_no[0]}"
# #         t['gender'] = "Male" if q[i]['4']['REGT_GENDER'] == "M" else "Female"
# #         t["dob"] = q[i]["4"]['REGT_DOB']
# #         t["mother_tongue"] = q[i]['4']['REGT_MT']
# #         z[f"{i}"] = t
# #         i += 1

# # set_z()

# # json.dump(z, open("dump.json", 'w'), indent = 4)


# def sync(table_1: list, table_2: list, sync_no: int) -> list:
#     temp = []
#     j = 0
#     i = 0
#     while i < len(table_1):
#         # if i % 500 == 0:
#         #     print(table_1[i]["REGT_ID"], table_2[j]["REGT_ID"])
#         #     input()
#         try:
#             if table_1[i]["REGT_ID"] == table_2[j]["REGT_ID"]:
#                 t = table_2[j]
#                 t[sync_no] = table_1[i]
#                 temp.append(t)
#                 j += 1
#                 i += 1
#             else:
#                 if int(table_1[i]["REGT_ID"]) > int(table_2[j]["REGT_ID"]):
#                     j += 1
#                 elif int(table_1[i]["REGT_ID"]) < int(table_2[j]["REGT_ID"]):
#                     i += 1
#         except IndexError:
#             break
#     time.sleep(2)
#     c()
#     print(f"Sync Pass Number : {sync_no} | Size of Data List : {len(temp)}")
#     return temp

# def final_sync(table_1: list, table_2: list) -> list:
#     temp = []
#     j = 0
#     i = 0
#     while i < len(table_1):
#         # if i % 500 == 0:
#         #     print(table_1[i]["REGT_ID"], table_2[j]["REGT_ID"])
#         #     input()
#         try:
#             if table_1[i]["reg_id"] == table_2[j]["REGT_ID"]:
#                 table_1[i]["our_status"] = 'Inactive'
#                 temp.append(table_1[i])
#                 j += 1
#                 i += 1
#             else:
#                 if int(table_1[i]["reg_id"]) > int(table_2[j]["REGT_ID"]):
#                     j += 1
#                 elif int(table_1[i]["reg_id"]) < int(table_2[j]["REGT_ID"]):
#                     i += 1
#         except IndexError:
#             break
#     time.sleep(2)
#     c()
#     print(f"Size of Data List : {len(temp)}")
#     return temp

# def finally_final_sync(table_1: list, table_2: list) -> list:
#     temp = []
#     j = 0
#     i = 0
#     z = 0
#     while i < len(table_1):
#         # if i % 500 == 0:
#         #     print(table_1[i]["REGT_ID"], table_2[j]["REGT_ID"])
#         #     input()
#         try:
#             if table_1[i]["reg_id"] == table_2[j]["reg_id"]:
#                 table_1[i]["our_status"] = 'Active'
#                 j += 1
#                 i += 1
#                 z += 1
#             else:
#                 if int(table_1[i]["reg_id"]) > int(table_2[j]["reg_id"]):
#                     j += 1
#                 elif int(table_1[i]["reg_id"]) < int(table_2[j]["reg_id"]):
#                     i += 1
#         except IndexError:
#             break
#     time.sleep(2)
#     c()
#     print(f"Size of Data List : {len(temp)}")
#     print(f"No. of Nevil's users found : {z}")
#     return table_1

# new_data = sync(reg_data, user_data, 0)

# before_2018 = datetime.strptime("2018-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

# final_data = list(filter(lambda x: datetime.strptime(x[0]["REGT_DATE"], "%Y-%m-%d %H:%M:%S") < before_2018, new_data))

# temp_data = json.load(open("reg_data.json", "rb"))

# temp_list = list(temp_data.values())

# finally_final_data = final_sync(temp_list, final_data)

# xcel_data = list(json.load(open("final.json", "r")).values())

# finally_final_data = finally_final_sync(finally_final_data, xcel_data)

# print(f"No. of Inactive Users : {len([x for x in finally_final_data if x['our_status'] == 'Inactive'])}")
# print(f"No. of Active Users : {len([x for x in finally_final_data if x['our_status']=='Active'])}")
# print([x["reg_id"] for x in finally_final_data if x['our_status']=='Active'])
# # c()
# # print("Syncing Data")
# # big_data = sync(loc_data, sync(reg_data, sync(life_data, sync(
# #     pref_data, sync(info_data, sync(ed_data, user_data, 0), 1), 2), 3), 4), 5)
# # c()
# # print(f"Final Data List Size : {len(big_data)}")

# # print("Saving to disk...")
# # json.dump(big_data, open("test.json", "w"), indent=4)
# # # print(len(temp))
# # print("Operation Finished")
# # print("Exiting...")
# # c()

# #!safas

# # d = json.load(open("test.json", "rb"))


# # def test_field(field_section, field_name):
# #     print(set(map(lambda x: x[field_section][field_name], d)))
# #     print(functools.reduce(
# #         max, list(map(lambda x: len(x[field_section][field_name]), d)), 0))


# # def work_section():
# #     print(d[0])

# #     i = 0

# #     all_details = {}

# #     while (i < len(d)):
# #         t = {}
# #         t['reg_id'] = d[i]['REGT_ID']
# #         t['interim_password'] = d[i]['3']['USER_PASSWORD']
# #         name = d[i]['4']['REGT_NAME'].split('-')
# #         t['first_name'] = name[0]
# #         t['last_name'] = " ".join(name[1:])
# #         t["mother_tongue"] = d[i]['4']['REGT_MT']
# #         t['gender'] = "Male" if d[i]['4']['REGT_GENDER'] == "M" else "Female"
# #         ph_no = d[i]['4']['REGT_CONTACT'].split("-")
# #         # t["phone_number"] = f"+{ph_no[0]}{ph_no[1]}" if len(
# #         # ph_no) > 1 else f"+91{ph_no[0]}"
# #         t["email"] = d[i]['3']['USER_NAME']
# #         t["country"] = d[i]['5']['country_id']
# #         t["state"] = d[i]['5']['state_id']
# #         t["city"] = d[i]['5']['city_id']
# #         t["age"] = int(d[i]['4']['REGT_AGE'])
# #         edu = d[i]['4']['REGT_EDUCATION']
# #         if edu in ["Graduate", "Post Graduate"]:
# #             t["education_level"] = edu
# #         elif edu is not None:
# #             t["education_level"] = "Other"
# #             t["other_type"] = edu
# #         else:
# #             t["education_level"] = "Less Than 10th"

# #         # TODO Education marks and school
# #         t["tenth_school"] = d[i]["edu_ten_name"] if d[i]["edu_ten_name"] is not None else " "
# #         t["hs_school"] = d[i]["edu_pre_univ_name"] if d[i]["edu_pre_univ_name"] is not None else " "
# #         t["grad_school"] = d[i]["edu_pre_grad_name"] if d[i]["edu_pre_grad_name"] is not None else " "
# #         t["post_grad_school"] = d[i]["edu_pre_post_grad_name"] if d[i]["edu_pre_post_grad_name"] is not None else " "
# #         t["other_school"] = d[i]["edu_pre_oth_name"] if d[i]["edu_pre_oth_name"] is not None else " "

# #         t["weight"] = float(d[i]['0']['pf_weight']
# #                             ) if d[i]['0']['pf_weight'] is not None else 0
# #         t["smoke"] = d[i]['2']['pf_smoke'] if d[i]['2']['pf_smoke'] is not None else "No"
# #         t["drink"] = d[i]['2']['pf_smoke'] if d[i]['2']['pf_smoke'] is not None else "No"
# #         t["diet"] = "Vegetarian" if d[i]['2']['pf_diet'] in [
# #             "Veg", None] else "Non-Vegetarian"
# #         if d[i]['4']['REGT_STATUS'] in ["Other", "Unmarried"]:
# #             t["marital_status"] = "Single"
# #         elif d[i]['4']['REGT_STATUS'] in ["Separated", "Divorced/Annulled", "Divorced", "Annulled"]:
# #             t["marital_status"] = "Divorced"
# #         else:
# #             t["marital_status"] = "Widowed"
# #         t["parish_baptized_at"] = d[i]['0']['pf_baptism']
# #         t["present_parish"] = d[i]['0']['pf_parish'] if d[i]['0']['pf_parish'] is not None else " "
# #         t["diocese"] = d[i]['0']['pf_diocese'] if d[i]['0']['pf_diocese'] is not None else " "

# #         t["fathers_name"] = d[i]['2']['pf_father_name'] if d[i]['2']['pf_father_name'] is not None else " "
# #         t["mothers_name"] = d[i]['2']['pf_mother_name'] if d[i]['2']['pf_mother_name'] is not None else " "
# #         t["brothers"] = 0
# #         t["sisters"] = 0
# #         t["siblings"] = int(d[i]['0']["noof_siblings"]
# #                             ) if d[i]['0']["noof_siblings"] is not None else 0
# #         t["about_yourself"] = d[i]['2']["pf_personal_details"]
# #         t["values"] = d[i]['2']["pf_background_family"] if d[i]['2']["pf_background_family"] in [
# #             "Liberal", "Moderate", "Traditional"] else "Traditional"
# #         t["family_members"] = 3 + t["brothers"] + t["sisters"]

# #         t["rite"] = d[i]['0']["caste_id"] if d[i]['0']["caste_id"] in [
# #             "Latin", "Syro Malankara", "Syro Malabar"] else "Latin"
# #         # "REGT_DOB": "1984-06-04"
# #         t["date_of_birth"] = d[i]['4']["REGT_DOB"]
# #         t["occupation"] = d[i]['4']["REGT_OCCUP"] if d[i]['4']["REGT_OCCUP"] is not None else " "
# #         # t["annual_income"] = d[i]["pf_income"]
# #         all_details[i] = t
# #         i += 1

# #     print(all_details[3])

# #     json.dump(all_details, open("reg_data.json", "w"), indent=4)
