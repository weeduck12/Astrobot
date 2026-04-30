import aiosqlite

DB_PATH = 'database.db'

async def init_db():
    
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS worlds (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name      TEXT NOT NULL,
                url       TEXT
            )
        ''' )
        await db.execute('''
            CREATE TABLE IF NOT EXISTS sub_series (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                world_id        INTEGER NOT NULL,
                name  TEXT NOT NULL,
                FOREIGN KEY (world_id) REFERENCES worlds(id)        
            )
        ''')    
        await db.execute('''
            CREATE TABLE IF NOT EXISTS zones (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                world_id         INTEGER NOT NULL,
                sub_series_id    INTEGER DEFAULT NULL,
                name        TEXT NOT NULL,
                url         TEXT,
                foreign key (world_id) REFERENCES worlds(id),
                foreign key (sub_series_id) REFERENCES sub_series(id)
            )
        ''' )
        await db.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                world_id        INTEGER NOT NULL,
                zone_id         INTEGER DEFAULT NULL,
                sub_series_id   INTEGER DEFAULT NULL,
                name            TEXT NOT NULL,
                url             TEXT,
                hp              INTEGER DEFAULT 100,
                defense         INTEGER DEFAULT 30,
                special_defense INTEGER DEFAULT 30,
                resistance      INTEGER DEFAULT 30,
                attack          INTEGER DEFAULT 50,
                attack_stamina  INTEGER DEFAULT 50,
                special_attack  INTEGER DEFAULT 50,
                special_stamina INTEGER DEFAULT 50,
                speed           INTEGER DEFAULT 20,
                foreign key (world_id) REFERENCES worlds(id),
                foreign key (zone_id) REFERENCES zones(id),
                foreign key (sub_series_id) REFERENCES sub_series(id)
            )
        ''')
        await db.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                type        TEXT NOT NULL,
                world_id    INTEGER DEFAULT NULL,
                url         TEXT,
                foreign key (world_id) REFERENCES worlds(id)
            )
        ''' )
        await db.execute('''
            CREATE TABLE IF NOT EXISTS user_items (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name        TEXT NOT NULL,
                type        TEXT NOT NULL,
                quantity         INTEGER NOT NULL,
                url         TEXT
            )
        ''' )
        await db.execute('''
            CREATE TABLE IF NOT EXISTS user_collection (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id        TEXT NOT NULL,
                character_id    INTEGER NOT NULL,
                copies         INTEGER DEFAULT 1,
                foreign key (character_id) REFERENCES characters(id)
            )
        ''' )
        await db.commit()
async def add_character(name, series, char_url, hp, defense, special_defense, resistance, attack, attack_stamina, special_attack, special_stamina, speed):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO characters (name, series, char_url, hp, defense, special_defense, resistance, attack, attack_stamina, special_attack, special_stamina, speed)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, series, char_url, hp, defense, special_defense, resistance, attack, attack_stamina, special_attack, special_stamina, speed))
        await db.commit()

async def add_user_item(item_name, item_type, quantity, item_url):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO user_items (item_name, item_type, quantity, item_url)
            VALUES (?, ?, ?, ?)
        """, (item_name, item_type, quantity, item_url))
        await db.commit()

async def add_world(map_name, zone_id, world_url):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO worlds (map_name, zone_id, world_url)
            VALUES (?, ?, ?)
        """, (map_name, zone_id, world_url))
        await db.commit()

async def add_zone(zone_name, zone_url):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            INSERT INTO zones (zone_name, zone_url)
            VALUES (?, ?)
        """, (zone_name, zone_url))
        await db.commit()

async def get_random_zone(world_id):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT * FROM zones
            WHERE world_id = ?
            ORDER BY RANDOM()
            LIMIT 1
        """, (world_id,)) as cursor:
            return await cursor.fetchone()
        
async def get_random_character(zone_id):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT * FROM characters
            WHERE zone_id = ?
            ORDER BY RANDOM()
            LIMIT 1
        """, (zone_id,)) as cursor:
            return await cursor.fetchone()
    
async def activate_pass(user_id, item_id, duration_hours):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            UPDATE user_items SET quantity = quantity - 1
            WHERE user_id = ? AND item_id = ? AND quantity > 0
        """, (user_id, item_id))
        await db.execute("""
            UPDATE user_items SET expires_at = datetime('now', '+? hours')
            WHERE user_id = ? AND item_id = ?
        """, (duration_hours, user_id, item_id))
        await db.commit()

async def get_active_passes(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT * FROM user_items
            WHERE user_id = ? AND type = 'pass' AND expires_at > datetime('now')
          """,(user_id,)) as cursor:
            return await cursor.fetchone()