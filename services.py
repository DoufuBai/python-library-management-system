from data import BOOKS_FILE, USERS_FILE, DEFAULT_BOOKS, DEFAULT_USERS
from storage import save_json, load_json
from model import Book, User
from utils import log_action, count_total_by_category
class LibraryManager:
    def __init__(self):
        books_data = load_json(BOOKS_FILE,DEFAULT_BOOKS)
        users_data = load_json(USERS_FILE,DEFAULT_USERS)
        self.books = []
        for book_dict in books_data:
            book = Book(
                book_dict['book_id'],
                book_dict['title'],
                book_dict['author'],
                book_dict['category'],
                book_dict['total'],
                book_dict['available']
            )
            self.books.append(book)
        self.users = []
        for user_dict in users_data:
            user = User(
                user_dict['user_id'],
                user_dict['name'],
                user_dict['borrowed']
            )
            self.users.append(user)


    def save(self):
        books = []
        users = []
        for book in self.books:
            books.append(book.to_dict())
        for user in self.users:
            users.append(user.to_dict())
        save_json(BOOKS_FILE,books)
        save_json(USERS_FILE,users)


    def find_book(self, book_id):
        for book in self.books:
            if book_id == book.book_id:
                return book
        return None
    

    def find_user(self, user_id):
        for user  in self.users:
            if user_id == user.user_id:
                return user
        return None
    
    @log_action
    def borrow_book(self, user_id, book_id):
        user = self.find_user(user_id)
        if user is None:
            return "用户不存在"
        book = self.find_book(book_id)
        if book is None:
            return "图书不存在"
        if book.available <= 0:
            return  "图书已借完"
        if book_id in user.borrowed:
            return "不能重复借同一本书"
        book.available -= 1
        user.borrowed.append(book_id)
        self.save()
        return "借书成功"
    

    @log_action
    def return_book(self,user_id,book_id):
        user = self.find_user(user_id)
        if user is None:
            return "用户不存在"
        book = self.find_book(book_id)
        if book is None:
            return "图书不存在"
        if book_id not in user.borrowed:
            return "该用户没有借这本书"
        book.available +=1
        user.borrowed.remove(book_id)
        self.save()
        return "还书成功"
    
    def get_user_books(self, user_id):
        user = self.find_user(user_id)
        user_books = []
        if user is  None:
            return None
        else:
            for book_id in user.borrowed:
                book = self.find_book(book_id)
                if book  is not None:
                    user_books.append(book)
        return user_books
    
    def search_books(self, keyword):
        keyword = keyword.lower().strip()
        if keyword == "":
            return None
        result = []
        for book in self.books:
            if keyword in book.author.lower().strip() or keyword in book.title.lower().strip() or keyword in book.category.lower().strip():
                result .append(book)
        return result

    def get_hot_books(self):
        book_count = {}
        for user in self.users:
            for book_id in user.borrowed:
                book_count[book_id] = book_count.get(book_id,0)+1
        if len(book_count) == 0:
            return []
        max_count = max(book_count.values())
        hot_books = []
        for book_id ,count in book_count.items():
            if count ==max_count:
                hot_books.append(book_id)
        return hot_books
    

    def sort_books_by_available(self):
        return sorted(self.books,key =  lambda book : book.available,reverse= True)
    

    def count_category_total(self, category):
        return count_total_by_category(self.books,category)
    
    def add_book(self, book_id, title, author, category, total):
        book_id = book_id.strip()
        title = title.strip()
        author = author.strip()
        category = category.strip()
        result = self.find_book(book_id)
        if result:
                return "图书已存在"
        if total<=0:
            return "图书总数不合法"
        if book_id == "" or title == "" or author == "" or category == "" :
            return "字段不能为空"
        book =Book(book_id = book_id , title  = title , author = author ,category = category , total = total ,available = total)
        self.books.append(book)
        self.save()
        return "添加图书成功"
    
    
    def delete_book(self, book_id):
        result = self.find_book(book_id)
        if result is None:
            return "图书不存在"
        for user in self.users:
            if book_id  in user.borrowed:
                return "图书正在被借阅，不能删除"

        self.books.remove(result)
        self.save()
        return "删除图书成功"
    def get_low_stock_books(self, threshold):
        low_stock_books = []
        if threshold < 0:
            return None
        for book in self.books:
            if book.available <= threshold:
                low_stock_books.append(book)
        return low_stock_books
    

    def get_books_by_author(self, author):
        with_author = []
        author = author.lower().strip()
        if author =="":
            return None
        for book in self.books:
            if  book.author.lower().strip() == author:
                with_author.append(book)
        return with_author
        
        

        
    
    def reset_book_stock(self, book_id):
        book = self.find_book(book_id)
        if book is None:
            return "图书不存在"
        for user in self.users:
            if book_id in user.borrowed:
                return "图书正在被借阅，不能重置库存"
        book.available = book.total
        self.save()
        return "重置库存成功"