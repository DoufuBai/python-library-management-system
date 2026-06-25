from model import Book,User
from services import LibraryManager
import pytest


def patch_save(manager:LibraryManager,monkeypatch)->list[str]:
    save_calls = []
    def fake_save()->None:
        save_calls.append("called")
    monkeypatch.setattr(manager,"save",fake_save)
    return save_calls


@pytest.fixture
def manager_with_book()->LibraryManager:
    manager = LibraryManager()
    book = Book(book_id= "B888",title= "飘",author="waiguo ren ", category= "feeling",total=100,available=100)
    manager.books = [book]
    return manager


@pytest.fixture
def manager_with_book_and_user()->LibraryManager:
    manager = LibraryManager()
    book = Book(book_id= "B888",author="xiaomingdetongshi ",title="钢铁是怎样练成的",category="insprit",total=100,available=100)
    user = User(user_id="U001",name="xiaoming de mingzi ")
    manager.books = [book]
    manager.users=[user]
    return manager


def test_find_book_found(manager_with_book:LibraryManager):
    result = manager_with_book.find_book("B888")
    assert isinstance(result,Book)
    assert result is manager_with_book.books[0]


def test_find_book_not_found(manager_with_book:LibraryManager):
    result = manager_with_book.find_book("B9956325")
    assert result is None


def test_search_book(manager_with_book:LibraryManager):
    result = manager_with_book.search_books("            WAIGUO REN          ")
    book_result = result[0]
    assert book_result is manager_with_book.books[0]


@pytest.mark.parametrize(
    "keyword, expected",
    [
        ("   ", None),
        ("woandiwajndajdna", []),
    ],
)


def test_search_books_boundary(manager_with_book,keyword,expected):
    result = manager_with_book.search_books(keyword=keyword)
    assert result == expected


def test_add_book_success(manager_with_book: LibraryManager, monkeypatch) -> None:
    save_calls = patch_save(manager= manager_with_book,monkeypatch=monkeypatch)
    result = manager_with_book.add_book(book_id="B805",title="xiaobaideshu ",author= "zhou henghui ",category= "xiaofenlei",total=95)
    assert len(manager_with_book.books)==2
    added_book = manager_with_book.find_book("B805")
    assert added_book is not None
    assert added_book.available == 95
    assert len(save_calls)==1
    assert result =="添加图书成功"


def test_add_book_duplicate_id(manager_with_book: LibraryManager, monkeypatch) -> None:
    save_calls =patch_save(manager=manager_with_book,monkeypatch=monkeypatch)
    result = manager_with_book.add_book(book_id= "B888",title="xiaobaideshu ",author= "zhou henghui ",category= "xiaofenlei",total=95)
    assert len(manager_with_book.books)==1
    assert result =="图书已存在"
    assert len(save_calls)==0


def test_add_book_under_zero_total(manager_with_book:LibraryManager,monkeypatch)->None:
    save_calls = patch_save(manager=manager_with_book,monkeypatch=monkeypatch)
    result = manager_with_book.add_book(book_id= "B0069",title= "mowjdasjbb",author="kkolok",category="xiaosiwo l ",total=-1)
    assert len(save_calls)==0
    assert result =="图书总数不合法"
    assert len(manager_with_book.books)==1


def test_add_book_empty_keyword(manager_with_book:LibraryManager,monkeypatch)->None:
    save_calls = patch_save(manager=manager_with_book,monkeypatch=monkeypatch)
    result = manager_with_book.add_book(book_id="",title="sdaida",category="ashdjahd",total=95,author="sdbnjahd")
    assert result =="字段不能为空"
    assert len(save_calls)==0
    assert len(manager_with_book.books)==1

    
def test_borrow_book_success(manager_with_book_and_user:LibraryManager,monkeypatch)->None:
    save_calls = patch_save(manager=manager_with_book_and_user,monkeypatch=monkeypatch)
    result = manager_with_book_and_user.borrow_book(book_id="B888",user_id="U001")
    assert result == "借书成功"
    assert len(save_calls)==1
    assert manager_with_book_and_user.books[0].available == 99
    assert "B888" in  manager_with_book_and_user.users[0].borrowed


def test_borrow_book_user_not_found(manager_with_book_and_user:LibraryManager,monkeypatch)->None:
    save_calls = patch_save(manager=manager_with_book_and_user,monkeypatch=monkeypatch)
    result = manager_with_book_and_user.borrow_book(user_id="U10086",book_id="B888")
    assert result == "用户不存在"
    assert len(save_calls)==0
    assert manager_with_book_and_user.books[0].available ==100
    assert len(manager_with_book_and_user.users[0].borrowed) == 0


def test_borrow_book_book_not_found(manager_with_book_and_user:LibraryManager,monkeypatch)->None:
    save_calls = patch_save(manager=manager_with_book_and_user,monkeypatch=monkeypatch)
    result = manager_with_book_and_user.borrow_book(user_id="U001",book_id="B8989")
    assert result =="图书不存在"
    assert len(save_calls)==0
    assert manager_with_book_and_user.books[0].available ==100
    assert len(manager_with_book_and_user.users[0].borrowed)==0


def test_borrow_book_done_book(manager_with_book_and_user:LibraryManager,monkeypatch)->None:
    save_calls = patch_save(manager=manager_with_book_and_user,monkeypatch=monkeypatch)
    manager_with_book_and_user.books[0].available = 0
    result = manager_with_book_and_user.borrow_book(user_id="U001",book_id="B888")
    assert result =="图书已借完"
    assert len(save_calls)==0
    assert len(manager_with_book_and_user.users[0].borrowed) ==0
    assert manager_with_book_and_user.books[0].available ==0

    
def test_borrow_book_reborrow_book(manager_with_book_and_user:LibraryManager,monkeypatch)->None:
    save_calls = patch_save(manager=manager_with_book_and_user,monkeypatch=monkeypatch)
    result1 = manager_with_book_and_user.borrow_book(user_id="U001",book_id="B888")
    result2 = manager_with_book_and_user.borrow_book(user_id="U001",book_id="B888")
    assert result1 =="借书成功"
    assert result2 == "不能重复借同一本书"
    assert len(save_calls)==1
    assert manager_with_book_and_user.books[0].available ==99
    assert "B888" in manager_with_book_and_user.users[0].borrowed