import sqlite3 , os

if __name__ == "__main__":
    from app import create
    app = create()
    app.run()