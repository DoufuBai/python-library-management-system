class  Book:
    def __init__(self,book_id,title,author,category,total,available):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.total = total
        self.available = available
    
    
    def __str__(self):
        return f"book_id:{self.book_id}  title: {self.title}    author:{self.author}    category:{self.category}  total :{self.total}   available:{self.available}"
    
    
    def to_dict(self):
        return {
            "book_id":self.book_id,
            "title":self.title,
            "author":self.author,
            "category":self.category,
            "total":self.total,
            "available":self.available
        }
    
class User:
    def __init__(self,user_id,name,borrowed=None):
        self.user_id = user_id
        self.name = name
        if borrowed is None:
            self.borrowed = []
        else:
            self.borrowed = borrowed
    def __str__(self):
        return f"user_id :{self.user_id}  name :{self.name}     borrowed:{self.borrowed}"
    def to_dict(self):
        return {
            "user_id" :self.user_id,
            "name":self.name,
            "borrowed":self.borrowed
        }
        