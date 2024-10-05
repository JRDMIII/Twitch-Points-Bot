import sqlite3 as sql

class Database:
    def __init__(self) -> None:
        try:
            # Connecting the program to the database for all the points
            self.conn = sql.connect('database.db')
        
            self.c = self.conn.cursor()

            self.c.execute("""
                CREATE TABLE chatters 
                    (
                        id text primary key,
                        username text,
                        points int
                    );
            """)
        except sql.OperationalError:
            # Database has already been created
            print("Database has already been created")
        
    def insert_user(self, username: str) -> None:
        """Insert a new chatter into the chatters table
        Args:   username (str): The username of the chatter
        """

        uid = hash(username) # Generating hash for the username

        # Execution statement to insert new chatter
        self.c.execute(f"""
            INSERT INTO chatters (id, username, points)
            VALUES ('{uid}', '{username}', 0)
        """)

        # Committing to the database
        self.conn.commit()
    
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
    

if __name__ == "__main__":
    db = Database()
    db.get_points("James")
    