"""Biblio : gestion des prets de livres d'une petite bibliotheque associative.

Usage :
    python biblio.py init
    python biblio.py livres
    python biblio.py chercher <texte>
    python biblio.py emprunter <id_livre> <id_membre>
    python biblio.py rendre <id_livre>
    python biblio.py retards
"""

import os
import sqlite3
import sys
from datetime import date, datetime, timedelta

DB_PATH = os.environ.get("BIBLIO_DB", "biblio.db")
LOAN_DAYS = 14


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.executescript(
        """
        DROP TABLE IF EXISTS loans;
        DROP TABLE IF EXISTS books;
        DROP TABLE IF EXISTS members;

        CREATE TABLE books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL
        );

        CREATE TABLE members (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );

        CREATE TABLE loans (
            id INTEGER PRIMARY KEY,
            book_id INTEGER NOT NULL REFERENCES books(id),
            member_id INTEGER NOT NULL REFERENCES members(id),
            loan_date TEXT NOT NULL,
            return_date TEXT
        );
        """
    )
    books = [
        (1, "L'Etranger", "Albert Camus"),
        (2, "Dune", "Frank Herbert"),
        (3, "Le Petit Prince", "Antoine de Saint-Exupery"),
        (4, "Fondation", "Isaac Asimov"),
        (5, "Les Miserables", "Victor Hugo"),
        (6, "Neuromancien", "William Gibson"),
    ]
    members = [(1, "Alice Martin"), (2, "Bilal Haddad"), (3, "Chloe Nguyen")]
    loans = [
        (1, 2, 1, "2026-01-10", None),
        (2, 4, 2, "2026-01-05", "2026-01-12"),
    ]
    cur.executemany("INSERT INTO books VALUES (?, ?, ?)", books)
    cur.executemany("INSERT INTO members VALUES (?, ?)", members)
    cur.executemany("INSERT INTO loans VALUES (?, ?, ?, ?, ?)", loans)
    conn.commit()
    conn.close()
    print("Base initialisee : %d livres, %d membres." % (len(books), len(members)))


def list_books():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, author FROM books ORDER BY id")
    books = cur.fetchall()
    for book in books:
        cur.execute(
            "SELECT member_id FROM loans WHERE book_id = ? AND return_date IS NULL",
            (book[0],),
        )
        loan = cur.fetchone()
        status = "disponible" if loan is None else "emprunte"
        print(f"[{book[0]}] {book[1]} - {book[2]} ({status})")
    conn.close()


def search(text):
    conn = get_connection()
    cur = conn.cursor()
    pattern = f"%{text}%"
    cur.execute(
        """
        SELECT id, title, author FROM books
        WHERE title LIKE ? OR author LIKE ?
        ORDER BY id
        """,
        (pattern, pattern),
    )
    books = cur.fetchall()
    for book in books:
        cur.execute(
            "SELECT member_id FROM loans WHERE book_id = ? AND return_date IS NULL",
            (book[0],),
        )
        loan = cur.fetchone()
        status = "disponible" if loan is None else "emprunte"
        print(f"[{book[0]}] {book[1]} - {book[2]} ({status})")
    conn.close()


def borrow(book_id, member_id):
    conn = get_connection()
    cur = conn.cursor()

    # Verify book existence
    cur.execute("SELECT id FROM books WHERE id = ?", (book_id,))
    if cur.fetchone() is None:
        print("Livre introuvable.")
        conn.close()
        return

    # Verify member existence
    cur.execute("SELECT id FROM members WHERE id = ?", (member_id,))
    if cur.fetchone() is None:
        print("Membre introuvable.")
        conn.close()
        return

    # Prevent double loan
    cur.execute(
        "SELECT id FROM loans WHERE book_id = ? AND return_date IS NULL", (book_id,)
    )
    if cur.fetchone():
        print("Le livre est déjà emprunté.")
        conn.close()
        return

    loan_date = date.today().isoformat()
    cur.execute(
        """
        INSERT INTO loans (book_id, member_id, loan_date, return_date)
        VALUES (?, ?, ?, NULL)
        """,
        (book_id, member_id, loan_date),
    )
    conn.commit()
    print(f"Emprunt du livre {book_id} enregistré pour le membre {member_id}.")
    conn.close()


def return_book(book_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM loans WHERE book_id = ? AND return_date IS NULL", (book_id,)
    )
    loan = cur.fetchone()
    if not loan:
        print("Ce livre n'est pas emprunté.")
        conn.close()
        return

    return_date = date.today().isoformat()
    cur.execute(
        "UPDATE loans SET return_date = ? WHERE id = ?", (return_date, loan[0])
    )
    conn.commit()
    print(f"Le livre {book_id} a été rendu.")
    conn.close()


def overdue():
    conn = get_connection()
    cur = conn.cursor()
    cutoff = (date.today() - timedelta(days=LOAN_DAYS)).isoformat()
    cur.execute(
        """
        SELECT loans.id, books.title, members.name, loans.loan_date
        FROM loans
        JOIN books ON loans.book_id = books.id
        JOIN members ON loans.member_id = members.id
        WHERE loans.return_date IS NULL AND loans.loan_date <= ?
        ORDER BY loans.loan_date
        """,
        (cutoff,),
    )
    rows = cur.fetchall()
    if not rows:
        print("Aucun retard.")
    else:
        print("Livres en retard :")
        for loan_id, title, member_name, loan_date in rows:
            print(f"- [{loan_id}] {title} (emprunté par {member_name} le {loan_date})")
    conn.close()


def main():
    if len(sys.argv) < 2:
        print("Commande manquante.")
        return

    cmd = sys.argv[1]

    if cmd == "init":
        init_db()
    elif cmd == "livres":
        list_books()
    elif cmd == "chercher":
        if len(sys.argv) < 3:
            print("Texte de recherche manquant.")
            return
        search(" ".join(sys.argv[2:]))
    elif cmd == "emprunter":
        if len(sys.argv) != 4:
            print("Usage: python biblio.py emprunter <id_livre> <id_membre>")
            return
        borrow(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "rendre":
        if len(sys.argv) != 3:
            print("Usage: python biblio.py rendre <id_livre>")
            return
        return_book(int(sys.argv[2]))
    elif cmd == "retards":
        overdue()
    else:
        print(f"Commande inconnue : {cmd}")


if __name__ == "__main__":
    main()