import allure

from config.config import BASE_URL
from utils.log_utils import get_logger

logger = get_logger()


@allure.step("1.解析请求数据")
def analyse_case(case):
    method = case["method"]
    url = BASE_URL.rstrip("/") + case["path"]
    hearders = eval(case["headers"]) if isinstance(case["headers"], str) else None
    params = eval(case["params"]) if isinstance(case["params"], str) else None
    data = eval(case["data"]) if isinstance(case["data"], str) else None
    json = eval(case["json"]) if isinstance(case["json"], str) else None
    files = eval(case["files"]) if isinstance(case["files"], str) else None

    request_data = {
        "method": method,
        "url": url,
        "headers": hearders,
        "params": params,
        "data": data,
        "json": json,
        "files": files,
    }
    logger.debug(f"解析请求参数完成: url={url}, method={method}")
    # 需要加上返回值
    return request_data