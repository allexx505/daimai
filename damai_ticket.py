# coding: utf-8
import sys
from json import loads
from time import sleep, time
from pickle import dump, load
from os.path import exists
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Concert(object):
    def __init__(self, session, price, real_name, nick_name, ticket_num, damai_url, target_url,driver_path):
        self.session = session  # 场次序号优先级
        self.price = price  # 票价序号优先级
        self.real_name = real_name  # 实名者序号
        self.status = 0  # 状态标记
        self.time_start = 0  # 开始时间
        self.time_end = 0  # 结束时间
        self.num = 0  # 尝试次数
        self.ticket_num = ticket_num  # 购买票数
        self.nick_name = nick_name  # 用户昵称
        self.damai_url = damai_url  # 大麦网官网网址
        self.target_url = target_url  # 目标购票网址
        self.driver_path = driver_path  # 浏览器驱动地址
        self.driver = None
        self.chrome_option = None

    def isClassPresent(self, item, name, ret=False):
        try:
            result = item.find_element_by_class_name(name)
            if ret:
                return result
            else:
                return True
        except:
            return False

    # 获取账号的cookie信息
    def get_cookie(self):
        self.driver.get(self.damai_url)
        print(u"###请点击登录###")
        self.driver.find_element_by_class_name('login-user').click()
        while self.driver.title.find('大麦网-全球演出赛事官方购票平台') != -1:  # 等待网页加载完成
            sleep(1)
        print(u"###请扫码登录###")
        while self.driver.title == '大麦登录':  # 等待扫码完成
            sleep(1)
        dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
        print(u"###Cookie保存成功###")

    def set_cookie(self):
        try:
            cookies = load(open("cookies.pkl", "rb"))  # 载入cookie
            for cookie in cookies:
                cookie_dict = {
                    'domain': '.damai.cn',  # 必须要有的, 否则就是假登录
                    'name': cookie.get('name'),
                    'value': cookie.get('value')
                }
                self.driver.add_cookie(cookie_dict)
            print(u'###载入Cookie###')
        except Exception as e:
            print(e)

    def login(self):
        print(u'###开始登录###')
        self.driver.get(self.target_url)
        WebDriverWait(self.driver, 10, 0.1).until(EC.title_contains('商品详情'))
        print(u'###登录成功###')
        self.set_cookie()

    def enter_concert(self):
        print(u'###打开浏览器，进入大麦网###')
        if not exists('cookies.pkl'):   # 如果不存在cookie.pkl,就获取一下
            self.driver = webdriver.Chrome(executable_path=self.driver_path)
            self.get_cookie()
            print(u'###成功获取Cookie，重启浏览器###')
            self.driver.quit()

        self.chrome_option = webdriver.ChromeOptions()
        self.chrome_option.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.chrome_option.add_argument('--disable-blink-features=AutomationControlled')
        self.chrome_option.add_experimental_option("mobileEmulation", {"deviceName": "iPhone 6"})
        self.chrome_option.add_argument("--auto-open-devtools-for-tabs")

        # 更换等待策略为不等待浏览器加载完全就进行下一步操作
        capa = DesiredCapabilities.CHROME
        capa["pageLoadStrategy"] = "none"
        self.driver = webdriver.Chrome(executable_path=rf'D://python_demo//damai-ticker//chromedriver.exe',options=self.chrome_option)
        # 登录到具体抢购页面
        self.login()
        self.driver.refresh()
        try:
            # 等待nickname出现
            # locator = (By.XPATH, "/html/body/div[1]/div/div[3]/div[1]/a[2]/div")
            # WebDriverWait(self.driver, 5, 0.3).until(EC.text_to_be_present_in_element(locator, self.nick_name))
            self.status = 1
            print(u"###登录成功###")
            self.time_start = time()
        except:
            self.status = 0
            self.driver.quit()
            raise Exception(u"***错误：登录失败,请删除cookie后重试***")

    # 实现购买函数
    def choose_ticket(self):
        print(u"###进入抢票界面###")
        
        while self.driver.title.find('确认订单') == -1:  # 如果跳转到了确认界面就算这步成功了，否则继续执行此步
            self.num += 1  #尝试次数加1

            if self.driver.current_url.find("buy.damai.cn") != -1:
                break

            # 确认页面刷新成功
            try:
                box = WebDriverWait(self.driver, 1, 0.1).until(EC.presence_of_element_located((By.CLASS_NAME, 'detail-tour')))
            except:
                raise Exception(u"***Error: 页面刷新出错***")

                 # 关闭实名
        
            # 进行选座购买按钮点击
            print("等待主页面刷新")
            import time
            # todo 需要尽量调小时间
            if self.num == 1:
                #第一次等待时间长一点
                time.sleep(3)
            else:
                time.sleep(0.1)
            print("点击购买按钮")
            self.driver.find_element(By.CLASS_NAME, 'buy__button').click()

            # 进行日期选择操作
            print("选择具体日子")
            date0618 = self.driver.find_elements(By.CLASS_NAME, "item-text.item-text-normal")
            print(f"date_text:{len(date0618)}")
            # day_item_list = self.driver.find_elements(By.CLASS_NAME, 'item-content.item-text.item-text-normal')
            # print(f"day_item_list_len:{len(sku_pop_wrapper)}")
            sys.exit(0)
            for day_item in day_item_list:
                day_str = str(day_item.get_attribute('innerText'))
                print(f"day_str:{day_str}")
                sys.exit(0)
                if '2023-06-18' in day_str:
                    print(f"选中该日期{day_str}，进行点击")
                    day_item.click()
                    break
            element_list = self.driver.find_elements_by_class_name('item-text.item-text-normal')
            print(len(element_list))
            for element in element_list:
                data_value = str(element.get_attribute('innerText'))
                print(f"data_value:{data_value}")
                if data_value.count(self.rob_price) > 0:
                    print("选择票档")
                    element.click()

            '''
            接下来的逻辑都需要重写
            1. 选择具体的场次和票价
            2. 如果显示无票，则直接raise error，并重新刷新页面
            3. 如果发现是有票，那么直接遍历所有票档
            4. 如果显示缺货登记，则直接raise error，并重新刷新页面
            5. 
            '''
            #region 选票，选座逻辑
            try:
                buybutton = box.find_element_by_class_name('buy__button') # 寻找立即购买标签
                buybutton_text = buybutton.text
            except:
                raise Exception(u"***Error: buybutton 位置找不到***")

            if buybutton_text == "即将开抢" or buybutton_text == "即将开售":
                self.status = 2
                raise Exception(u"---尚未开售，刷新等待---")

            try:
                selects = box.find_elements_by_class_name('perform__order__select') # 场次和票档进行定位
                for item in selects:
                    if item.find_element_by_class_name('select_left').text == '场次':
                        session = item
                        # print('\t场次定位成功')
                    elif item.find_element_by_class_name('select_left').text == '票档':
                        price = item
                        # print('\t票档定位成功')

                session_list = session.find_elements_by_class_name('select_right_list_item')#选定场次
                # print('可选场次数量为：{}'.format(len(session_list)))
                for i in self.session:  # 根据优先级选择一个可行场次
                    j = session_list[i-1]
                    k = self.isClassPresent(j, 'presell', True)
                    if k: # 如果找到了带presell的类
                        if k.text == '无票':
                            continue
                        elif k.text == '预售':
                            j.click()
                            break
                    else:
                        j.click()# 选定好场次点击按钮确定
                        break

                price_list = price.find_elements_by_class_name('select_right_list_item')#选定票档
                # print('可选票档数量为：{}'.format(len(price_list)))
                for i in self.price:
                    j = price_list[i-1]
                    k = self.isClassPresent(j, 'notticket')
                    if k:  # 存在notticket代表存在缺货登记，跳过
                        continue
                    else:
                        j.click()#选定好票档点击确定
                        break
            except:
                raise Exception(u"***Error: 选择场次or票档不成功***")
            # region 选票，选座逻辑

            '''
            1. 修改数量，变成2
            2. 下一步，直接点击 “确定“按钮
            3. 此时直接跳转到订单界面
            4. 选择实名观演人，1和2
            5. 直接提交订单，并提示用户到app上进行支付
            '''

            try:
                ticket_num_up = box.find_element_by_class_name('cafe-c-input-number-handler-up')
            except:
                if buybutton_text == "选座购买":  # 选座购买没有增减票数键
                    buybutton.click()
                    self.status = 5
                    print(u"###请自行选择位置和票价###")
                    break
                elif buybutton_text == "提交缺货登记":
                    raise Exception(u'###票已被抢完，持续捡漏中...或请关闭程序并手动提交缺货登记###')
                else:
                    raise Exception(u"***Error: ticket_num_up 位置找不到***")

            if buybutton_text == "立即预订":
                for i in range(self.ticket_num-1):  # 设置增加票数
                    ticket_num_up.click()
                buybutton.click()
                self.status = 3

            elif buybutton_text == "立即购买":
                for i in range(self.ticket_num-1):  # 设置增加票数
                    ticket_num_up.click()
                buybutton.click()
                self.status = 4

    def check_order(self):
        if self.status in [3, 4, 5]:
            if self.real_name is not None:
                print(u"###等待--确认订单--页面出现，可自行刷新，若长期不跳转可选择-- CRTL+C --重新抢票###")
                try:
                    tb = WebDriverWait(self.driver, 1, 0.1).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[2]/div')))
                except:
                    raise Exception(u"***Error：实名信息选择框没有显示***")

                print(u'###开始确认订单###')
                print(u'###选择购票人信息,可手动帮助点击###')
                init_sleeptime = 0.0
                Labels = tb.find_elements_by_tag_name('label')

                # 防止点击过快导致没有选择多个人
                while True:
                    init_sleeptime += 0.1
                    true_num = 0
                    for num_people in self.real_name:
                        tag_input = Labels[num_people-1].find_element_by_tag_name('input')
                        if tag_input.get_attribute('aria-checked') == 'false':
                            sleep(init_sleeptime)
                            tag_input.click()
                        else:
                            true_num += 1
                    if true_num == len(self.real_name):
                        break
                print("本次抢票时间：", time()-self.time_start)
                self.driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[9]/button').click() # 同意以上协议并提交订单

            else:
                self.driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[8]/button').click()

            # 判断title是不是支付宝
            print(u"###等待跳转到--付款界面--，可自行刷新，若长期不跳转可选择-- CRTL+C --重新抢票###")
            try:
                WebDriverWait(self.driver, 3600, 0.1).until(EC.title_contains('支付宝'))
            except:
                raise Exception(u'***Error: 长期跳转不到付款界面***')

            self.status = 6
            print(u'###成功提交订单,请手动支付###')
            self.time_end = time()


if __name__ == '__main__':
    with open('./config.json', 'r', encoding='utf-8-sig') as f:
        config = loads(f.read())
        # params: 场次优先级，票价优先级，实名者序号, 用户昵称， 购买票数， 官网网址， 目标网址, 浏览器驱动地址
    con = Concert(config['sess'], config['price'], config['real_name'], config['nick_name'], config['ticket_num'],
                  config['damai_url'], config['target_url'], config['driver_path'])
    con.enter_concert()
    # try:
    #     with open('./config.json', 'r', encoding='utf-8-sig') as f:
    #         config = loads(f.read())
    #         # params: 场次优先级，票价优先级，实名者序号, 用户昵称， 购买票数， 官网网址， 目标网址, 浏览器驱动地址
    #     con = Concert(config['sess'], config['price'], config['real_name'], config['nick_name'], config['ticket_num'], config['damai_url'], config['target_url'], config['driver_path'])
    #     con.enter_concert() #进入到具体抢购页面
    # except Exception as e:
    #     print(e)
    #     exit(1)
    while True:
        try:
            con.choose_ticket()
            con.check_order()
        except Exception as e:
            con.driver.get(con.target_url)
            print(e)
            continue

        if con.status == 6:
            print(u"###经过%d轮奋斗，共耗时%.1f秒，抢票成功！请确认订单信息###" % (con.num, round(con.time_end-con.time_start, 3)))
            break
    # 五月天杭州场次 721069251830