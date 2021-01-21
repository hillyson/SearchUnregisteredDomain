# -*- coding: utf-8 -*-
import copy
import unittest

import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import threadpool

class __init__(unittest.TestCase):
    def setUp(self):
        # 使用chromedriver
        # self.driver = webdriver.Chrome()
        # self.driver = webdriver.Chrome(r"C:\Users\caihy\AppData\Local\Programs\Python\Python35\chromedriver.exe") # Windows Path
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)


        # 使用HTMLunit
        # 通过下载https://github.com/sveneisenschmidt/selenium-server-standalone/blob/master/bin/selenium-server-standalone.jar
        # 运行java -jar selenium-server-standalone.jar -port 4444启动服务后再运行
        # self.driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub',desired_capabilities=webdriver.DesiredCapabilities.HTMLUNIT)


        self.driver.implicitly_wait(30)
        self.verificationErrors = []
        self.accept_next_alert = True

        self.pool = threadpool.ThreadPool(10)
        self.result_url_list = []

    def test_123(self):
        url_list = self.get_url_list()
        start_time = time.time()
        requests = threadpool.makeRequests(self.is_registered, url_list)
        [self.pool.putRequest(req) for req in requests]
        self.pool.wait()
        print('%d second' % (time.time() - start_time))
        for url in self.result_url_list:
            print("Unregistered:" + url)

    def is_registered(self, url):
        start_time = time.time()
        driver = self.driver
        try:
            driver.get(url)
        except WebDriverException:
            True
        try:
            # aliyun的特征
            # driver.find_element_by_class_name("delegate-buy-bt")

            # chinaz的特征
            driver.find_element_by_class_name("WhoisWrap")

            return True
        except NoSuchElementException:
            try:
                driver.find_element_by_class_name("fz16 YaHei tc")
                self.result_url_list.append(url)
                print("Unregistered or Timeout:" + url)
                return False
            except NoSuchElementException:
                return True
        finally:
            print(url, (time.time() - start_time))

    @staticmethod
    # 生成需要扫描的数字域名列表
    def get_url_list():
        max_digit = 1 # 数字域名的最大位数
        num_list = __init__.generate_num(max_digit)
        return __init__.get_url_string_list_from_num(num_list)

    @staticmethod
    # 根据数字矩阵生成数字域名列表
    def get_url_string_list_from_num(num_list):
        url_string_list = []
        # format_string = "https://whois.aliyun.com/whois/domain/{0}.com"
        format_string = "http://whois.chinaz.com/{0}.com"
        for item in num_list:
            #item为一维数字数组,把其序列化数字字符串
            join_num = "".join([str(x) for x in item])
            #格式化成域名字符串
            format_url = format_string.format(join_num)
            url_string_list.append(format_url)
        return url_string_list

    @staticmethod
    # 生成数字域名矩阵
    def generate_num(max_digit):
        num_list = []
        for index in range(0, max_digit):
            # 若结果数组为空,初始化第一位遍历的所有结果,其余位都为0
            if index == 0:
                for i in range(0, 10):
                    # 按照max_digit生成初始数组,例如:[0, 0, 0, 0, 0]
                    add_item = []
                    for x in range(0, max_digit):
                        add_item.append(0)
                    # 把第一位改为对应数字
                    add_item[index] = i
                    # 得出结果,例如:[[0,0,0,0,0],
                    #              [1,0,0,0,0],
                    #              [2,0,0,0,0],
                    #              [3,0,0,0,0],
                    #              [4,0,0,0,0],
                    #              [5,0,0,0,0]]
                    num_list.append(add_item)
            # 若数组不为空,递归遍历
            else:
                # 给指定数位赋值0-9的数字,要深复制出各个数组
                copy_num_list = copy.deepcopy(num_list)
                for i in range(1, 10):
                    add_copy_num_list = copy.deepcopy(copy_num_list)
                    for item_index in range(0, len(add_copy_num_list)):
                        add_copy_num_list[item_index][index] = i
                    # 把新数组合并进目标数组
                    num_list.extend(add_copy_num_list)
        print(len(num_list))
        return num_list

    @staticmethod
    def is_alert_present():
        # try: self.driver.switch_to_alert()
        # except NoAlertPresentException, e: return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to.alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True

    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


if __name__ == "__main__":
    unittest.main()
