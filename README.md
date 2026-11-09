wms-api-test
WMS 仓库管理系统接口自动化测试框架：Excel 数据驱动 + Pytest + Allure。
项目
说明
被测项目
WMS 仓库管理系统
测试地址
http://60.204.225.104:9632
技术栈
Python / Pytest / Requests / openpyxl / jsonpath / Allure
目录结构
config/       环境配置（BASE_URL、数据库连接）
data/         测试用例.xlsx
testcases/    用例执行引擎
utils/        Excel 读取、请求解析、断言、提取、日志、Allure
run.py        一键执行
log/          运行日志（自动生成）
report/       Allure 报告（自动生成）
运行
pip install -r requirements.txt
pip install jinja2 pymysql   # 模板渲染与数据库断言额外依赖
python run.py
- Allure CLI 需单独安装，用 allure --version 校验
- 被测地址在 config/config.py 的 BASE_URL 中修改
说明
- 所有用例写在 data/测试用例.xlsx，新增用例无需改动代码
- 用例字段包含请求参数、JsonPath 断言、预期结果与字段提取；登录 token、业务主键通过 {{}} 在用例间传递
- 用例按 Excel 行序执行，存在顺序依赖（新增 → 查询 → 修改 → 删除），不支持并发
报告
Allure 报告：report/html_report/index.html　日志：log/test.logions），每次提交自动回归并归档 Allure 报告
