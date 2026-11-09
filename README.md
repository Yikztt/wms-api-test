# wms-api-test

基于 **Excel 数据驱动 + Pytest + Allure** 的 WMS 仓库管理系统接口自动化测试框架，支持参数依赖传递、可重复执行与多维度断言。

| 项目 | 说明 |
| --- | --- |
| 被测项目 | WMS 仓库管理系统（RuoYi-Vue + Spring Boot 后端） |
| 测试地址 | `http://60.204.225.104:9632`（配置文件：`config/config.py`） |
| 技术栈 | Python 3.x / Pytest / Requests / openpyxl / jsonpath / Allure / PyMySQL |
| 执行日期 | 2026-11-08 |

---

## 目录

| 目录 / 文件 | 内容 |
| --- | --- |
| `config/` | 环境配置：被测服务地址 `BASE_URL`、Excel 文件与 Sheet 名、数据库连接信息 |
| `data/` | 测试用例数据源 `测试用例.xlsx`（用例的唯一维护入口） |
| `testcases/` | 用例执行引擎 `test_runner.py`，负责参数化、请求、断言、提取的调度 |
| `utils/` | 框架能力封装：Excel 读取、请求解析、断言、提取、日志、Allure |
| `run.py` | 一键执行入口：跑 Pytest 并自动生成 Allure HTML 报告 |
| `pytest.ini` | Pytest 配置（日志统一交由 `utils/log_utils.py` 管理） |
| `requirements.txt` | 项目依赖 |
| `log/` | 运行日志 `test.log`（运行时自动生成，已 gitignore） |
| `report/` | Allure 中间结果与 HTML 报告（运行时自动生成，已 gitignore） |

### utils 模块职责

| 文件 | 职责 |
| --- | --- |
| `excel_utils.py` | 读取 Excel：第 2 行作表头 key，第 3 行起为用例数据，转成 `list[dict]` |
| `analyse_case.py` | 解析用例字段并拼装 `requests.request(**kwargs)` 所需参数 |
| `send_request.py` | 发送 HTTP 请求 / 执行 JDBC 查询（PyMySQL） |
| `asserts.py` | HTTP 响应断言（JsonPath 或包含式）+ 数据库断言 |
| `extractor.py` | JSON / 数据库字段提取，回填全局变量供后续用例引用 |
| `log_utils.py` | 统一日志：控制台（WARNING 以上）+ `./log/test.log`（DEBUG 全量，UTF-8） |
| `allure_utils.py` | 动态写入 Allure 的 feature / story / title，报告按模块分层展示 |

---

## 框架设计

用例与代码完全分离：**所有测试数据只写在 Excel 里**，新增接口用例无需改动 Python 代码。

```
data/测试用例.xlsx
        │  openpyxl 读取（表头映射为 dict）
        ▼
pytest.mark.parametrize  →  每条用例生成一个独立测试项
        │
        ▼
Jinja2 渲染 {{ts}}  ← 唯一时间戳，保证用例可重复执行
        │
        ├─ 1. 解析请求：method / path / headers / params / data / json / files
        ├─ 2. 发送请求：requests.request(**request_data)
        ├─ 3. 断言校验：HTTP 响应断言 + 数据库断言
        ├─ 4. 字段提取：JsonPath / SQL 提取结果写入全局变量
        └─ 5. 结果归档：Allure 报告 + 日志
```

### 用例字段说明

| 字段 | 含义 |
| --- | --- |
| `id` / `feature` / `story` / `title` | 用例编号、所属模块、所属场景、用例标题 |
| `method` / `path` | 请求方式与接口路径（自动拼接 `BASE_URL`） |
| `headers` / `params` / `data` / `json` / `files` | 请求头、URL 参数、表单、JSON 体、文件参数 |
| `check` / `expected` | JsonPath 校验表达式与预期值；`check` 为空时退化为「响应文本包含 `expected`」 |
| `sql_check` / `sql_expected` | 数据库断言 SQL 与预期值（为空则自动跳过） |
| `jsonExData` / `sqlExData` | 字段提取映射，如 `{"token": "$..token"}`，提取结果供后续用例以 `{{token}}` 引用 |

### 关键设计点

1. **接口依赖链**：登录提取 `token` → 新增提取业务主键 `id` → 查询/修改/删除引用 `{{id}}`，形成完整业务闭环，而非孤立的单接口调用。
2. **可重复执行**：每次运行生成一个毫秒级时间戳 `ts`，业务单号统一使用 `WH{{ts}}`、`IT{{ts}}` 等模板，反复执行不会因唯一键冲突失败。
3. **断言分层**：既校验响应体（`code` / `msg` / `content`），也可校验数据库落库结果，避免只验「接口通了」。
4. **失败可定位**：每条用例打印 ID、标题、模块、请求详情、响应状态码与响应体，异常处输出完整堆栈。
5. **报告可读**：Allure 按 `feature → story → 用例` 三层展开，步骤划分为「解析请求 / 发送请求 / 断言 / 提取」。

> 注意：用例存在顺序依赖（新增 → 查询 → 修改 → 删除），按 Excel 行序执行，不支持随机乱序或并发执行。

---

## 测试范围

覆盖用户认证（验证码、登录）、仓库 / 库区 / 货架、物料、客户、供应商、承运商、基础数据、库存、出入库、账务等模块，接口操作包括列表查询、新增、条件查询、修改、删除与导出。

其中仓库、库区、货架、物料、客户、供应商、承运商七个核心主数据模块均打通了「新增 → 查询 → 修改 → 删除」全链路。

---

## 主要交付物

- 测试用例数据源：`data/测试用例.xlsx`（含请求参数、校验表达式、预期结果、提取规则）
- 接口自动化工程：`testcases/` + `utils/`（Excel 驱动执行引擎与通用能力封装）
- 执行日志：`log/test.log`（每条用例的请求、响应、断言与提取明细）
- Allure 测试报告：`report/html_report/index.html`
- Allure 中间结果：`report/json_report/`

---

## 运行自动化

### 1. 环境准备

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
# 模板渲染与数据库断言额外依赖
pip install jinja2 pymysql
```

需要本地已安装 **Allure 命令行工具**（用于生成 HTML 报告），校验方式：

```bash
allure --version
```

若被测 WMS 服务地址与本框架不一致，请先修改 `config/config.py` 中的 `BASE_URL`；若要启用数据库断言，同时补全 `JDBC_*` 配置（默认值下 `sql_check` 为空，断言会自动跳过）。

### 2. 执行

一键执行（跑用例 + 生成 HTML 报告）：

```bash
python run.py
```

等价的分步命令：

```bash
pytest testcases/test_runner.py -vs \
  --alluredir=./report/json_report --clean-alluredir

allure generate ./report/json_report -o ./report/html_report --clean
allure open ./report/html_report
```

### 3. 查看结果

报告打开 `report/html_report/index.html`（或 `allure open ./report/html_report`）；需要看单条用例的失败现场时，查 `log/test.log` 中对应 `ID` 的「请求详情」与「响应内容」两行，再对照 Allure 报告中的断言步骤。

---

## 后续规划

- 接入 `pytest-xdist` 前先做用例解耦（去掉顺序依赖），再考虑并发执行
- 引入数据清理机制，删除自动化生成的测试数据，减少环境脏数据
- 将「是否执行」列（`is_true`）接入用例筛选，支持按模块 / 优先级选择执行集
- 接入 CI（Jenkins / GitHub Actions），每次提交自动回归并归档 Allure 报告
