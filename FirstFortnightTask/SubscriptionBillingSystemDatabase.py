from sqlalchemy import create_engine, text

database = create_engine(
    "postgresql+psycopg2://postgres:k4sh%40L1014@localhost/SubscriptionBillingSystem")


with database.connect() as conn:
    result = conn.execute(text("SELECT * FROM users"))
    for row in result:
        print(row)



insert_query = text("""insert into users(name, address, age, email)
                    values(:name, :address, :age, :email)""")

user_data= {
    "name": "Abhram Lincoln",
    "address": "123 Main St, Springfield",
    "age": 55,
    "email": "abhram.lincoln@example.com"
}

with database.connect() as conn:
    conn.execute(insert_query, user_data)
    conn.commit()

print("New user inserted successfully.")