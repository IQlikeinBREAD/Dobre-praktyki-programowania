import uuid
import sqlite3

def produce_taks():
    con = sqlite3.connect("tasks.db")
    cur = con.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS task(
                id TEXT PRIMARY KEY,
                status TEXT
                )''')
    
    con.commit()

    for i in range(100):
        task_id = str(uuid.uuid4())
        cur.execute("INSERT INTO task (id, status) VALUES (?, ?)", (task_id,'pending'))

    con.commit()
    con.close()
    
if __name__ == "__main__":
    produce_taks()