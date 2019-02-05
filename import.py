import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

engine = create_engine(os.getenv('DATABASE_URL'))
db = scoped_session(sessionmaker(bind=engine))

def main():
    with open('books.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        id = 1
        for isbn, title, author, year in reader:
            db.execute("INSERT INTO books (book_id, isbn, title, author, year) VALUES (:book_id, :isbn, :title, :author, :year)",
                        {"book_id": id, "isbn": isbn, "title": title, "author": author, "year": year})
            print(f"Added book {title} by {author}, {year}. ISBN: {isbn}")
            id += 1
            db.commit()


if __name__ == '__main__':
    main()