import pyodbc

def connect_db():
    """Attempts to connect to the database."""
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=localhost;"  
            "DATABASE=DummyDatabase;"  
            "UID=userName_1;"  
            "PWD=sqlusername;" 
            "TrustServerCertificate=yes;" 
        )
        print("✅ Database connection successful!")
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")


def print_table_content(table_name):
    """Fetch and print all content from a given table."""
    conn = connect_db()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]  # Get column names

        # Print column headers
        print(f"\n📌 Table: {table_name}")
        print("-" * 40)
        print("\t".join(columns))
        print("-" * 40)

        # Print each row
        for row in rows:
            print("\t".join(str(cell) for cell in row))

    except Exception as e:
        print(f"❌ Error fetching table data: {e}")
    finally:
        conn.close()

# Example Usage
if __name__ == "__main__":
    table_name = input("Enter table name: ")  # Get table name from user
    print_table_content(table_name)
