import os

from sqlalchemy import URL, create_engine, text


DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "5432"))
DB_NAME = os.getenv("DB_NAME", "SubscriptionBillingSystem")

if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD environment variable is required.")

database = create_engine(
    URL.create(
        "postgresql+psycopg2",
        username=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
    )
)


with database.connect() as conn:

    print("\n--- USERS ---")
    result = conn.execute(text("SELECT * FROM users"))
    for row in result:
        print(row)

    
    print("\n--- PLANS ---")
    result = conn.execute(text("SELECT * FROM plans"))
    for row in result:
        print(row)
    
    print("\n--- SUBSCRIPTIONS ---")
    result = conn.execute(text("SELECT * FROM subscriptions"))
    for row in result:
        print(row)

    print("\n--- INVOICES ---") 
    result = conn.execute(text("SELECT * FROM invoices"))
    for row in result:
        print(row)


# -------------------------
# INSERT DATA (Auto Commit)
# -------------------------


insert_query = text("""insert into users(name, address, age, email)
                    values(:name, :address, :age, :email)""")

user_data= {
    "name": "Abhram Lincoln",
    "address": "123 Main St, Springfield",
    "age": 55,
    "email": "abhram.lincoln@example.com"
}

with database.begin() as conn:
    conn.execute(insert_query, user_data)

print("New user inserted successfully.")