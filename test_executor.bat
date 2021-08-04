@echo off
del /f /q report\temp_data
REM pytest scripts\main.py --soft-asserts --alluredir=report\temp_data --html=report\pytest_html_report\report.html --self-contained-html
REM allure-cli\allure-2.10.0\bin\allure generate report\temp_data -c -o report\allure_html_report
del /f /q report\temp_data
pytest scripts\main.py
echo "============= Execution Completed ================"