import allure
import jsonpath

from utils.send_request import send_jdbc_request
from utils.log_utils import get_logger

logger = get_logger()


def json_extractor(case,all,res):
    if case["jsonExData"]:
        with allure.step("4.JSON提取"):
            # 首先要把 jsonExData 的 key，value 拆开
            for key, value in eval(case["jsonExData"]).items():
                result = jsonpath.jsonpath(res.json(), value)
                if not result:
                    logger.error(f"JSON提取失败: 表达式 {value} 未匹配到数据，跳过 {key}")
                    continue
                extract_val = result[0]
                all[key] = extract_val
                logger.info(f"JSON提取: {key} = {extract_val}  (表达式 {value})")
    else:
        logger.debug("JSON提取: jsonExData 为空，跳过")

def jdbc_extractor(case,all):
    if case["sqlExData"]:
        with allure.step("4.JDBC提取"):
            for key, value in eval(case["sqlExData"]).items():
                extract_val = send_jdbc_request(value)
                all[key] = extract_val
                logger.info(f"JDBC提取: {key} = {extract_val}  (sql {value})")
    else:
        logger.debug("JDBC提取: sqlExData 为空，跳过")
