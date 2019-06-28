## qunar_selenium project

### Entry Task

测试https://www.qunar.com  
首页-机票-国内机票搜索模块  
1、按照测试用例模版编写测试用例  
2、在本地搭建运行selenium并基于selenium编写UI自动化脚本，语言不限


### 运行说明
sh run.sh
* 脚本说明:  
1、虚拟环境生效：source /Users/jinlinxiao/py_env/selenium_env/bin/activate  
2、执行测试：cd /Users/jinlinxiao/gitCode/qunar_selenium_proj; nohup python qunar_test.py &  
3、deactivate 虚拟环境失效  

### unittest HTML执行报告
借助nose来输出HTML报告：  
##### 1、安装  
pip install nose  
pip install nose-html-reporting  

###### nose-html-reporting需要解决中文编码问题  
下载其源码之后，修改__init__.py文件  
1.1、在import sys后面增加以下两行代码：  
reload(sys)  
sys.setdefaultencoding("utf8")  
1.2、修改 _format_output 函数  
将 return o.decode('latin-1') 修改为 return o.decode('utf-8')  

##### 2、使用说明：
nosetests -v qunar_test.py --with-html --html-report=qunar_flight_ui_report.html  
带 --with-html --html-report=qunar_flight_ui_report.html 参数  

##### 3、nose使用说明：
执行单个用例：  
nosetests -v qunaer_test.py:TestFlightRoundTrip.test_roundtrip_normal  
执行一个Case Class下的所有用例（函数形式的用例也是这样执行）  
nosetests -v qunaer_test.py:TestFlightRoundTrip  
执行单个Case  
nosetests -v qunaer_test.py:TestFlightRoundTrip.test_roundtrip_normal  


### 用例列表
单程-直接输入城市，查找单程机票信息 ... 搜索报错  
单程-只选择出发城市，查询单程机票信息  
单程-选择出发城市和到达城市，查询单程机票信息 ... 搜索报错  
单程-到达城市传空-查询结果检查  
往返-输入出发城市和到达城市以及出发时间、返程时间，查询机票信息  
往返-从一个城市到所有地点，查询机票信息  
往返-在选择框选择出发城市和到达城市都为"所有城市"，选择出发时间、返程时间，查询机票信息  
往返-在选择框选择出发城市和到达城市以及出发时间、返程时间,调换出发和到达城市，查询机票信息  
往返-在选择框选择出发城市和到达城市以及出发时间、返程时间，查询机票信息  
往返-到达城市传空-查询结果检查   

### todo list 2019-02-26
##### todo list:
1、自动化用例各入参均放在case中，未进行参数化  
2、机票搜索结果检查需与db对应，目前仅在console中打印出来，未进行结果校验  
3、待实现测试场景：  
    单程输入或选择到达城市的场景，搜索结果展示不出来，通过跟踪Network显示，调用/api/lp_multifetch时传入的apiData[data]为空，返回"系统繁忙"错误  



