#!/bin/sh

source /Users/jinlinxiao/py_env/selenium_env/bin/activate

cd /Users/jinlinxiao/gitCode/qunar_selenium_proj; nosetests -v qunar_test.py --with-html --html-report=qunar_flight_ui_report.html

deactivate