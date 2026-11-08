import allure


def allure_init(case):
    # 初始化allure报告
    allure.dynamic.feature(case.get("feature") or "未分类")
    allure.dynamic.story(case.get("story") or "默认")
    allure.dynamic.title(f"ID:{case.get('id')} -- {case.get('title') or case.get('feature', '')}")