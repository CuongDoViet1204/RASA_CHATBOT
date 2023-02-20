# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sqlite3
import datetime

import numpy as np
import string
from googletrans import Translator

from ProcessDB.getDB import GetDB
from ProcessDB.insertDB import InsertDB
from ProcessDB.deleteRow import DeleteDB

from Algorithm.Random_Forest import Random_Forest

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.events import Restarted
from rasa_sdk.events import FollowupAction


sql_path = 'E:\BaiTapTriTueNhanTao\demo_chatbot_rasa_2\ProcessDB\database.db'
filename = 'E:\BaiTapTriTueNhanTao\demo_chatbot_rasa_2\DatasetOriginal'
random_fr = Random_Forest(filename)
random_fr.PreProcessingCSV()
random_fr.Fit()
symptom = np.zeros((1, random_fr.numberOfHeader), dtype = int)

list_prognosis = ['Hepatitis C', 'Dengue', 'Arthritis', 'Fungal infection', 'Psoriasis', 'hepatitis A', '(vertigo) Paroymsal  Positional Vertigo', 'Gastroenteritis', 'Hepatitis D', 'Osteoarthristis', 'Acne', 'GERD', 'Hyperthyroidism', 'Chicken pox', 'Common Cold', 'Alcoholic hepatitis', 'Pneumonia', 'Hepatitis B', 'Dimorphic hemmorhoids(piles)', 'Allergy', 'Hypoglycemia', 'Drug Reaction', 'Jaundice', 'Typhoid', 'Peptic ulcer diseae', 'Diabetes ', 'Paralysis (brain hemorrhage)', 'Cervical spondylosis', 'AIDS', 'Hypothyroidism', 'Impetigo', 'Urinary tract infection', 'Hepatitis E', 'Varicose veins', 'Chronic cholestasis', 'Bronchial Asthma', 'Heart attack', 'Migraine', 'Malaria', 'Tuberculosis', 'Hypertension ']
list_url = [
            ['https://vi.wikipedia.org/wiki/Vi%C3%AAm_gan_C'],
            ['https://vi.wikipedia.org/wiki/S%E1%BB%91t_xu%E1%BA%A5t_huy%E1%BA%BFt'],
            ['https://vi.wikipedia.org/wiki/Vi%C3%AAm_kh%E1%BB%9Bp'],
            ['https://en.wikipedia.org/wiki/Fungal_infection'],
            ['https://vi.wikipedia.org/wiki/B%E1%BB%87nh_v%E1%BA%A9y_n%E1%BA%BFn'],
            ['https://vi.wikipedia.org/wiki/Vi%C3%AAm_gan_A'],
            ['https://vi.wikipedia.org/wiki/Ch%C3%B3ng_m%E1%BA%B7t_l%C3%A0nh_t%C3%ADnh_do_t%C6%B0_th%E1%BA%BF'],
            ['https://en.wikipedia.org/wiki/Gastroenteritis'],
            ['https://en.wikipedia.org/wiki/Hepatitis_D'],
            ['https://vi.wikipedia.org/wiki/Tho%C3%A1i_h%C3%B3a_kh%E1%BB%9Bp'],
            ['https://vi.wikipedia.org/wiki/M%E1%BB%A5n'],
            ['https://vi.wikipedia.org/wiki/Tr%C3%A0o_ng%C6%B0%E1%BB%A3c_d%E1%BA%A1_d%C3%A0y_th%E1%BB%B1c_qu%E1%BA%A3n'],
            ['https://vi.wikipedia.org/wiki/C%C6%B0%E1%BB%9Dng_gi%C3%A1p'],
            ['https://vi.wikipedia.org/wiki/Th%E1%BB%A7y_%C4%91%E1%BA%ADu'],
            ['https://vi.wikipedia.org/wiki/C%E1%BA%A3m_l%E1%BA%A1nh'],
            ['https://vi.wikipedia.org/wiki/Vi%C3%AAm_gan_do_r%C6%B0%E1%BB%A3u'],
            ['https://vi.wikipedia.org/wiki/Vi%C3%AAm_ph%E1%BB%95i'],
            ['https://vi.wikipedia.org/wiki/Vi%C3%AAm_gan_B'],
            ['https://vi.wikipedia.org/wiki/Tr%C4%A9_(b%E1%BB%87nh)'],
            ['https://vi.wikipedia.org/wiki/D%E1%BB%8B_%E1%BB%A9ng'],
            ['https://vi.wikipedia.org/wiki/H%E1%BA%A1_%C4%91%C6%B0%E1%BB%9Dng_huy%E1%BA%BFt'],
            ['https://en.wikipedia.org/wiki/Adverse_drug_reaction'],
            ['https://vi.wikipedia.org/wiki/V%C3%A0ng_da'],
            ['https://vi.wikipedia.org/wiki/Th%C6%B0%C6%A1ng_h%C3%A0n'],
            ['https://vi.wikipedia.org/wiki/Vi%C3%AAm_lo%C3%A9t_d%E1%BA%A1_d%C3%A0y_t%C3%A1_tr%C3%A0ng'],
            ['https://vi.wikipedia.org/wiki/%C4%90%C3%A1i_th%C3%A1o_%C4%91%C6%B0%E1%BB%9Dng'],
            ['https://www.medicalnewstoday.com/articles/317080'],
            ['https://vi.wikipedia.org/wiki/Tho%C3%A1i_h%C3%B3a_%C4%91%E1%BB%91t_s%E1%BB%91ng_c%E1%BB%95'],
            ['https://vi.wikipedia.org/wiki/HIV/AIDS'],
            ['https://vi.wikipedia.org/wiki/Suy_gi%C3%A1p'],
            ['https://vi.wikipedia.org/wiki/Ch%E1%BB%91c'],
            ['https://vi.wikipedia.org/wiki/Nhi%E1%BB%85m_tr%C3%B9ng_%C4%91%C6%B0%E1%BB%9Dng_ti%E1%BA%BFt_ni%E1%BB%87u'],
            ['https://en.wikipedia.org/wiki/Hepatitis_E'],
            ['https://en.wikipedia.org/wiki/Varicose_veins'],
            ['https://my.clevelandclinic.org/health/diseases/24554-cholestasis'],
            ['https://vi.wikipedia.org/wiki/Hen_ph%E1%BA%BF_qu%E1%BA%A3n'],
            ['https://vi.wikipedia.org/wiki/Nh%E1%BB%93i_m%C3%A1u_c%C6%A1_tim'],
            ['https://vi.wikipedia.org/wiki/%C4%90au_n%E1%BB%ADa_%C4%91%E1%BA%A7u'],
            ['https://vi.wikipedia.org/wiki/S%E1%BB%91t_r%C3%A9t'],
            ['https://vi.wikipedia.org/wiki/Lao'],
            ['https://vi.wikipedia.org/wiki/T%C4%83ng_huy%E1%BA%BFt_%C3%A1p'],
            ]
# symptom[:, 0] = range(1)
# symptom[0, :] = range(random_fr.numberOfHeader)
# print(symptom)
isSlotSet = False

def name_cap(text):
    tarr = text.split()
    for idx in range(len(tarr)):
        tarr[idx] = tarr[idx].capitalize()
    return ' '.join(tarr)

def take_name(text):
    tarr = text.split()
    for idx in range(len(tarr)):
        tarr[idx] = tarr[idx].capitalize()
    if len(tarr) >= 2:
        if tarr[len(tarr) - 1] == "Anh":
            return ' '.join([tarr[len(tarr) - 2], tarr[len(tarr) - 1]])
    return tarr[len(tarr) - 1]

class action_save_cust_info_when_give_name(Action): # cập nhật lại slot khi người dùng đưa tên
    def name(self) -> Text:
        return "action_save_cust_info_when_give_name"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        id = (tracker.current_state())["sender_id"]
        print(id)
        cust_name = next(tracker.get_latest_entity_values("cust_name"), None)
        cust_sex = next(tracker.get_latest_entity_values("cust_sex"), None)
        bot_position = "mình"    
        if (cust_sex is None):
            cust_sex = "bạn"
        if (cust_sex == "anh") | (cust_sex == "chị") | (cust_sex == "Anh") | (cust_sex == "Chị"):
            bot_position = "em"
        elif (cust_sex == "cô") | (cust_sex == "chú") | (cust_sex == "ông") | (cust_sex == "bác") | (cust_sex == "Bà") | (cust_sex == "Cô") | (cust_sex == "Chú") | (cust_sex == "Ông") | (cust_sex == "Bác") | (cust_sex == "Bà"):
            bot_position = "cháu"
        else:
            cust_sex = "bạn"
            bot_position = "Mình"
        user = GetDB(sql_path).get_user(id)
        if (cust_name is None):
            cust_name = ""
        else:
            cust_name = take_name(cust_name)
        if user is None:
            InsertDB(sql_path).InsertUser(id, cust_name, cust_sex, bot_position)     
            print('insert')
        else:            
            DeleteDB(sql_path).DeleteUser(id)
            InsertDB(sql_path).InsertUser(id, cust_name, cust_sex, bot_position)   
            print('update')
        isSlotSet = True
        return [SlotSet('cust_name', name_cap(cust_name)),SlotSet('cust_sex', name_cap(cust_sex)),SlotSet('bot_position', name_cap(bot_position))]

class action_save_cust_info_when_greet(Action): # cập nhật lại slot khi người dùng chào
    def name(self) ->Text:
        return "action_save_cust_info_when_greet"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        if isSlotSet == True:
            return []
        id = (tracker.current_state())["sender_id"]
        print(id)        
        user = GetDB(sql_path).get_user(id)
        if user:
            cust_name = user[1]
            cust_sex = user[2]
            bot_position = user[3]
        else:
            cust_name = ""
            cust_sex = "bạn"
            bot_position = "mình"
        return [SlotSet('cust_name', name_cap(cust_name)),SlotSet('cust_sex', name_cap(cust_sex)),SlotSet('bot_position', name_cap(bot_position))]

class action_greet_user(Action): # chào người dùng
    def name(self) ->Text:
        return "action_greet_user"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id = (tracker.current_state())["sender_id"]
        print(id)        
        user = GetDB(sql_path).get_user(id)
        if user is None:
            dispatcher.utter_message(text = "Chào bạn ^^, chúc bạn một ngày tốt lành! Mình là Rasa, Trợ lí ảo tư vấn chuẩn đoán bệnh.\nBạn có thể cho mình biết tên để tiện xưng hô không?")
        else:
            dispatcher.utter_message(response = "utter_give_name")
            diagnostics = GetDB(sql_path).get_diagnostic(id)
            if diagnostics is None:
                return [FollowupAction("action_give_button_start")]
            else:
                cust_sex = user[2]
                ret_text = cust_sex + " cần: "
                button1 = {
                        "type": "postback",
                        "title": "Lịch sử chẩn đoán",
                        "payload": "Lịch sử chẩn đoán"
                }
                button2 = {
                        "type": "postback",
                        "title": "Bắt đầu tư vấn",
                        "payload": "Bắt đầu tư vấn chẩn đoán bệnh"
                    }    
                dispatcher.utter_message(text = ret_text, buttons = [button1, button2])
        
class action_give_button_start(Action):
    def name(self) ->Text:
        return "action_give_button_start"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        ret_text = "Bạn có muốn bắt đầu tư vấn chẩn đoán bệnh?"
        button = {
                "type": "postback",
                "title": "Bắt đầu tư vấn",
                "payload": "Bắt đầu tư vấn chẩn đoán bệnh"
            }
        dispatcher.utter_message(text = ret_text, buttons = [button])

class action_give_button_request(Action):
    def name(self) ->Text:
        return "action_give_button_request"
    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        check = False
        for i in range (len(symptom[0])):
            if symptom[0, i] == 1:
                check = True
                break
        id = (tracker.current_state())["sender_id"] 
        print(id)        
        user = GetDB(sql_path).get_user(id)
        if user:
            cust_sex = user[2]
        else:
            cust_sex = "bạn"
        dispatcher.utter_message(text = "Triệu chứng của " + cust_sex + " là gì?")
        if check == True:
            ret_text = "Bạn có muốn nhận lời chẩn đoán?"
            button = {
                    "type": "postback",
                    "title": "Nhận lời chẩn đoán",
                    "payload": "Nhận lời chẩn đoán"
                }
            dispatcher.utter_message(text = ret_text, buttons = [button])
            
class action_take_symptom(Action):
    def name(self) ->Text:
        return "action_take_symptom"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id = (tracker.current_state())["sender_id"]
        cust_symptom = tracker.get_slot("cust_symptom")
        print(cust_symptom)
        list_symptom = ['ngứa', 'phát ban da', 'phát ban nốt da', 'hắt hơi liên tục', 'rùng mình', 'ớn lạnh', 'đau khớp', 'đau dạ dày', 'thiếu axit', 'loét lưỡi', 'lãng phí cơ bắp', 'nôn mửa', 'nóng rát', 'tiểu ra máu', 'mệt mỏi', 'tăng cân', 'lo lắng', 'tay chân lạnh', 'tâm trạng lâng lâng', 'sụt cân', 'bồn chồn', 'thờ ơ', 'mảng ở cổ', 'lượng đường không đủ', 'ho', 'sốt cao', 'mắt trũng sâu', 'khó thở', 'đổ mồ hôi', 'mất nước', 'khó tiêu', 'đau đầu', 'da hơi vàng', 'nước tiểu đậm', 'buồn nôn', 'ăn mất ngon', 'đau sau mắt', 'đau lưng', 'táo bón', 'đau bụng', 'tiêu chảy', 'sốt nhẹ', 'nước tiểu vàng', 'mắt vàng', 'suy gan cấp tính', 'quá tải chất lỏng', 'sưng bụng', 'sưng hạch bạch huyết', 'phiền muộn', 'thị lực mờ, méo mó', 'đờm', 'viêm họng', 'mắt đỏ', 'xoang', 'sổ mũi', 'sung huyết', 'đau ngực', 'chân tay yếu', 'nhịp tim nhanh', 'đau khi đi nặng', 'đau hậu môn', 'phân có máu', 'ngứa hậu môn', 'đau cổ', 'chóng mặt', 'chuột rút', 'bầm tím', 'béo phì', 'sưng chân', 'sưng mạch máu', 'mắt và mặt sưng húp', 'phì đại tuyến giáp', 'móng tay dễ gãy', 'sưng tứ chi', 'đói quá mức', 'bệnh tình dục', 'môi khô và ngứa', 'nói lắp', 'đau đầu gối', 'đau khớp háng', 'yếu cơ', 'cứng cơ', 'sưng khớp', 'cử động cứng', 'chuyển động quay', 'mất thăng bằng', 'không vững vàng', 'yếu một bên cơ thể', 'mất mùi', 'bàng quang khó chịu', 'nước tiểu có mùi hôi', 'liên tục buồn tiểu', 'đầy hơi', 'ngứa bên trong', 'bệnh thương hàn', 'trầm cảm', 'dễ cáu gắt', 'đau cơ', 'thay đổi cảm giác', 'mụn đỏ trên cơ thể', 'đau bụng', 'kinh nguyệt bất thường', 'vùng đổi màu', 'chảy nước mắt', 'tăng khẩu vị', 'đa niệu', 'bệnh di truyền', 'đờm nhầy', 'đờm gỉ', 'thiếu tập trung', 'rối loạn thị giác', 'nhận truyền máu', 'tiêm không vô trùng', 'hôn mê', 'chảy máu dạ dày', 'chướng bụng', 'tiền sử uống rượu', 'quá tải chất lỏng', 'máu trong đờm', 'nổi gân bắp chân', 'tức ngực', 'đau khi đi lại', 'mụn nhọt nhiều mủ', 'mụn đầu đen', 'chạy gấp', 'tróc da', 'bạc như bụi', 'vết lõm trên móng tay', 'móng tay bị viêm', 'mụn rộp', 'đau đỏ quanh mũi', 'lớp vỏ màu vàng chảy ra']
        for idx in range (len(cust_symptom)):
            for i in range (len(list_symptom)):
                if list_symptom[i] == cust_symptom[idx]:
                    print(list_symptom[i])
                    symptom[0, i] = 1
                    break
        print(symptom)
        return [FollowupAction("action_give_button_request")]

class action_prognosis(Action):
    def name(self) ->Text:
        return "action_prognosis"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        check = False
        for i in range (len(symptom[0])):
            if symptom[0, i] == 1:
                check = True
                break
        if check == False:
            dispatcher.utter_message(text = "Bạn chưa đưa ra bất kì triệu chứng nào")
            return [FollowupAction("action_give_button_start")]
        else:
            prognosis = random_fr.Predict(isTest = False, value = symptom.tolist())
            print(str(prognosis[0]))
            pos = -1
            for i in range (len(list_prognosis)):
                if prognosis[0] == list_prognosis[i]:
                    pos = i
                    break

            final_prognosis = ""
            if str(prognosis[0]) == '(vertigo) Paroymsal  Positional Vertigo':
                final_prognosis = 'Bệnh chóng mặt lành tính do tư thế'
            elif str(prognosis[0]) == 'Chronic cholestasis':
                final_prognosis = 'Ứ mật mãn tĩnh'
            elif str(prognosis[0]) == 'Dimorphic hemmorhoids(piles)':
                final_prognosis = 'Trĩ'
            elif str(prognosis[0]) == 'GERD':
                final_prognosis = 'Trào ngược dạ dày thực quản'
            elif str(prognosis[0]) == 'Impetigo':
                final_prognosis = 'Bệnh chốc'
            elif str(prognosis[0]) == 'Osteoarthristis':
                final_prognosis = 'Thoái hóa khớp'
            elif str(prognosis[0]) == 'Cervical spondylosis':
                final_prognosis = 'Thoái hóa đốt sống cổ'
            else:
                translate = Translator()
                final_prognosis = translate.translate(str(prognosis[0]), src = 'en', dest = 'vi').text
                print(final_prognosis)
            id = (tracker.current_state())["sender_id"]
            st = ""
            for i in range(len(symptom[0])):
                st = st + str(symptom[0, i])
            InsertDB(sql_path).InsertDiagnostic(id, datetime.datetime.now(), st, final_prognosis)
            print(id)        
            user = GetDB(sql_path).get_user(id)
            if user:
                cust_sex = user[2]
                bot_position = user[3]
            else:
                cust_sex = "bạn"
                bot_position = "mình"
            ret_text = "Theo " + bot_position + ", có thể " + cust_sex + " đã mắc " + final_prognosis
            for i in range (len(symptom[0])):
                symptom[0, i] = 0
            print(list_url[pos][0])
            button1 = {
                "type": "web_url",
                "title": "Thông tin về bệnh",
                "url": str(list_url[pos][0])
            }
            button2 = {
                "type": "postback",
                "title": "Lịch sử chẩn đoán",
                "payload": "Lịch sử chẩn đoán"
            }
            button3 = {
                    "type": "postback",
                    "title": "Bắt đầu tư vấn",
                    "payload": "Bắt đầu tư vấn chẩn đoán bệnh"
                }
            dispatcher.utter_message(text = ret_text, buttons = [button1, button2, button3])
        
class action_get_history(Action): 
    def name(self) ->Text:
        return "action_get_history"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        id = (tracker.current_state())["sender_id"]
        diagnostics = GetDB(sql_path).get_diagnostic(id)
        list_symptom = ['ngứa', 'phát ban da', 'phát ban nốt da', 'hắt hơi liên tục', 'rùng mình', 'ớn lạnh', 'đau khớp', 'đau dạ dày', 'thiếu axit', 'loét lưỡi', 'lãng phí cơ bắp', 'nôn mửa', 'nóng rát', 'tiểu ra máu', 'mệt mỏi', 'tăng cân', 'lo lắng', 'tay chân lạnh', 'tâm trạng lâng lâng', 'sụt cân', 'bồn chồn', 'thờ ơ', 'mảng ở cổ', 'lượng đường không đủ', 'ho', 'sốt cao', 'mắt trũng sâu', 'khó thở', 'đổ mồ hôi', 'mất nước', 'khó tiêu', 'đau đầu', 'da hơi vàng', 'nước tiểu đậm', 'buồn nôn', 'ăn mất ngon', 'đau sau mắt', 'đau lưng', 'táo bón', 'đau bụng', 'tiêu chảy', 'sốt nhẹ', 'nước tiểu vàng', 'mắt vàng', 'suy gan cấp tính', 'quá tải chất lỏng', 'sưng bụng', 'sưng hạch bạch huyết', 'phiền muộn', 'thị lực mờ, méo mó', 'đờm', 'viêm họng', 'mắt đỏ', 'xoang', 'sổ mũi', 'sung huyết', 'đau ngực', 'chân tay yếu', 'nhịp tim nhanh', 'đau khi đi nặng', 'đau hậu môn', 'phân có máu', 'ngứa hậu môn', 'đau cổ', 'chóng mặt', 'chuột rút', 'bầm tím', 'béo phì', 'sưng chân', 'sưng mạch máu', 'mắt và mặt sưng húp', 'phì đại tuyến giáp', 'móng tay dễ gãy', 'sưng tứ chi', 'đói quá mức', 'bệnh tình dục', 'môi khô và ngứa', 'nói lắp', 'đau đầu gối', 'đau khớp háng', 'yếu cơ', 'cứng cơ', 'sưng khớp', 'cử động cứng', 'chuyển động quay', 'mất thăng bằng', 'không vững vàng', 'yếu một bên cơ thể', 'mất mùi', 'bàng quang khó chịu', 'nước tiểu có mùi hôi', 'liên tục buồn tiểu', 'đầy hơi', 'ngứa bên trong', 'bệnh thương hàn', 'trầm cảm', 'dễ cáu gắt', 'đau cơ', 'thay đổi cảm giác', 'mụn đỏ trên cơ thể', 'đau bụng', 'kinh nguyệt bất thường', 'vùng đổi màu', 'chảy nước mắt', 'tăng khẩu vị', 'đa niệu', 'bệnh di truyền', 'đờm nhầy', 'đờm gỉ', 'thiếu tập trung', 'rối loạn thị giác', 'nhận truyền máu', 'tiêm không vô trùng', 'hôn mê', 'chảy máu dạ dày', 'chướng bụng', 'tiền sử uống rượu', 'quá tải chất lỏng', 'máu trong đờm', 'nổi gân bắp chân', 'tức ngực', 'đau khi đi lại', 'mụn nhọt nhiều mủ', 'mụn đầu đen', 'chạy gấp', 'tróc da', 'bạc như bụi', 'vết lõm trên móng tay', 'móng tay bị viêm', 'mụn rộp', 'đau đỏ quanh mũi', 'lớp vỏ màu vàng chảy ra']
        if diagnostics:
            for i in range (len(diagnostics)):
                ret_text = "Ngày: " + diagnostics[i][1] + '\n' + "Triệu chứng: "
                for idx in range(len(diagnostics[i][2])):
                    if diagnostics[i][2][idx] != '0':
                        ret_text = ret_text + list_symptom[idx] + ', '
                ret_text += '\n' + 'Chẩn đoán: ' + diagnostics[i][3] +'\n*******************************'
                dispatcher.utter_message(text = ret_text)
        else:
            dispatcher.utter_message(text = "Bạn chưa chẩn đoán bất kì bệnh nào trước đây!")
        return [FollowupAction("action_give_button_start")]

class action_give_ability(Action): 
    def name(self) ->Text:
        return "action_give_ability"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response = "utter_ask_ability")
        id = (tracker.current_state())["sender_id"]
        diagnostics = GetDB(sql_path).get_diagnostic(id)
        if diagnostics:
            ret_text = "Bạn cần: "
            button1 = {
                    "type": "postback",
                    "title": "Lịch sử chẩn đoán",
                    "payload": "Lịch sử chẩn đoán"
                }
            button2 = {
                    "type": "postback",
                    "title": "Bắt đầu tư vấn",
                    "payload": "Bắt đầu tư vấn chẩn đoán bệnh"
                }    
            dispatcher.utter_message(text = ret_text, buttons = [button1, button2])
        else:
            return [FollowupAction("action_give_button_start")]
