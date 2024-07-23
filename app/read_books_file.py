import pandas as pd
from sqlalchemy.orm import Session
from common.CRUD.book_crud import *
from common.CRUD.author_crud import *
from common.database.database import session_local, get_db
from schemas.author import AuthorSchema
from schemas.book import BookSchema

def process_csv(file_path: str, db: Session):
    df = pd.read_csv(file_path, usecols=['title', 'authors', 'categories', 'description'])

    for index, row in df.iterrows():
        title = row['title']
        author_names = row['authors'].split(';')  
        categories = row['categories']
        description = row['description']
        
        book_data = BookSchema(title=title, categories=categories, description=description)
        create_book(db, book_data)
        for author_name in author_names:
            book_data = AuthorSchema(name=author_name , biography=None)
            db_author = get_author_id_by_name(db, author_name)
            if not db_author:
                author_data = AuthorSchema(name=author_name, biography=None)
                db_author = create_author(db, author_data)
                db_author = get_author_id_by_name(db, author_name)
                print(db_author)
                associate_book_with_author(db, book_data, author_data)

# Can i call the get_db and use it ?
db_session = session_local()
process_csv('cleaned_books.csv', db_session)
db_session.close()