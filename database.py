import sqlite3 as sql
import uuid

class Database:
    def __init__(self) -> None:
        """Constructor for database class
        """
        try:
            # Connecting the program to the database for all the points
            self.conn = sql.connect('database.db')

            # Used to perform SQL operations
            self.c = self.conn.cursor()

            # Creating the tables
            self.c.execute("""
                CREATE TABLE chatters 
                    (
                        id TEXT primary key,
                        username TEXT NOT NULL,
                        points INTEGER DEFAULT 0
                    );
            """)

            self.conn.commit()

            self.c.execute("""
                CREATE TABLE transactions
                    (
                        id TEXT PRIMARY KEY,
                        userID TEXT,
                        date DATE,
                        action TEXT,
                        points TEXT,
                        FOREIGN KEY(userID) REFERENCES chatters(id)
                    );
            """)

            self.conn.commit()

            self.c.execute("""
                CREATE TABLE commands
                    (
                        id TEXT PRIMARY KEY,
                        name TEXT NOT NULL,
                        points INTEGER DEFAULT 100,
                        action TEXT NOT NULL,
                        params TEXT NOT NULL
                    );
            """)

            self.conn.commit()
            
        except sql.OperationalError:
            # Database has already been created
            print("Database has already been created")
        
    def insert_user(self, username: str) -> bool:
        """Insert a new chatter into the chatters table
        Args:   username (str): The username of the chatter
        """
        # Checking if the user already exists in the table as the username should be unique
        self.c.execute(f"SELECT * FROM chatters WHERE username='{username}'")

        if self.c.fetchone() != None: 
            print("User already exists")
            return False

        uid = str(abs(hash(username))) # Generating hash for the username

        # Execution statement to insert new chatter
        self.c.execute(f"""
            INSERT INTO chatters (id, username, points)
            VALUES ('{uid}', '{username}', 0)
        """)

        # Committing to the database
        self.conn.commit()

        return True
    
    def get_points(self, username: str) -> int:
        """Gets the points of a certain chatter
        Args:   username (str): The username of the chatter
        """

        self.c.execute(f"""
            SELECT points 
            FROM chatters 
            WHERE username='{username}'
        """)

        return int(self.c.fetchone()[0])

    def deduct_points(self, username: str, points: int) -> bool:
        """Remove points from a certain chatter
        Args:   username (str): The username of the chatter
                points (int): The points to be added to the chatter
        """

        # Calculating the new points
        new_points = self.get_points(username) - points

        # If the user will have negative points then return False
        if new_points < 0: return False

        # Updating the points value for that user
        self.c.execute(f"""
            UPDATE chatters
            SET points={new_points}
            WHERE username='{username}'
        """)

        # Committing to the database
        self.conn.commit()
    
        return True
    
    def add_points(self, username: str, points: int) -> None:
        """Remove points from a certain chatter
        Args:   username (str): The username of the chatter
                points (int): The points to be added to the chatter
        """

        # Calculating the new points
        new_points = self.get_points(username) + points

        # Updating the points value for that user
        self.c.execute(f"""
            UPDATE chatters
            SET points={new_points}
            WHERE username='{username}'
        """)

        # Committing to the database
        self.conn.commit()
    
    def get_user_id(self, username: str) -> str:
        self.c.execute(f"""
            SELECT id
            FROM chatters
            WHERE username='{username}'
        """)

        return self.c.fetchone()[0]

    def user_exists(self, username: str) -> bool:
        # Checking if the user already exists in the table as the username should be unique
        self.c.execute(f"SELECT * FROM chatters WHERE username='{username}'")

        return self.c.fetchone() != None

    def add_transaction(self, transaction: dict) -> None:
        """Adds a transaction to the database
        Args:   transaction (dict[str, str]): Dictionary with transaction information
        """

        id = str(uuid.uuid4())
        user_id = self.get_user_id(transaction["username"])

        self.c.execute(f"""
            INSERT INTO transactions(id, userID, date, action, points)
            VALUES ('{id}', '{user_id}', DATETIME('now'), '{transaction["action"]}', {transaction["points"]})
        """)

        self.conn.commit()

    # Command Functions
    def get_commands(self):
        self.c.execute("SELECT * FROM commands")
        
        return self.c.fetchall()

