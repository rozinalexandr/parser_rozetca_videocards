import sqlite3

connection = sqlite3.connect("videocards_db.sqlite")

connection.execute("""
    CREATE TABLE source(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        price TEXT,
        memory_frequency TEXT,
        graphics_chip TEXT,
        memory_capacity TEXT,
        max_resolution TEXT,
        min_power_capacity TEXT
    )
""")
