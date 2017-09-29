
# import httplib
import http.client

import json
import hashlib
import random
import time

class SmsSenderUtil:
    """ 工具类定义 """

    @staticmethod
    def get_random():
        return random.randint(100000, 999999)

    @staticmethod
    def get_cur_time():
        return int(time.time())

    def calculate_sig(self, appkey, rnd, cur_time, phone_numbers):
        phone_numbers_string = phone_numbers[0]
        for i in range(1, len(phone_numbers)):
            phone_numbers_string += "," + phone_numbers[i]
        return hashlib.sha256("appkey=" + appkey + "&random=" + str(rnd) + "&time=" + str(cur_time)
                              + "&mobile=" + phone_numbers_string).hexdigest()

    @classmethod
    def calculate_sig_for_templ_phone_numbers(cls, appkey, rnd, cur_time, phone_numbers):
        """ 计算带模板和手机号列表的 sig """
        phone_numbers_string = phone_numbers[0]
        for i in range(1, len(phone_numbers)):
            phone_numbers_string += "," + phone_numbers[i]
        return hashlib.sha256("appkey=" + appkey + "&random=" + str(rnd) + "&time="
                              + str(cur_time) + "&mobile=" + phone_numbers_string).hexdigest()

    def calculate_sig_for_templ(self, appkey, rnd, cur_time, phone_number):
        phone_numbers = [phone_number]
        return self.calculate_sig_for_templ_phone_numbers(appkey, rnd, cur_time, phone_numbers)

    def phone_numbers_to_list(self, nation_code, phone_numbers):
        tel = []
        for phone_number in phone_numbers:
            tel.append({"nationcode": nation_code, "mobile":phone_number})
        return tel

    @staticmethod
    def send_post_request(host, url, data):
        con = None
        try:
            con = http.client.HTTPSConnection(host)
            con.request('POST', url, json.dumps(data))
            response = con.getresponse()
            if '200' != str(response.status):
                obj = {}
                obj["result"] = -1
                obj["errmsg"] = "connect failed:\t"+str(response.status) + " " + response.reason
                result = json.dumps(obj)
            else:
                result = response.read()
        except Exception as e:
            obj = {}
            obj["result"] = -2
            obj["errmsg"] = "connect failed:\t" + str(e)
            result = json.dumps(obj)
        finally:
            if con:
                con.close()
        return result
