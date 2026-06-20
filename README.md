# Python 图书馆管理系统

一个使用 Python 面向对象编程开发的命令行图书馆管理系统。

项目通过多个模块组织数据模型、文件读写、业务逻辑和程序入口，并使用 JSON 文件持久化保存图书与用户数据。它是一个用于练习 Python 基础语法和工程化组织方式的综合项目。

## 功能介绍

- 查看全部图书
- 按书名、作者或分类搜索图书
- 用户借书与还书
- 查看指定用户已借图书
- 查看当前热门图书
- 按可用库存降序排列图书
- 按分类递归统计图书总册数
- 添加和删除图书
- 按库存阈值查询低库存图书
- 按作者查询图书
- 重置未被借阅图书的库存
- 自动保存图书和用户数据
- 文件不存在或 JSON 损坏时恢复默认数据
- 使用装饰器记录借书、还书函数的执行日志

## 技术要点

- 类与对象
- 实例属性和实例方法
- 魔法方法 `__init__`、`__str__`
- 对象与字典之间的转换
- 列表和字典的组合使用
- JSON 文件读写
- 异常处理
- 模块化设计
- 装饰器
- 递归函数
- `lambda` 排序
- 命令行交互

## 项目结构

```text
library_project/
|-- main.py       # 命令行菜单和程序入口
|-- services.py   # LibraryManager 和核心业务逻辑
|-- model.py      # Book、User 数据模型
|-- storage.py    # JSON 文件加载与保存
|-- utils.py      # 日志装饰器和递归统计函数
|-- data.py       # 默认数据和文件名配置
|-- books.json    # 当前图书数据
|-- users.json    # 当前用户数据
`-- README.md     # 项目说明
```

## 模块职责

### `model.py`

定义项目的数据模型：

- `Book`：保存图书 ID、书名、作者、分类、总册数和可用库存。
- `User`：保存用户 ID、姓名和已借图书 ID。
- `to_dict()`：把对象转换成可写入 JSON 的字典。
- `__str__()`：控制对象被打印时的显示内容。

### `storage.py`

负责 JSON 文件持久化：

- `load_json(filename, default_data)`：读取 JSON 数据。
- `save_json(filename, data)`：保存 JSON 数据。
- 文件不存在或内容损坏时，写入并返回默认数据。

### `services.py`

定义 `LibraryManager`，负责加载对象、保存数据和处理图书馆业务。

主要方法包括：

```text
find_book()                 查询图书
find_user()                 查询用户
borrow_book()               借书
return_book()               还书
get_user_books()            查看用户已借图书
search_books()              关键字搜索
get_hot_books()             查看热门图书
sort_books_by_available()   按库存排序
count_category_total()      按分类统计总册数
add_book()                  添加图书
delete_book()               删除图书
get_low_stock_books()       查看低库存图书
get_books_by_author()       按作者查询
reset_book_stock()          重置图书库存
```

### `utils.py`

- `log_action`：装饰借书和还书方法，输出函数开始、完成或异常日志。
- `count_total_by_category`：通过递归统计指定分类的图书总册数。

### `main.py`

负责展示菜单、接收用户输入、调用 `LibraryManager`，并把结果输出到终端。

## 数据流转

JSON 文件只能直接保存字典、列表、字符串、数字和布尔值等基础数据，因此程序启动和保存时需要进行转换：

```text
程序启动：JSON 文件 -> 字典列表 -> Book / User 对象列表
程序保存：对象列表 -> 字典列表 -> JSON 文件
```

项目遵循的核心原则是：

```text
程序内部使用对象处理业务，JSON 文件使用字典保存数据。
```

## 运行环境

- Python 3.8 或更高版本
- 不需要安装第三方依赖

## 运行方法

进入项目目录：

```bash
cd library_project
```

启动程序：

```bash
python main.py
```

启动后会显示以下菜单：

```text
===== 图书馆管理系统 =====
1. 查看所有图书
2. 搜索图书
3. 借书
4. 还书
5. 查看用户已借图书
6. 查看热门图书
7. 按库存排序
8. 按分类统计图书总册数
9. 添加图书
10. 删除图书
11. 查看低库存图书
12. 按作者查询图书
13. 重置图书库存
0. 退出
```

按照提示输入选项、用户 ID 或图书 ID 即可操作。

默认用户：

```text
U001  小明
U002  小红
```

默认图书 ID：

```text
B001  Python入门
B002  数据结构
B003  算法图解
```

## 数据保存说明

借书、还书、添加图书、删除图书和重置库存成功后，程序会自动更新 `books.json` 与 `users.json`。

直接修改 JSON 文件时需要保持原有字段结构，否则程序可能无法把字典转换成对象。

## 后续计划

- 增加用户管理功能
- 增加借阅历史记录
- 使用 `pytest` 编写自动化测试
- 使用 SQLite 替代 JSON 文件
- 使用 FastAPI 提供 Web API
- 增加图形界面或 Web 前端
