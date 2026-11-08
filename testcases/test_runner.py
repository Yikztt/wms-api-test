import time

import pytest
import requests
from jinja2 import Template
from utils.allure_utils import allure_init
from utils.analyse_case import analyse_case
from utils.asserts import http_assert, jdbc_assert
from utils.excel_utils import read_excel
from utils.extractor import json_extractor, jdbc_extractor
from utils.log_utils import get_logger
from config.config import EXCEL_FILE, SHEET_NAME

logger = get_logger()


class TestRunner:

    # 读测试用例文件中的全部数据，用属性保存即可
    data = read_excel(EXCEL_FILE, SHEET_NAME)
    # 提取后的数据需要初始化一个全局的属性来保存，可以使用 {} 空字典
    # ts 作为每次运行的唯一时间戳，供用例模板生成唯一编号（如客户/物料单号），可重复执行
    all = {"ts": int(time.time() * 1000)}

    @pytest.mark.parametrize("case", data)
    def test_case(self, case):
        #引用全局变量all
        all = self.all
        # 根据 all 的值，渲染 case
        case = eval(Template(str(case)).render(all))

        case_id = case.get("id", "?")
        case_title = case.get("title") or case.get("feature", "")
        logger.info("=" * 60)
        logger.info(f"开始执行用例  ID:{case_id}  {case_title}")
        logger.info(f"所属模块: feature={case.get('feature')}  story={case.get('story')}")

        try:
            # 初始化 allure 报告
            allure_init(case)

            # 核心步骤1：解析请求数据
            request_data = analyse_case(case)
            logger.info(f"发送请求 -> {request_data.get('method')} {request_data.get('url')}")
            logger.debug(f"请求详情: {request_data}")

            # 核心步骤2：发起请求，得到响应结果
            res = requests.request(**request_data)
            logger.info(f"响应状态码: {res.status_code}")
            logger.debug(f"响应内容: {res.text}")

            # 核心步骤3：处理断言
            # http响应断言
            http_assert(case, res)

            # 数据库断言（无数据库时 sql 字段为空，自动跳过）
            jdbc_assert(case)

            # 核心步骤4：提取
            #json提取
            json_extractor(case, all, res)

            # 数据库提取
            jdbc_extractor(case, all)

            logger.info(f"用例执行结果  ID:{case_id}  {case_title}  ==> PASS")
        except Exception as e:
            logger.error(f"用例执行失败  ID:{case_id}  {case_title}  ==> FAIL: {e}", exc_info=True)
            raise
