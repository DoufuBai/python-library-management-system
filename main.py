from services import LibraryManager
def show_menu():
    print("""
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
""")
    
def print_books(books):
    if books is None or len(books) ==0 :
        print("没有找到图书")
    else:
        for book in books:
            print(book)


def main():
    manager = LibraryManager()
    while True:
        show_menu()
        choice = input("请输入选项").strip()
        try:
            choice = int(choice)
        except ValueError:
            print("非法字符，请输入数字")
            continue
        if choice ==1:
            print_books(manager.books)
        elif choice ==0:
            print("成功退出系统！")
            break
        elif choice ==2:
            keyword = input("请输入搜索关键字：").strip()
            if keyword == "":
                print("关键字不能为空")
            else:
                result = manager.search_books(keyword)
                print_books(result)
        elif choice == 3:
            book_id = input("请输入书籍id").strip()
            user_id = input("请输入用户id").strip()
            result = manager.borrow_book(book_id= book_id,user_id= user_id)
            print(result)
        elif choice ==4:
            book_id = input("请输入书籍id").strip()
            user_id = input("请输入用户id").strip()
            result = manager.return_book(book_id= book_id,user_id= user_id)
            print(result)
        elif choice == 5:
            user_id = input("请输入用户id").strip()
            result = manager.get_user_books(user_id=user_id)
            if result is None:
                print("用户不存在")
            elif len(result)==0:
                print("该用户没有借书")
            else:
                print_books(result)
        elif choice ==6:
            result = manager.get_hot_books()
            if result ==[]:
                print("没有热门书籍")
            else:
                print(f"热门书籍id:{result}")
        elif choice == 7 :
            result = manager.sort_books_by_available()
            print_books(result)
        elif choice == 8:
            category = input("请输入分类").strip()
            result = manager.count_category_total(category)
            print(f"当前分类下的书籍总数是：{result}")
        elif choice == 9 :
            book_id_add = input("请输入图书id").strip()
            title = input("请输入书籍名字").strip()
            author = input("请输入作者名字").strip()
            category_add = input("请输入书籍分类").strip()
            while True:
                total = input("请输入书籍总册")
                try:
                    total = int(total)
                except ValueError:
                    print("总册数必须是数字,重新输入图书总册")
                    continue
                result = manager.add_book(book_id= book_id_add , title= title, author= author,category= category_add,total= total)
                break
            print(result)
        elif choice == 10:
            book_id_delete = input("请输入想要删除的图书id").strip()
            result = manager.delete_book(book_id= book_id_delete)
            print(result)
        elif choice == 11:
                threshold = input("请输入库存阈值")
                try :
                    threshold = int(threshold)
                    result11 = manager.get_low_stock_books(threshold= threshold)
                    if result11 is None:
                        print("库存阈值非法")
                    else:
                        print_books(result11)
                except ValueError:
                    print("库存阈值必须是数字")
        elif choice ==12:
            author_12 = input("请输入作者名字")
            result12 = manager.get_books_by_author(author= author_12)
            if result12 is None:
                print("请输入作者名字，作者名字不能为空")
            else:
                print_books(result12)
        elif choice == 13 :
            book_id13 = input("请输入图书id").strip()
            result  = manager.reset_book_stock(book_id= book_id13)
            print(result)
        else:
            print("输入错误，请重新选择")
if __name__ == "__main__":
    main()
        