from model import Book
def test_book_to_dict()->None:
    expected_dict = {
        "book_id":"B1027",
        "title":"我的书籍",
        "author": "白豆腐",
        "category":"白豆腐书籍分类",
        "total":100,
        "available":100
    }
    book = Book(book_id="B1027",title="我的书籍",author= "白豆腐",category="白豆腐书籍分类",total= 100,available=100)
    result = book.to_dict()
    assert isinstance(result,dict) is True
    assert result == expected_dict