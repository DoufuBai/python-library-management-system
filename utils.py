def log_action(func):
    def wrapper(*args,**kwargs):
        print(f"开始执行：{func.__name__}")
        try:
            result = func(*args,**kwargs)
            print(f"执行完成：{func.__name__}")
            return result
        except Exception as e:
            print(f"执行出错：{e}")
            return None
    return wrapper

def count_total_by_category(books, category, index=0):
    if index >=len(books):
        return 0
    book = books[index]
    if book.category == category:
        return book.total + count_total_by_category(books, category, index+1)
    else:
        return count_total_by_category(books, category, index+1)
    
    