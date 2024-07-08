# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher

import requests
import json
from rasa_sdk.events import SlotSet

class ValidateRecommendForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_recommend_form"

    def validate_product(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher, 
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if slot_value.lower() == "":
            msg = "I don't recognize that product."
            dispatcher.utter_message(text=msg)
            return {"product": ""}
        # dispatcher.utter_message(text=f"Product is {slot_value}.")
        return {"product": slot_value}

    def validate_product_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher, 
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:

        if slot_value.lower() =="":
            msg = "I don't recognize that type."
            dispatcher.utter_message(text=msg)
            return {"product_type": ""}
        
 
        product_type = slot_value.lower()
        ptype = 9

        if product_type == "điện thoại":
            # Code for điện thoại product type
            ptype = 1
        elif product_type == "laptop":
            # Code for laptop product type
            ptype = 3
        elif product_type == "tablet":
            # Code for tablet product type
            ptype = 2
        else:
            msg = "I'm sorry, I don't have information for that product type."
            dispatcher.utter_message(text=msg)
            return {"product_type": ""}

        return {"product_type": ptype}
    
    def validate_budget(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher, 
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        api_url = "http://localhost:8087/api/category/"

        if slot_value =="":
            msg = "Please select among the given ranges."
            dispatcher.utter_message(text=msg)
            return {"budget": ""}
        
        

        # dispatcher.utter_message(text=f"Your budget is in range {slot_value}.")
        return {"budget": slot_value}
    
    def validate_brand(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher, 
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        if slot_value.lower() == "":
            msg = "I don't recognize that brand."
            dispatcher.utter_message(text=msg)
            return {"brand": ""}
        
        brand = slot_value.lower()
        
        # Add your code to handle different brand cases here
        
        return {"brand": slot_value}


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []
    
class ActionProvideProductInfo(Action):
    def name(self) -> Text:
        return "action_product_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product = tracker.get_slot("product")
        brand = tracker.get_slot("brand")

        # Base URL of your Spring Boot API
        api_url = "http://localhost:8087/api/product/search"

        params = {
            "page": 1,              # Trang đầu tiên
            "limit": 10,            # Giới hạn số sản phẩm trên mỗi trang (tùy chỉnh)
            "sortBy": "createdDate",   # Sắp xếp theo ngày tạo (hoặc tùy chỉnh)
            "sortValue": "DESC"
        }

        # Thêm tham số brand nếu có giá trị
        # if brand and brand != "tất cả":
        params["keyword"] = product

        # Xử lý tham số price nếu có giá trị

        params["price"] = ""  

        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("totalElements") > 0:  # Kiểm tra xem có sản phẩm hay không
                products = data.get("content")  # Lấy danh sách sản phẩm
                response_text = "Đây là kết quả tìm kiếm của bạn:\n"
                formatted_response = {
                        "payload": 'cardsCarousel',
                        "data": []
                    }
        
        # Format each product and add to the response
                for product in products:
                    formatted_product = {
                        "image": product.get("mainImage", "Default image URL if none"),
                        "title": product.get("name", "No title"),
                        "description": product.get("price", "No ratings")
                    }
                    formatted_response["data"].append(formatted_product)
                    
            
                # for product in products:
                #     response_text += f"- {product['name']} - {product['brand']} - {product['price']} USD\n"  # Tùy chỉnh hiển thị

            else:
                response_text = "No products found."

        except requests.exceptions.RequestException as e:
            response_text = "Đã có lỗi xảy ra trong quá trình tìm kiếm. Vui lòng thử lại sau."

        dispatcher.utter_message(text=response_text)
        dispatcher.utter_message(json_message=formatted_response)
        return []
    
class ActionProvideProductAvaibility(Action):
    def name(self) -> Text:
        return "action_product_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product = tracker.get_slot("product")
        dispatcher.utter_message(text=f"Thông tin số lượng sản phẩm {product}: Số lượng còn 1")
        return []

class ActionSearchProduct(Action):
    def name(self) -> Text:
        return "action_search_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        product = tracker.get_slot("product")
        brand = tracker.get_slot("brand")

        # Base URL of your Spring Boot API
        api_url = "http://localhost:8087/api/product/search"

        params = {
            "page": 1,              # Trang đầu tiên
            "limit": 10,            # Giới hạn số sản phẩm trên mỗi trang (tùy chỉnh)
            "sortBy": "createdDate",   # Sắp xếp theo ngày tạo (hoặc tùy chỉnh)
            "sortValue": "DESC"
        }

        # Thêm tham số brand nếu có giá trị
        # if brand and brand != "tất cả":
        params["brand"] = ""
        params["keyword"] = product

        # Xử lý tham số price nếu có giá trị

        params["price"] = ""  

        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("totalElements") > 0:  # Kiểm tra xem có sản phẩm hay không
                products = data.get("content")  # Lấy danh sách sản phẩm
                response_text = "Đây là kết quả tìm kiếm của bạn:\n"
                for product in products:
                    response_text += f"- {product['name']} - {product['brand']} - {product['price']} USD\n"  # Tùy chỉnh hiển thị
            else:
                response_text = "{products}"

        except requests.exceptions.RequestException as e:
            response_text = "Đã có lỗi xảy ra trong quá trình tìm kiếm. Vui lòng thử lại sau."

        dispatcher.utter_message(text=response_text)
        return []
    
class ActionProvideProductPrice(Action):
    def name(self) -> Text:
        return "action_provide_product_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product = tracker.get_slot("product")
        dispatcher.utter_message(text=f"Giá của sản phẩm {product} là 1.000.000 VNĐ.")
        return []

class ActionCheckProductAvailability(Action):
    def name(self) -> Text:
        return "action_check_product_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        product = tracker.get_slot("product")
        dispatcher.utter_message(text=f"Sản phẩm {product} hiện tại còn hàng.")
        return []

class ActionProvideDeliveryInfo(Action):
    def name(self) -> Text:
        return "action_provide_delivery_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Thông tin giao hàng: Đơn hàng sẽ được giao trong vòng 3-5 ngày làm việc.")
        return []

class ActionProvidePaymentMethods(Action):
    def name(self) -> Text:
        return "action_payment_methods"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Phương thức thanh toán: Chúng tôi chấp nhận thanh toán qua thẻ tín dụng, thẻ ghi nợ, và thanh toán khi nhận hàng.")
        return []

class ActionCheckOrderStatus(Action):
    def name(self) -> Text:
        return "action_check_order_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Tình trạng đơn hàng: Đơn hàng của bạn đang được xử lý và sẽ sớm được giao.")
        return []

class ActionProvideDeliveryTime(Action):
    def name(self) -> Text:
        return "action_delivery_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Thời gian giao hàng: Đơn hàng sẽ được giao trong vòng 3-5 ngày làm việc.")
        return []

# Action for intent ask_recommnedation
class ActionProvideRecommendation(Action):
    def name(self) -> Text:
        return "action_provide_recommendation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        product_type = tracker.get_slot("product_type")
        
        brand = tracker.get_slot("brand")
        
        budget = tracker.get_slot("budget")
        if budget == "low":
            budget = [0, 5000000]
        elif budget == "medium":
            budget = [5000000, 10000000]
        elif budget == "high":
            budget = [10000000, 99999999]
        else:
            budget = [0, 99999999]
        # Base URL of your Spring Boot API
        api_url = "http://localhost:8087/api/product/search/v2"

        params = {
            "page": 1,              # Trang đầu tiên
            "limit": 10,            # Giới hạn số sản phẩm trên mỗi trang (tùy chỉnh)
            "sortBy": "createdDate",   # Sắp xếp theo ngày tạo (hoặc tùy chỉnh)
            "sortValue": "DESC"
        }
        if product_type:
            params["cateogry"] = product_type
        if brand:
            params["brand"] = brand.lower()
        params["price"] = budget

        formatted_response = {
                        "payload": 'cardsCarousel',
                        "data": []
                    }
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data.get("totalElements") > 0:  # Kiểm tra xem có sản phẩm hay không
                products = data.get("content")  # Lấy danh sách sản phẩm
                response_text = "Đây là kết quả tìm kiếm của bạn:\n"
                formatted_response = {
                        "payload": 'cardsCarousel',
                        "data": []
                    }
        
        # Format each product and add to the response
                for product in products:
                    formatted_product = {
                        "image": product.get("mainImage", "Default image URL if none"),
                        "title": product.get("name", "No title"),
                        "description": product.get("price", "No ratings")
                    }
                    formatted_response["data"].append(formatted_product)
                         
                # for product in products:
                #     response_text += f"- {product['name']} - {product['brand']} - {product['price']} USD\n"  # Tùy chỉnh hiển thị

            else:
                response_text = "No products found."

        except requests.exceptions.RequestException as e:
            response_text = "Đã có lỗi xảy ra trong quá trình tìm kiếm. Vui lòng thử lại sau."

        dispatcher.utter_message(text=response_text)
        dispatcher.utter_message(json_message=formatted_response)
        return []
    
class ActionUtterGeneralPromotion(Action):
    def name(self) -> Text:
        return "action_utter_general_promotion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # promotions = get_promotions()
        promotions = "Giảm giá"
        if promotions:
            response = "📢 Hiện tại chúng tôi có các chương trình khuyến mãi sau:\n"
            for promotion in promotions:
                response += f"- {promotion}: {promotion}\n"
        else:
            response = "Hiện tại không có chương trình khuyến mãi nào."

        dispatcher.utter_message(text=response)
        return []


class ActionProductSpecificPromotion(Action):
    def name(self) -> Text:
        return "action_product_specific_promotion"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # product = tracker.get_slot("product")
        product = "Product #"
        promotions = "Giảm giá"
        
        if promotions:
            response = f"🎉  {product} hiện đang có các ưu đãi sau:\n"
            for promotion in promotions:
                # response += f"- {promotion['name']}: {promotion['description']}\n"
                response += f"- {promotion}"
        else:
            response = f"Hiện tại {promotions} không có khuyến mãi."

        dispatcher.utter_message(text=response)
        return []
    
class ActionClearAllSlots(Action):
    def name(self) -> Text:
        return "action_clear_all_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        slots_to_reset = [SlotSet(slot, None) for slot in tracker.slots.keys()]
        return slots_to_reset  
    
