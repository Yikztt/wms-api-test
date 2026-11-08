import openpyxl


def read_excel(file_path, sheet_name):
    # 打开 excel 文件
    workbook = openpyxl.load_workbook(file_path)  # 参数传文件路径
    # 选择表
    worksheet = workbook[sheet_name]

    # 读数据操作，zip() 函数的作用可以把可迭代对象打包成一个个元组
    # 思路，因为 dict(zip(key, value)) 可以把读取到的数据变成字典类型，所以只需分别取出 key行，和value行即可
    # print(dict(zip([1, 2, 3, 4], ["a", "b", "c"])))
    data = []  # 空列表，用于组装字典
    keys = [cell.value for cell in worksheet[2]]  # 拿key行，也就是表的第二行，生成一个 key 的列表
    for row in worksheet.iter_rows(min_row=3, values_only=True):  # 从第三行开始拿，只返回值
        # print(row)  # 打印value列表
        # print(dict(zip(keys, row)))
        dict_data = dict(zip(keys, row))
        data.append(dict_data)
    # print(data) # 打印拿到的所有数据

    # 关闭 excel 文件
    workbook.close()
    return data