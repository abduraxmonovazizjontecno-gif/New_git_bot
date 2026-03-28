import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="1"
)
cursor = conn.cursor()
with open("movies.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()
for line in lines:
    movie = line.strip()
    if movie:
        cursor.execute("INSERT INTO movies (title) VALUES (%s)", (movie,))
conn.commit()
cursor.close()
conn.close()

print("Filmlar muvaffaqiyatli qo'shildi!")