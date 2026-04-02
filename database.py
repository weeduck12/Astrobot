import aiosqlite

DB_PATH = 'database.db'

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT NOT NULL,
                series          TEXT,
                image_url       TEXT,
                hp              INTEGER DEFAULT 100,
                defense         INTEGER DEFAULT 30,
                special_defense INTEGER DEFAULT 30,
                resistance      INTEGER DEFAULT 30,
                attack          INTEGER DEFAULT 50,
                attack_stamina  INTEGER DEFAULT 50,
                special_attack  INTEGER DEFAULT 50,
                special_stamina INTEGER DEFAULT 50,
                speed           INTEGER DEFAULT 20
            )
        ''')
        await db.commit()

async def add_character(name, series, image_url, hp, defense, special_defense, resistance, attack, attack_stamina, special_attack, special_stamina, speed):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO characters (name, series, image_url, hp, defense, special_defense, resistance, attack, attack_stamina, special_attack, special_stamina, speed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, series, image_url, hp, defense, special_defense, resistance, attack, attack_stamina, special_attack, special_stamina, speed))
        await db.commit()