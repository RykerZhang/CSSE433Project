from pyignite import Client
client = Client()
client.connect('433-34.csse.rose-hulman.edu', 10800)

Books = client.get_or_create_cache("Books")
Title_ISBN = client.get_or_create_cache("Title_ISBN")
isbn_authors = client.get_or_create_cache("isbn_authors")
# Books.remove_all()
# Title_ISBN.remove_all()
# isbn_authors.remove_all()
# print(Books.get("1"))
def listToString(s):
    str1 = " "
    return (str1.join(s))
        
def addBook(title, author, ISBN, pageNum):
    if(Books.get(ISBN) == None):
        Title_ISBN.put(title, ISBN)
        Books.put(ISBN, (title, ISBN, pageNum))
        isbn_authors.put(ISBN, author)
        print("Book added.\n")
    else:
        print("ISBN already exists.\n")

def deleteBook(title):
    if(Title_ISBN.get(title)!=None):
       isbn = Title_ISBN.get(title)
       Title_ISBN.remove_key(title)
       Books.remove_key(isbn)
       isbn_authors.remove_key(isbn)
       print("Book deleted\n")
    else:
        print("Book does not exist.\n")

def editBook(title, InformationToEdit, newInformation):
    #check title existence
    if(Title_ISBN.get(title)==None):
        print("Book does not exist.\n")
        return
    isbn = Title_ISBN.get(title)
    book = Books.get(isbn)
    title = book[0]
    isbn = book[1]
    pagenumber = book[2]
    authors = isbn_authors.get(isbn)
    if(InformationToEdit.lower() == "title"):
        #check title existence
        if(Title_ISBN.get(newInformation)!=None):
            print("Book title already exist.\n")
            return
        #delete old title in title_isbn
        Title_ISBN.remove_key(title)
        title = newInformation
    elif(InformationToEdit.lower() == "isbn"):
        #chekc isbn existence
        if(Books.get(newInformation)!=None):
            print("Book isbn already exist")
            return
        #delete old one
        Books.remove_key(isbn)
        isbn = newInformation
    elif(InformationToEdit.lower() == "authors"):
        authors = newInformation
    elif(InformationToEdit.lower() == "pagenumber"):
        pagenumber = newInformation
    else:
        print("Please input valid information to edit")
    Title_ISBN.put(title, isbn)
    Books.put(isbn, [title, isbn, pagenumber])
    isbn_authors.put(isbn, authors)
    
def searchBook(InformationToSearch, info):
    if(InformationToSearch.lower() == "title"):
        with Books.scan() as cursor:
            for k, v in cursor:
                title = v[0]
                isbn = v[1]
                pageNumber = v[2]
                if(title == info):
                    authors = isbn_authors.get(isbn)
                    print("Title: " + title + " ISBN: " + isbn + " Authors: "+ listToString(authors) + " PageNumber: " + pageNumber)
    elif(InformationToSearch.lower() == "isbn"):
        with Books.scan() as cursor:
            for k, v in cursor:
                title = v[0]
                isbn = v[1]
                pageNumber = v[2]
                if(isbn == info):
                    authors = isbn_authors.get(isbn)
                    print("Title: " + title + " ISBN: " + isbn + " Authors: "+ listToString(authors) + " PageNumber: " + pageNumber)
    elif(InformationToSearch.lower() == "pagenumber"):
        with Books.scan() as cursor:
            for k, v in cursor:
                title = v[0]
                isbn = v[1]
                pageNumber = v[2]
                if(pageNumber == info):
                    authors = isbn_authors.get(isbn)
                    print("Title: " + title + " ISBN: " + isbn + " Authors: "+ listToString(authors) + " PageNumber: " + pageNumber)   
    elif(InformationToSearch.lower() == "authors"):
        with isbn_authors.scan() as cursor:
            for k, v in cursor: 
                if info in v:
                    output = Books.get(k)
                    title = output[0]
                    isbn = output[1]
                    pageNumber = output[2]
                    print("Title: " + title + " ISBN: " + isbn + " Authors: "+ listToString(v) + " PageNumber: " + pageNumber)
    else:
        print("Pleas input valid information.\n")  
     
def sortBook(InformationToSort):
    if(InformationToSort == "title"):
        titleList = []
        with Books.scan() as cursor:
            for k, v in cursor:
                title = v[0]
                isbn = v[1]
                pageNumber = v[2]
                if(pageNumber == info):
                    authors = isbn_authors.get(isbn) 
  

while(True):
    commandNum = input("Please input the command number.\n0- Exist this application  1- Add Book  2- Delete Book  3- Edit Book  4- Search Book  5- Sort Book\n")
    if(commandNum == "0"):
        print("The application will be shut down.\n")
        exit()
    if(commandNum == "1"):
        author = []
        title = input("Please input the book title:\n")
        AuthorNumber = int(input("Please input the number of authors:\n"))
        for i in range (0,AuthorNumber):
            author.append(input())
        isbn = input("Please input the ISBN:\n")
        pageNum = input("Please input the page number:\n")
        addBook(title, author, isbn, pageNum)
    if(commandNum == "2"):
        title = input("Please enter the book title you want to delete:\n")
        deleteBook(title)
    if(commandNum == "3"):
        title = input("Please enter the book title you want to edit (title, authors, pagenumber, isbn):\n")
        InformationToEdit  = input("Please input the information you want to edit:\n")
        if((InformationToEdit.lower() =="isbn") or (InformationToEdit.lower() =="title")or(InformationToEdit.lower() =="pagenumber")):
            newInformation = input("Please input the new information:\n")
            editBook(title, InformationToEdit, newInformation)
        elif(InformationToEdit.lower() == "authors"):
            newInformation = []
            AuthorNumber = int(input("Please input the number of authors:\n"))
            for i in range (0,AuthorNumber):
                newInformation.append(input())
            editBook(title, InformationToEdit, newInformation)
        else:
            print("Information Not Valid.\n")
    if(commandNum == "4"):
        InformationToSearch = input("Please enter the book information used for searching (title, isbn, pagenumber, authors):\n")
        if((InformationToSearch.lower() =="isbn") or (InformationToSearch.lower() =="authors")or(InformationToSearch.lower() =="pagenumber")or (InformationToSearch.lower() == "title")):
            info = input("Please type the info\n")
            searchBook(InformationToSearch, info)
            print("Search ends. Please continue your command\n\n")
        else:
            print("No such information.\n")
    if(commandNum == "5"):
        InformationToSort = input("Please enter the information you want to for sorting:\n")
        sortBook(InformationToSort)
        print("Sort ends. Please continue your command\n\n")
