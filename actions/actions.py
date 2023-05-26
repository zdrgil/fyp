# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import requests
from requests.auth import HTTPBasicAuth

from rasa_sdk.events import SlotSet

class ActionHelloWorld(Action):
    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # 獲取 CSRF token
        csrf_token_url = "http://192.168.110.91:8000/api/get_csrf_token/"
        response = requests.get(csrf_token_url)

        if response.status_code == 200:
            csrf_token = response.json().get("csrf_token")
            # 發送用戶信息的 API 請求
            user_id = tracker.sender_id  # 用戶的 ID，可以用於識別不同的用戶
            api_url = f"http://192.168.110.91:8000/api/users/{user_id}"
            username = "admin"
            password = "admin"

            headers = {
                "X-CSRFToken": csrf_token
            }
            response = requests.get(api_url, auth=HTTPBasicAuth(username, password), headers=headers)

            if response.status_code == 200:
                user_info = response.json()
                username = user_info.get("username")
                email = user_info.get("email")
                customer = user_info.get("customer")
                if customer:
                    customer_id = customer.get("id")
                    fullname = customer.get("fullname")
                    age = customer.get("age")
                    sex = customer.get("sex")
                    phonenumber = customer.get("phonenumber")
                    login_status = customer.get("login_status")
                    # 使用 dispatcher 將用戶信息回傳給對話流
                    dispatcher.utter_message(text=f"用戶名稱：{username}")
                    dispatcher.utter_message(text=f"電子郵件：{email}")
                    dispatcher.utter_message(text=f"顧客ID：{customer_id}")
                    dispatcher.utter_message(text=f"姓名：{fullname}")
                    dispatcher.utter_message(text=f"年齡：{age}")
                    dispatcher.utter_message(text=f"性別：{sex}")
                    dispatcher.utter_message(text=f"電話號碼：{phonenumber}")
                    dispatcher.utter_message(text=f"登錄狀態：{login_status}")
                else:
                    dispatcher.utter_message(text="無法獲取顧客信息。")
            else:
                dispatcher.utter_message(text="無法獲取用戶信息。")
        else:
            dispatcher.utter_message(text="無法獲取 CSRF token。")

        return []
    
class ActionCollectAppointmentData(Action):
    def name(self) -> Text:
        return "action_collect_appointment_data"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # 獲取用戶輸入的日期和時間
        entities = tracker.latest_message.get("entities", [])
        date = None
        time = None
        doctor = None
        customer = None
        fullname = None
        age = None
        sex = None
        clinic = None
        
        for entity in entities:
            if entity["entity"] == "date":
                date = entity["value"]
            elif entity["entity"] == "time":
                time = entity["value"]
            elif entity["entity"] == "doctor":
                time = entity["value"]
            elif entity["entity"] == "customer":
                time = entity["value"]
            elif entity["entity"] == "fullname":
                time = entity["value"]
            elif entity["entity"] == "age":
                time = entity["value"]
            elif entity["entity"] == "sex":
                time = entity["value"]
            elif entity["entity"] == "clinic":
                time = entity["value"]                        

        # 更新 slots
        return [
            SlotSet("date", date),
            SlotSet("time", time),
            SlotSet("doctor", doctor),
            SlotSet("customer", customer),
            SlotSet("fullname", fullname),
            SlotSet("age", age),
            SlotSet("sex", sex),
            SlotSet("clinic", clinic),
            
        ]


class ActionSubmitAppointment(Action):
    def name(self) -> Text:
        return "action_submit_appointment"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # 获取 slots 中的数据
        date = tracker.get_slot("date")
        time = tracker.get_slot("time")
        doctor = int(tracker.get_slot("doctor"))
        customer = int(tracker.get_slot("customer"))
        fullname = tracker.get_slot("fullname")
        age = int(tracker.get_slot("age"))
        sex = tracker.get_slot("sex").lower()
        clinic = int(tracker.get_slot("clinic"))

        # 其他预约相关的数据也可以从 slots 中获取

        # 在这里实现提交预约的逻辑，例如保存到数据库或调用 API

        dispatcher.utter_message("Date: " + date)
        dispatcher.utter_message("Time: " + time)
        dispatcher.utter_message("Doctor: " + str(doctor))
        dispatcher.utter_message("Customer: " + str(customer))
        dispatcher.utter_message("Fullname: " + fullname)
        dispatcher.utter_message("Age: " + str(age))
        dispatcher.utter_message("Sex: " + sex)
        dispatcher.utter_message("Clinic: " + str(clinic))

        csrf_token_url = "http://192.168.110.91:8000/api/get_csrf_token/"
        response = requests.get(csrf_token_url)

        if response.status_code == 200:
            csrf_token = response.json().get("csrf_token")
            # 发送用户信息的 API 请求
            user_id = tracker.sender_id  # 用户的 ID，可以用于识别不同的用户
            api_url = f"http://192.168.110.91:8000/api/users/{user_id}"
            username = "admin"
            password = "admin"

            headers = {
                "X-CSRFToken": csrf_token
            }
            response = requests.get(api_url, auth=HTTPBasicAuth(username, password), headers=headers)
            if response.status_code == 200:
                api_url2 = "http://192.168.110.91:8000/api/register_appointment/"

                payload = {
                    "date": date,
                    "time": time,
                    "doctor": doctor,
                    "customer": customer,
                    "fullname": fullname,
                    "age": age,
                    "sex": sex,
                    "clinic": clinic
                }

                response2 = requests.post(api_url2, auth=HTTPBasicAuth(username, password), headers=headers, json=payload)

                if response2.status_code == 201:
                    dispatcher.utter_message("预约已提交。")
                else:
                    dispatcher.utter_message(text="无法提交预约。")
            else:
                dispatcher.utter_message(text="无法获取用户信息。")
        else:
            dispatcher.utter_message(text="无法获取 CSRF 令牌。")

        return []
    
class ActionAskDate(Action):
    def name(self) -> Text:
        return "action_ask_date"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="請提供預約的日期,格式為YY|MM|DD。")
        return []
    
class ActionAskDoctor(Action):
    def name(self) -> Text:
        return "action_ask_doctor"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        csrf_token_url = "http://192.168.110.91:8000/api/get_csrf_token/"
        response = requests.get(csrf_token_url)

        if response.status_code == 200:
            csrf_token = response.json().get("csrf_token")
            # 发送用户信息的 API 请求
            user_id = tracker.sender_id  # 用户的 ID，可以用于识别不同的用户
            api_url = f"http://192.168.110.91:8000/api/users/{user_id}"
            username = "admin"
            password = "admin"

            headers = {
                "X-CSRFToken": csrf_token
            }
            response = requests.get(api_url, auth=HTTPBasicAuth(username, password), headers=headers)
            if response.status_code == 200:
                api_url2 = "http://192.168.110.91:8000/api/clinics/"
                response = requests.get(api_url2, auth=HTTPBasicAuth(username, password), headers=headers)
                if response.status_code == 200:
                    clinic_data = response.json()
                    for clinic in clinic_data:
                        clinic_id = clinic.get("id")
                        clinic_name = clinic.get("clinicname")
                        doctors = clinic.get("doctors")
                        if doctors:
                            for doctor in doctors:
                                doctor_id = doctor.get("id")
                                doctor_name = doctor.get("name")
                                message = f"Name: {clinic_name}, Doctor ID: {doctor_id}, Doctor Name: {doctor_name}"
                                dispatcher.utter_message(text=message)
                         

                        else:
                            dispatcher.utter_message(text=f"Clinic ID: {clinic_id}, Name: {clinic_name}, 无法获取医生信息。")
                           
                else:
                    dispatcher.utter_message(text="无法获取诊所列表。")
                dispatcher.utter_message(text="輸入Doctor ID")    
        else:
            dispatcher.utter_message(text="无法获取 CSRF token。")

        return []




class ActionAskTime(Action):
    def name(self) -> Text:
        return "action_ask_time"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="請提供預約的時間,格式為HH|MM|SS。")
        return []
    
class ActionAskFullname(Action):
    def name(self) -> Text:
        return "action_ask_fullname"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="請提供預約人的全名")
        return []    
    
class ActionAskAge(Action):
    def name(self) -> Text:
        return "action_ask_age"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="請提供預約的年紀")
        return []    
    
class ActionAskSex(Action):
    def name(self) -> Text:
        return "action_ask_sex"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="請提供預約人的性別")
        return []     
           

    

    

import re

class ActionStoreDate(Action):
    def name(self) -> Text:
        return "action_store_date"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # 獲取用戶提供的日期
        date = tracker.latest_message.get("text")
        
        # 檢查日期格式
        if not re.match(r"\d{4}-\d{2}-\d{2}", date):
            dispatcher.utter_message(text="請提供有效的日期格式，格式為2023-05-31。")
            return []
        
        # 更新 slot 中的日期
        return [SlotSet("date", date)]


class ActionStoreTime(Action):
    def name(self) -> Text:
        return "action_store_time"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # 獲取用戶提供的時間
        time = tracker.latest_message.get("text")
        
        # 檢查時間格式
        if not re.match(r"\d{2}:\d{2}:\d{2}", time):
            dispatcher.utter_message(text="請提供有效的時間格式，格式為HH:MM:SS。")
            return []
        
        # 更新 slot 中的時間
        return [SlotSet("time", time)] 
    
class ActionStoreDoctor(Action):
    def name(self) -> Text:
        return "action_store_doctor"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # 获取用户提供的医生 ID
        message = tracker.latest_message.get("text")
        doctor_id = None

        # 使用正则表达式查找医生 ID
        match = re.search(r"\b(\d+)\b", message)
        if match:
            doctor_id = match.group(1)

            csrf_token_url = "http://192.168.110.91:8000/api/get_csrf_token/"
            response = requests.get(csrf_token_url)

            if response.status_code == 200:
                csrf_token = response.json().get("csrf_token")
                # 发送用户信息的 API 请求
                user_id = tracker.sender_id  # 用户的 ID，可以用于识别不同的用户
                api_url = f"http://192.168.110.91:8000/api/users/{user_id}"
                username = "admin"
                password = "admin"

                headers = {
                    "X-CSRFToken": csrf_token
                }
                response = requests.get(api_url, auth=HTTPBasicAuth(username, password), headers=headers)
                if response.status_code == 200:
                    api_url2 = f"http://192.168.110.91:8000/api/doctors/{doctor_id}"
                    
                    # 发送医生信息的 API 请求
                    response = requests.get(api_url2, auth=HTTPBasicAuth(username, password), headers=headers)
                    
                    if response.status_code == 200:
                        doctor_info = response.json()
                        doctor = str(doctor_info.get("id"))
                        clinic = str(doctor_info.get("clinic"))

                        # 更新 slot 中的医生和诊所信息
                        slot_values = [
                            SlotSet("doctor", doctor),
                            SlotSet("clinic", clinic)
                        ]

                        return slot_values
                    
                    else:
                        dispatcher.utter_message(text="无法获取医生信息。")
                else:
                    dispatcher.utter_message(text="无法获取用户信息。")
            else:
                dispatcher.utter_message(text="无法获取 CSRF 令牌。")
        else:
            dispatcher.utter_message(text="无法从句子中提取医生 ID。")

        return []


    
class ActionStoreFullname(Action):
    def name(self) -> Text:
        return "action_store_fullname"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # 獲取用戶提供的醫生名字
        fullname = tracker.latest_message.get("text")

        # 檢查醫生名字格式
       

        # 更新 slot 中的醫生名字
        return [SlotSet("fullname", fullname)]      
    
class ActionStoreSex(Action):
    def name(self) -> Text:
        return "action_store_sex"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # 獲取用戶提供的性別
        sex = tracker.latest_message.get("text")

        # 檢查性別格式
        if not re.match(r"^(male|female)$", sex, re.IGNORECASE):
            dispatcher.utter_message(text="請提供有效的性別，只能是 male 或 female。")
            return []

        # 更新 slot 中的性別
        return [SlotSet("sex", sex)]    
    
class ActionStoreAge(Action):
    def name(self) -> Text:
        return "action_store_age"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # 獲取用戶提供的文本
        text = tracker.latest_message.get("text")
        
        # 使用正則表達式匹配年齡數字
        age_match = re.search(r"\b(\d+)\b", text)
        
        if age_match:
            age = str(age_match.group(1))  # 将匹配到的数字转换为字符串
            return [SlotSet("age", age)]
        else:
            dispatcher.utter_message(text="無法從文本中識別年齡數字。請提供有效的年齡信息。")
            return []       
     
    
class ActionStoreCustomer(Action):
    def name(self) -> Text:
        return "action_store_customer"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        csrf_token_url = "http://192.168.110.91:8000/api/get_csrf_token/"
        response = requests.get(csrf_token_url)

        if response.status_code == 200:
            csrf_token = response.json().get("csrf_token")
            # 發送用戶信息的 API 請求
            user_id = tracker.sender_id  # 用戶的 ID，可以用於識別不同的用戶
            api_url = f"http://192.168.110.91:8000/api/users/{user_id}"
            username = "admin"
            password = "admin"

            headers = {
                "X-CSRFToken": csrf_token
            }
            response = requests.get(api_url, auth=HTTPBasicAuth(username, password), headers=headers)

            if response.status_code == 200:
                user_info = response.json()
                username = user_info.get("username")
                email = user_info.get("email")
                customer = user_info.get("customer")
                if customer:
                    customer_id = customer.get("id")
                    fullname = customer.get("fullname")
                    age = customer.get("age")
                    sex = customer.get("sex")
                    phonenumber = customer.get("phonenumber")
                    login_status = customer.get("login_status")
                    # 使用 dispatcher 將用戶信息回傳給對話流

                else:
                    dispatcher.utter_message(text="無法獲取顧客信息。")
            else:
                dispatcher.utter_message(text="無法獲取用戶信息。")
        else:
            dispatcher.utter_message(text="無法獲取 CSRF token。")
        customer = str(customer_id)
    
    
        return [SlotSet("customer", customer)]

  
class ActionRecordChatLog(Action):
    def name(self) -> Text:
        return "action_record_chatlog"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # 获取 CSRF 令牌
        csrf_token_url = "http://192.168.110.91:8000/api/get_csrf_token/"
        response = requests.get(csrf_token_url)
        csrf_token = response.json().get("csrf_token")
        sender_id = tracker.sender_id
        chatlog = tracker.latest_message.get("text")
        headers = {
            "X-CSRFToken": csrf_token
        }

        api_url = "http://192.168.110.91:8000/api/chatlogs/"
        payload = {
            "message": chatlog,
            "sender": sender_id,
        }

        # 发送聊天日志的 API 请求
        auth = HTTPBasicAuth('admin', 'admin')  # 替换为实际的用户名和密码
        response = requests.post(api_url, headers=headers, json=payload, auth=auth)

        return []







 
    
 


