#!/Users/jinlinxiao/py_env/selenium_env/bin/python
# -*- coding: utf-8 -*-
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import datetime
import time
import sys
from nose.tools import nottest


class WaitElement(object):

    def __init__(self, by, value):
        self.by = by
        self.value = value

    def __call__(self, driver):
        return driver.find_element(self.by, self.value)


class WaitElements(object):

    def __init__(self, by, value, el_len=1):
        self.by = by
        self.value = value
        self.element_len = el_len

    def __call__(self, driver):
        elements = driver.find_elements(self.by, self.value)
        if len(elements) >= self.element_len:
            return True
        else:
            return False
        # return driver.find_element(self.by, self.value)


class TestFlightBase(unittest.TestCase):
    flight_form_id = "js_flight_domestic_searchbox"

    __name__ = "TestQunarFlight"

    def init_driver(self):
        """
        初始化web driver
        :return:
        """
        self.browser = webdriver.Chrome()
        # self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(15)

    def get_index(self):
        """
        进入去哪儿首页
        :return:
        """
        self.browser.get("https://www.qunar.com")
        # 最大化浏览器
        self.browser.maximize_window()
        # 默认为单程
        self.is_roundtrip = False

    def enter_flight(self):
        """
        进入机票搜索标签页
        :return:
        """
        WebDriverWait(self.browser, 1).until(WaitElement(By.CLASS_NAME, 'c_flight'))
        self.browser.find_element(By.CLASS_NAME, "c_flight").click()

    def set_search_type(self):
        """
        设置搜索类型，是单程或往返?
        :return:
        """
        if self.is_roundtrip:
            self.browser.find_element(By.ID, "js_searchtype_roundtrip").click()
        else:
            self.browser.find_element(By.ID, "js_searchtype_oneway").click()

    def set_from_city(self, from_city):
        """
        设置出发城市
        :param from_city: 出发城市 unicode 编码
        :return:
        """
        from_city_el = self.browser.find_element_by_id(self.flight_form_id).find_element_by_name("fromCity")
        from_city_el.clear()
        # for i in range(10):
        #     from_city_el.send_keys(Keys.BACKSPACE)
        from_city_el.send_keys(from_city)
        WebDriverWait(self.browser, 2).until(WaitElement(By.CLASS_NAME, 'keyString'))
        self.browser.find_element(By.CLASS_NAME, "keyString").click()

    def set_to_city(self, to_city):
        """
        设置到达城市
        :param to_city: 到达城市 unicode 编码
        :return:
        """
        to_city_el = self.browser.find_element(By.ID, self.flight_form_id).find_element(By.NAME, "toCity")
        to_city_el.clear()
        to_city_el.send_keys(to_city)
        time.sleep(0.5)
        keys_str_els = self.browser.find_elements(By.CLASS_NAME, "keyString")
        if len(keys_str_els) > 1:
            keys_str_els[1].click()

    def change_city(self):
        """
        click 换，调换出发和到达城市
        :return:
        """
        self.browser.find_element(By.ID, self.flight_form_id).find_element(By.CLASS_NAME, "lnk_change").click()

    def select_from_city(self, is_all=False):
        """
        通过城市选择框选择出发城市
        :param is_all: 是否选择all
        :return:
        """
        city_control_el = self.browser.find_element(By.ID, self.flight_form_id).find_element(By.CLASS_NAME, "crl_sp2_1")
        from_city_ctl_el = city_control_el.find_elements(By.CLASS_NAME, "controls")[0]
        from_city_ctl_el.find_element(By.CLASS_NAME, "qcbox-info").click()  # 调取选择框
        # from_city_el = self.browser.find_element_by_id(self.flight_form_id).find_element_by_name("fromCity")
        # from_city_el.click()  # 调取选择框
        time.sleep(0.1)
        if is_all:
            # 选择最后一个标签
            from_city_ctl_el.find_element(By.CLASS_NAME, "m-hct-nav").find_elements(By.TAG_NAME, "span")[-1].click()
            citys_el = from_city_ctl_el.find_elements(By.CLASS_NAME, "m-hct-lst")[-1].find_elements(By.TAG_NAME, "li")
            # 点击 最后一个城市
            citys_el[-1].find_element(By.TAG_NAME, "a").click()
        else:
            # todo 选择的index通过读取入参完成
            index = 0
            # 点击 nav 的第一个标签：国内热门
            from_city_ctl_el.find_element(By.CLASS_NAME, "m-hct-nav").find_elements(By.TAG_NAME, "span")[index].click()
            citys_el = from_city_ctl_el.find_elements(By.CLASS_NAME, "m-hct-lst")[index].find_elements(By.TAG_NAME, "li")
            # 点击 国内热门下面的第2个城市
            citys_el[1].find_element(By.TAG_NAME, "a").click()

    def select_to_city(self, is_all=False):
        """
        通过城市选择框选择到达城市
        :param is_all: 是否选择all
        :return:
        """
        city_control_el = self.browser.find_element(By.ID, self.flight_form_id).find_element(By.CLASS_NAME, "crl_sp2_1")
        to_city_ctl_el = city_control_el.find_elements(By.CLASS_NAME, "controls")[1]

        # to_city_el = self.browser.find_element_by_id(self.flight_form_id).find_element_by_name("toCity")
        # self.browser.get_screenshot_as_file("1.png")
        to_city_ctl_el.find_element(By.CLASS_NAME, "qcbox-info").click()  # 调取选择框
        # self.browser.get_screenshot_as_file("2.png")
        time.sleep(0.1)
        if is_all:
            # 选择最后一个标签
            to_city_ctl_el.find_element(By.CLASS_NAME, "m-hct-nav").find_elements(By.TAG_NAME, "span")[-1].click()
            citys_el = to_city_ctl_el.find_elements(By.CLASS_NAME, "m-hct-lst")[-1].find_elements(By.TAG_NAME, "li")
            # 点击 最后一个城市
            citys_el[-1].find_element(By.TAG_NAME, "a").click()
        else:
            # todo 选择的index通过读取入参完成
            # 点击 ABCDE
            index = 1
            to_city_ctl_el.find_element(By.CLASS_NAME, "m-hct-nav").find_elements(By.TAG_NAME, "span")[index].click()
            citys_el = to_city_ctl_el.find_elements(By.CLASS_NAME, "m-hct-lst")[index].find_elements(By.TAG_NAME, "li")
            # 点击 ABCDE 下面的第3个城市
            citys_el[2].find_element(By.TAG_NAME, "a").click()

    def set_from_date(self, from_date):
        """
        设置出发时间
        :param from_date:
        :return:
        """
        self.browser.execute_script("document.querySelector('#js_domestic_fromdate').value='%s';" % from_date)

    def set_to_date(self, to_date):
        """
        设置返程时间
        :param to_date:
        :return:
        """
        self.browser.execute_script("document.querySelector('#js_domestic_todate').value='%s';" % to_date)

    def submit(self):
        """
        发起搜索请求
        :return:
        """
        self.browser.find_element_by_id(self.flight_form_id).find_element_by_class_name("button-search").submit()

    def check_search_type(self):
        """
        校验单程or往返
        :return:
        """
        if self.is_roundtrip:
            check_text = u"往返"
        else:
            check_text = u"单程"
        self.assertEqual(check_text,
                         self.browser.find_element(By.ID, "searchboxForm").find_elements(By.CLASS_NAME, "yselector_input")[1].text)

    def check_oneway_to_any_city(self, from_city, from_date):
        """
        校验单程情况下，输入from_city和from_date，到达城市为默认值时的返回情况
        :param from_city: 出发城市
        :param from_date: 出发时间(格式为:xx月xx日)
        :return:
        """
        WebDriverWait(self.browser, 10).until(WaitElement(By.ID, 'list-box'))
        self.assertTrue(u"去哪儿" in self.browser.title)
        plsts = self.browser.find_elements(By.CLASS_NAME, "b-plst")
        for plst in plsts:
            print plst.find_element(By.CLASS_NAME, "a-city").text.encode('utf-8')
            print plst.find_element(By.CLASS_NAME, "a-time").text.encode('utf-8')
            self.assertTrue(from_city in plst.find_element(By.CLASS_NAME, "a-city").text)
            self.assertTrue(from_date in plst.find_element(By.CLASS_NAME, "a-time").text)

    def check_roundtrip_to_any_city(self, from_city, from_date, to_date):
        """
        校验返程情况下，输入from_city和from_date、to_date，到达城市为默认值时的返回情况
        :param from_city: 出发城市
        :param from_date: 出发时间(格式为:xx月xx日)
        :param to_date: 返程时间(格式为:xx月xx日)
        :return:
        """
        WebDriverWait(self.browser, 10).until(WaitElement(By.ID, 'list-box'))
        self.assertTrue(u"去哪儿" in self.browser.title)
        plsts = self.browser.find_elements(By.CLASS_NAME, "b-plst")
        for plst in plsts:

            print plst.find_element(By.CLASS_NAME, "a-city").text.encode('utf-8')

            self.assertTrue(from_city in plst.find_element(By.CLASS_NAME, "a-city").text)
            a_time_els = plst.find_elements(By.CLASS_NAME, "a-time")

            # debug print
            for a_time_el in a_time_els:
                print a_time_el.text.encode('utf-8')
            # 往返 这里展示是两组时间信息 一去一回，所以长度是2
            self.assertEqual(2, len(a_time_els))
            self.assertTrue(from_date in a_time_els[0].text)
            self.assertTrue(u"去" in a_time_els[0].text)
            self.assertTrue(to_date in a_time_els[1].text)
            self.assertTrue(u"回" in a_time_els[1].text)

    def get_search_date(self, offset=0):
        """
        获取搜索的date，搜索时输入和check时的格式不一样，这里统一进行转换
        :param offset:
        :return:搜索输入时间和搜索结果校验时间
        """
        today = datetime.datetime.now()
        offset_day = datetime.timedelta(days=offset)
        out_day = today + offset_day
        d_qry = out_day.strftime("%Y-%m-%d")
        d_check = out_day.strftime("%m月%d日")
        # print type(d_check.decode('utf-8'))
        return d_qry, d_check.decode('utf-8')

    def setUp(self):
        self.is_roundtrip = False
        self.init_driver()
        self.get_index()
        self.enter_flight()

    def tearDown(self):
        time.sleep(2)
        self.browser.quit()

    def check_airfly_list(self):
        """
        校验 airfly_list
        :return:
        """
        self.assertTrue(u"去哪儿" in self.browser.title)
        self.assertTrue(self.browser.find_element(By.CLASS_NAME, "m-airfly-lst"))
        # print len(self.browser.find_elements(By.CLASS_NAME, "b-airfly"))
        for index, e_airfly in enumerate(self.browser.find_elements(By.CLASS_NAME, "b-airfly")):
            print "机票信息 %s：" % index
            s_trips = e_airfly.find_elements(By.CLASS_NAME, "s-trip")
            self.assertEqual(2, len(s_trips))
            print "==== 去 ===="
            self.check_s_trip(s_trips[0])
            print "==== 回 ===="
            self.check_s_trip(s_trips[1])
            print "+" * 8

    def check_s_trip(self, el):
        """
        解析和校验输入两个城市并且有返程时的机票信息
        :param el:
        :return:
        """
        airline = el.find_element(By.CLASS_NAME, "col-airline")
        air_el = airline.find_element(By.CLASS_NAME, "air")
        self.assertTrue(air_el.find_element(By.TAG_NAME, "img"))
        self.assertTrue(air_el.find_element(By.TAG_NAME, "span").text)
        self.assertTrue(len(airline.find_elements(By.CLASS_NAME, "n")) == 2)
        airfly_info = "%s_%s_%s" % (
            air_el.find_element(By.TAG_NAME, "span").text.encode('utf-8'),
            airline.find_elements(By.CLASS_NAME, "n")[0].text.encode('utf-8'),
            airline.find_elements(By.CLASS_NAME, "n")[1].text.encode('utf-8')
        )
        print airfly_info
        time_el = el.find_element(By.CLASS_NAME, "col-time")
        self.assertTrue(time_el)
        lf_el = time_el.find_element(By.CLASS_NAME, "sep-lf")
        # print lf_el.find_element(By.TAG_NAME, "h2").text
        # for el in lf_el.find_elements(By.TAG_NAME, "span"):
        #     print el.text
        lf_info = "depart time:%s,airport:%s %s" % (
            lf_el.find_element(By.TAG_NAME, "h2").text.encode('utf-8'),
            lf_el.find_elements(By.TAG_NAME, "span")[0].text.encode('utf-8'),
            lf_el.find_elements(By.TAG_NAME, "span")[1].text.encode('utf-8')  #.encode('utf-8')
        )
        # print "type lf_info", type(lf_info)
        ct_info = time_el.find_element(By.CLASS_NAME, "range").text
        # print type(ct_info)
        rt_el = time_el.find_element(By.CLASS_NAME, "sep-rt")
        # print type(rt_el.find_element(By.TAG_NAME, "h2").text)
        # for el in lf_el.find_elements(By.TAG_NAME, "span"):
        #     print type(el.text)
        rt_info = "arrive time:%s,airport:%s-%s" % (
            rt_el.find_element(By.TAG_NAME, "h2").text.encode('utf-8'),
            rt_el.find_elements(By.TAG_NAME, "span")[0].text.encode('utf-8'),
            rt_el.find_elements(By.TAG_NAME, "span")[1].text.encode('utf-8')
        )
        print "航班信息: %s;range:%s;%s" % (lf_info, ct_info.encode('utf-8'), rt_info)

    def check_fuzzy_list(self):
        """
        针对 test_roundtrip_select_city_all 的校验，查询结果存储于 class=m-fuzzylst 的节点下
        :return:
        """
        e_nav_el = self.browser.find_element(By.CLASS_NAME, 'm-fuzzylst').find_element(By.CLASS_NAME, "e-nav")
        for loc_city in e_nav_el.find_element(By.ID, "loc_id").find_elements(By.TAG_NAME, "p"):
            self.assertEqual(u"所有地点", loc_city.text)
        fu_de_lst_el = self.browser.find_element(By.ID, "fu_de_lst_id")
        for lst_el in fu_de_lst_el.find_elements(By.TAG_NAME, "li"):
            ct = lst_el.find_element(By.CLASS_NAME, "col_ct").text.encode('utf-8')
            pr = lst_el.find_element(By.CLASS_NAME, "col_pr").find_elements(By.TAG_NAME, "span")[0].text.encode('utf-8')
            print "国家\地区: %s, 每位成人价格: %s." % (ct, pr)


class TestFlightOneWay(TestFlightBase):

    __name__ = "TestFlightOneWay"

    @nottest
    def test_oneway_normal(self):
        """
        单程-直接输入城市，查找单程机票信息
        :return:
        """
        try:
            from_city = u"上海"
            to_city = u"拉萨"
            from_date, from_date_check = self.get_search_date(offset=6)
            self.set_search_type()
            self.set_from_city(from_city)
            self.set_to_city(to_city)
            self.set_from_date(from_date)
            self.set_search_type()
            # todo can't check so set wait=1 to quit browser
            self.browser.implicitly_wait(1)
            self.submit()

            # self.is_roundtrip = True
            # from_city = u"上海"
            # to_city = u"拉萨"
            # from_date, from_date_check = self.get_search_date(offset=6)
            # to_date, to_date_check = self.get_search_date(offset=6 + 3)
            # self.set_search_type()
            # self.set_from_city(from_city)
            # self.set_to_city(to_city)
            # self.set_from_date(from_date)
            # self.set_to_date(to_date)
            # # self.submit()
            # self.is_roundtrip = False
            # self.set_search_type()
            # self.submit()
            #
            # # check
            # WebDriverWait(self.browser, 5).until(WaitElement(By.CLASS_NAME, 'm-airfly-lst'))
            # todo
        except Exception, e:
            print sys.exc_info()
            print e.message
            # self.browser.get_screenshot_as_file("test_oneway_normal.png")
            raise

    @nottest
    def test_oneway_select_city_noraml(self):
        """
        单程-选择出发城市和到达城市，查询单程机票信息
        :return:
        """
        # from_date, from_date_check = self.get_search_date(offset=6)
        self.select_from_city()
        self.select_to_city()
        # todo can't check so set wait=1 to quit browser
        self.browser.implicitly_wait(1)
        self.submit()

    def test_oneway_select_city_any(self):
        """
        单程-只选择出发城市，查询单程机票信息
        :return:
        """
        # from_date, from_date_check = self.get_search_date(offset=6)
        self.select_from_city()
        # self.select_to_city()
        # todo can't check so set wait=1 to quit browser
        self.browser.implicitly_wait(1)
        self.submit()

    def test_oneway_to_any_city_1(self):
        """
        单程-到达城市传空-查询结果检查
        :return:
        """
        try:
            from_city = u"上海"
            from_date, from_date_check = self.get_search_date(offset=6)
            self.set_from_city(from_city)
            self.set_from_date(from_date)
            self.submit()
            self.check_search_type()
            self.check_oneway_to_any_city(from_city, from_date_check)
        except Exception, e:
            print sys.exc_info()
            print e.message
            # self.browser.get_screenshot_as_file("test_oneway_to_any_city_1.png")
            raise


class TestFlightRoundTrip(TestFlightBase):

    __name__ = "TestFlightRoundTrip"

    def test_roundtrip_normal(self):
        """
        往返-输入出发城市和到达城市以及出发时间、返程时间，查询机票信息
        :return:
        """
        try:
            self.is_roundtrip = True
            from_city = u"上海"
            to_city = u"拉萨"
            from_date, from_date_check = self.get_search_date(offset=6)
            to_date, to_date_check = self.get_search_date(offset=6 + 3)
            self.set_search_type()
            self.set_from_city(from_city)
            self.set_to_city(to_city)
            self.set_from_date(from_date)
            self.set_to_date(to_date)
            self.submit()

            # check
            # todo
            WebDriverWait(self.browser, 10).until(WaitElement(By.CLASS_NAME, 'm-airfly-lst'))
            # self.browser.get_screenshot_as_file("test_roundtrip_normal.png")
            self.check_airfly_list()
        except Exception, e:
            print sys.exc_info()
            print e.message
            # self.browser.get_screenshot_as_file("test_oneway_normal.png")
            raise

    def test_roundtrip_select_city_normal(self):
        """
        往返-在选择框选择出发城市和到达城市以及出发时间、返程时间，查询机票信息
        :return:
        """
        try:
            self.is_roundtrip = True
            from_date, from_date_check = self.get_search_date(offset=6)
            to_date, to_date_check = self.get_search_date(offset=6 + 3)
            self.set_search_type()
            self.select_from_city()
            self.select_to_city()
            self.set_from_date(from_date)
            self.set_to_date(to_date)
            self.submit()

            # check
            # todo
            WebDriverWait(self.browser, 10).until(WaitElement(By.CLASS_NAME, 'm-airfly-lst'))
            self.check_airfly_list()
        except Exception, e:
            print sys.exc_info()
            print e.message
            # self.browser.get_screenshot_as_file("test_oneway_normal.png")
            raise

    def test_roundtrip_select_city_chg(self):
        """
        往返-在选择框选择出发城市和到达城市以及出发时间、返程时间,调换出发和到达城市，查询机票信息
        :return:
        """
        try:
            self.is_roundtrip = True
            from_date, from_date_check = self.get_search_date(offset=6)
            to_date, to_date_check = self.get_search_date(offset=6 + 3)
            self.set_search_type()
            self.select_from_city()
            self.select_to_city()
            self.set_from_date(from_date)
            self.set_to_date(to_date)
            # 调换城市
            self.change_city()
            self.submit()

            # check
            # todo
            WebDriverWait(self.browser, 10).until(WaitElement(By.CLASS_NAME, 'm-airfly-lst'))
            self.check_airfly_list()
        except Exception, e:
            print sys.exc_info()
            print e.message
            # self.browser.get_screenshot_as_file("test_oneway_normal.png")
            raise

    def test_roundtrip_sel_city_to_all(self):
        """
        往返-从一个城市到所有地点，查询机票信息
        :return:
        """
        self.is_roundtrip = True
        from_date, from_date_check = self.get_search_date(offset=6)
        to_date, to_date_check = self.get_search_date(offset=6 + 3)
        self.set_search_type()
        self.set_from_city(u"上海")  # 输入深圳时，查询不到航班信息
        self.select_to_city(is_all=True)
        self.set_from_date(from_date)
        self.set_to_date(to_date)
        self.submit()
        # todo check
        # 展示的页面不一样 list-box

    def test_roundtrip_select_city_all(self):
        """
        往返-在选择框选择出发城市和到达城市都为"所有城市"，选择出发时间、返程时间，查询机票信息
        :return:
        """
        try:
            self.is_roundtrip = True
            from_date, from_date_check = self.get_search_date(offset=6)
            to_date, to_date_check = self.get_search_date(offset=6 + 3)
            self.set_search_type()
            self.select_from_city(is_all=True)
            self.select_to_city(is_all=True)
            self.set_from_date(from_date)
            self.set_to_date(to_date)
            self.submit()

            # check
            # todo
            WebDriverWait(self.browser, 10).until(WaitElement(By.CLASS_NAME, 'm-fuzzylst'))
            self.check_fuzzy_list()
        except Exception, e:
            print sys.exc_info()
            print e.message
            # self.browser.get_screenshot_as_file("test_oneway_normal.png")
            raise

    def test_roundtrip_to_any_city_1(self):
        """
        往返-到达城市传空-查询结果检查
        :return:
        """
        try:
            self.is_roundtrip = True
            from_city = u"上海"
            from_date, from_date_check = self.get_search_date(offset=6)
            to_date, to_date_check = self.get_search_date(offset=6+3)
            self.set_search_type()
            self.set_from_city(from_city)
            self.set_from_date(from_date)
            self.set_to_date(to_date)
            self.submit()
            self.check_search_type()
            self.check_roundtrip_to_any_city(from_city, from_date_check, to_date_check)
        except Exception, e:
            print sys.exc_info()
            print e.message
            # self.browser.get_screenshot_as_file("test_roundtrip_to_any_city_1.png")
            raise


def run_one_case():
    """
    执行指定用例，可以采用nose的方式执行单个用例
    :return:
    """
    flight_suite = unittest.TestSuite()
    # flight_suite.addTest(TestFlightOneWay('test_oneway_normal'))
    flight_suite.addTest(TestFlightRoundTrip('test_roundtrip_normal'))
    flight_suite.addTest(TestFlightOneWay('test_oneway_to_any_city_1'))
    flight_suite.addTest(TestFlightRoundTrip('test_roundtrip_to_any_city_1'))
    # flight_suite.addTest(TestFlightOneWay('test_oneway_select_city_noraml'))
    flight_suite.addTest(TestFlightOneWay('test_oneway_select_city_any'))
    flight_suite.addTest(TestFlightRoundTrip('test_roundtrip_select_city_normal'))
    flight_suite.addTest(TestFlightRoundTrip('test_roundtrip_select_city_chg'))
    flight_suite.addTest(TestFlightRoundTrip('test_roundtrip_select_city_all'))
    flight_suite.addTest(TestFlightRoundTrip('test_roundtrip_sel_city_to_all'))
    # 手工测试
    # 如需单独测试某一个case，可以把其他addTest注释掉，然后执行
    test_runner = unittest.TextTestRunner()
    test_runner.run(flight_suite)


if __name__ == "__main__":
    run_one_case()
