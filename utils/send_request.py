import allure
import pymysql
import requests

from config.config import *


@allure.step("2.发送HTTP请求")
def send_http_request(**request_data):
    res = requests.request(**request_data)
    return res

def send_jdbc_request(sql, index=0):
    conn = pymysql.Connect(
        host=JDBC_HOST,
        port=JDBC_PORT,
        database=JDBC_DATABASE,
        user=JDBC_USER,
        password=JDBC_PASSWORD,
        charset="utf8"
    )
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result[index]
