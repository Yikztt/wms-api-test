# http响应断言
import allure
import jsonpath
from utils.send_request import send_jdbc_request
from utils.log_utils import get_logger

logger = get_logger()


@allure.step("3.HTTP响应断言")
def http_assert(case,res):
    if case["check"]:
        actual = jsonpath.jsonpath(res.json(), case["check"])[0]
        logger.info(f"HTTP断言: 表达式={case['check']}  实际值={actual}  期望值={case['expected']}")
        assert actual == case["expected"]
    else:
        logger.info(f"HTTP断言: 期望包含 '{case['expected']}'  实际响应包含={case['expected'] in res.text}")
        assert case["expected"] in res.text


def jdbc_assert(case):
    # 数据库断言
    if case["sql_check"] and case["sql_expected"]:
        with allure.step("3.JDBC响应断言"):
            logger.info(f"JDBC断言: sql={case['sql_check']}  期望值={case['sql_expected']}")
            assert send_jdbc_request(case["sql_check"]) == case["sql_expected"]
    else:
        logger.debug("JDBC断言: sql_check/sql_expected 为空，跳过数据库断言")