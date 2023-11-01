#!/usr/bin/env python
# coding: utf-8

import json
import os
import sqlite3


def database(books_file: str, authors_file: str, list_file: str, series_file: str) -> sqlite3.Cursor:
    """
    Either create a new database called tables.db or establish a connection if already exists.

    Args:
        books_file (str): Books file path.
        authors_file (str): Authors file path.
        list_file (str): List file path.
        sereis_file (str): Series file path.

    Returns:
        cursor (sqlite3.Cursor): Database connection.
    """
    
    # Check if database file already exists, if yes establish connection and if not create the file
    if os.path.isfile('tables.db'):
        conn = sqlite3.connect('tables.db')
        cursor = conn.cursor()
        print("Connection to the database tables.db was successfully established!")
        
    else:
        conn = sqlite3.connect('tables.db')
        cursor = conn.cursor()
        # Create table authors if not exists
        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS authors
                            (
                                id INT,
                                ratings_count INT,
                                average_rating FLOAT,
                                text_reviews_count INT,
                                name TEXT,
                                gender TEXT,
                                about TEXT,
                                fans_count INT
                            )
                        """)

        # Create table with mapping from book to author if not exists
        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS book_to_author
                            (
                                author_id INT,
                                book_id INT
                            )
                        """)

        # Create table books if not exists
        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS books
                            (
                                id INT,
                                title TEXT,
                                author_id INT,
                                language TEXT,
                                average_rating FLOAT,
                                rating_dist_1 INT,
                                rating_dist_2 INT,
                                rating_dist_3 INT,
                                rating_dist_4 INT,
                                rating_dist_5 INT,
                                ratings_count INT,
                                text_reviews_count INT,
                                publication_date TEXT,
                                original_publication_date TEXT,
                                format TEXT,
                                num_pages INT,
                                series_id INT,
                                description TEXT
                            )
                        """)

        # Create table with worst books list if not exists
        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS worst_books_list
                            (
                                book_id INT,
                                title TEXT,
                                author_id INT,
                                author TEXT
                            )
                        """)
        
 
        # Create table series if not exists
        cursor.execute("""
                            CREATE TABLE IF NOT EXISTS series
                            (
                                id INT,
                                title TEXT
                            )
                        """)
        
        # Parse through the books file and add every entry to the books table
        # The ratings list is being split in one column for every rating each
        with open(books_file, 'r') as f:

            for line in f:

                if len(line) > 1:

                    entry = json.loads(line)

                    book_id = int(entry.get('id'))
                    title = str(entry.get('title'))
                    author_id = int(entry.get('author_id'))
                    language = str(entry.get('language'))
                    average_rating = float(entry.get('average_rating'))
                    rating_dist = [int(rating[2:]) for rating in entry.get('rating_dist', '').split('|')[:-1]]
                    rating_dist_1 = rating_dist[4]
                    rating_dist_2 = rating_dist[3]
                    rating_dist_3 = rating_dist[2]
                    rating_dist_4 = rating_dist[1]
                    rating_dist_5 = rating_dist[0]
                    ratings_count = int(entry.get('ratings_count'))
                    text_reviews_count = int(entry.get('text_reviews_count'))
                    publication_date = str(entry.get('publication_date'))
                    original_publication_date = str(entry.get('original_publication_date'))
                    format = str(entry.get('format'))
                    try:
                        num_pages = int(entry.get('num_pages'))
                    except:
                        num_pages = None
                    try:
                        series_id = int(entry.get('series_id'))
                    except:
                        series_id = None
                    description = str(entry.get('description'))
                        
                    cursor.execute("""
                                        INSERT INTO books
                                        (
                                            id,
                                            title,
                                            author_id,
                                            language,
                                            average_rating,
                                            rating_dist_1,
                                            rating_dist_2,
                                            rating_dist_3,
                                            rating_dist_4,
                                            rating_dist_5,
                                            ratings_count,
                                            text_reviews_count,
                                            publication_date,
                                            original_publication_date,
                                            format,
                                            num_pages,
                                            series_id,
                                            description
                                        )
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                                    """,
                                   (book_id,
                                    title,
                                    author_id,
                                    language,
                                    average_rating,
                                    rating_dist_1,
                                    rating_dist_2,
                                    rating_dist_3,
                                    rating_dist_4,
                                    rating_dist_5,
                                    ratings_count,
                                    text_reviews_count,
                                    publication_date,
                                    original_publication_date,
                                    format,
                                    num_pages,
                                    series_id,
                                    description))

        conn.commit()
        
        # Parse through the authors file and split the column with book ids to a mapped table
        # Example:
        # author1 -> book_id1
        # author1 -> book_id2
        # author1 -> book_id3
        # author2 -> book_id4
        # author2 -> book_id5
        with open(authors_file, 'r') as f:

            for line in f:

                if len(line) > 1:

                    entry = json.loads(line)

                    author_id = int(entry.get('id'))
                    book_ids = entry.get('book_ids')

                    for book_id in book_ids:

                        cursor.execute("""
                                            INSERT INTO book_to_author
                                            (
                                                author_id,
                                                book_id
                                            )
                                            VALUES (?, ?)
                                        """,
                                       (author_id,
                                        int(book_id)))

        conn.commit()
        
        # Parse through the authors file and add every entry to the authors table
        with open(authors_file, 'r') as f:

            for line in f:

                if len(line) > 1:

                    entry = json.loads(line)

                    ratings_count = int(entry.get('ratings_count'))
                    average_rating = float(entry.get('average_rating'))
                    text_reviews_count = int(entry.get('text_reviews_count'))
                    id = int(entry.get('id'))
                    name = str(entry.get('name'))
                    gender = str(entry.get('gender'))
                    about = str(entry.get('about'))
                    fans_count = int(entry.get('fans_count'))

                    cursor.execute("""
                                        INSERT INTO authors 
                                        (
                                            id,
                                            ratings_count,
                                            average_rating,
                                            text_reviews_count,
                                            name,
                                            gender,
                                            about,
                                            fans_count
                                        )
                                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                                    """,
                                   (id,
                                    ratings_count,
                                    average_rating,
                                    text_reviews_count,
                                    name,
                                    gender,
                                    about,
                                    fans_count))

        conn.commit()
        
        # Parse through the list file and extract only the list with the title 'The Worst Books of All Time'
        with open(list_file, 'r') as f:
            for line in f:
                item = json.loads(line)
                if item['title'] == 'The Worst Books of All Time':
                    for book in item['books']:

                        book_id = int(book.get('book_id'))
                        title = str(book.get('title'))
                        author_id = int(book.get('author_id'))
                        author = str(book.get('author'))

                        cursor.execute("""
                                                INSERT INTO worst_books_list
                                                (
                                                    book_id,
                                                    title,
                                                    author_id,
                                                    author
                                                )
                                                VALUES (?, ?, ?, ?)
                                            """,
                                           (book_id,
                                            title,
                                            author_id,
                                            author))

        conn.commit()
        
        # Parse through the series file and add every entry to the series table
        with open(series_file, 'r') as f:

            for line in f:

                if len(line) > 1:

                    entry = json.loads(line)

                    id = int(entry.get('id'))
                    title = entry.get('title')

                    cursor.execute("""
                                        INSERT INTO series
                                        (
                                            id,
                                            title
                                        )
                                        VALUES (?, ?)
                                    """,
                                   (id,
                                    title))

        conn.commit()
        
        # Add a new column year and month based on the publication_date in books
        cursor.execute("ALTER TABLE books ADD COLUMN publication_month INTEGER")
        cursor.execute("ALTER TABLE books ADD COLUMN publication_year INTEGER")
        cursor.execute("UPDATE books SET publication_month = substr(publication_date, 6, 2), \
                        publication_year = substr(publication_date, 1, 4)")
        conn.commit()

        # Add indices for better query performance
        cursor.execute("create index book_index on books(id)")
        conn.commit()
        cursor.execute("create index author_index on authors(id)")
        conn.commit()
        cursor.execute("create index series_index on series(id)")
        conn.commit()
        cursor.execute("create index idx_books_covering on books(publication_year, publication_month, num_pages, id, author_id)")
        conn.commit()
        cursor.execute("create index idx_books_id_author_id on books(id, author_id)")
        conn.commit()
        cursor.execute("create index idx_book_to_author_book_id_author_id on book_to_author(book_id, author_id)")
        conn.commit()
        
        print("Database tables.db was successfully created and connection established!")
        
    return conn, cursor


def clean_database():
    
    # Connect to database
    conn = sqlite3.connect('tables.db')
    cursor = conn.cursor()
    
    # Clean books table
    cursor.execute("""
                        DELETE FROM books
                        WHERE id < 1 OR LENGTH(title) < 1 OR author_id < 1 OR NOT (publication_date LIKE '____-__-__'
                        AND strftime('%Y-%m-%d', publication_date) = publication_date AND date(publication_date) <= date('now'))
                        OR NOT (original_publication_date LIKE '____-__-__' AND strftime('%Y-%m-%d', original_publication_date) =
                        original_publication_date AND date(original_publication_date) <= date('now')) OR num_pages < 1
                        OR num_pages IS NULL OR (series_id IS NOT NULL AND series_id < 1)
                   """)
    
    conn.commit()
    
    # Clean authors table
    cursor.execute("""
                        DELETE FROM authors
                        WHERE id < 1 OR ratings_count < 0 OR average_rating < 0 OR text_reviews_count < 0 OR LENGTH(name) < 1
                        OR fans_count < 0
                   """)
    
    conn.commit()   
