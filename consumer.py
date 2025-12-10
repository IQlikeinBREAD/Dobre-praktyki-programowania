import time
import sqlite3

def process_tasks():
    while True:
        con = sqlite3.connect('tasks.db')
        cur = con.cursor()

        cur.execute("SELECT id FROM task WHERE status = 'pending' LIMIT 1")
        result = cur.fetchone()

        if result:
            task_id = result[0]

            cur.execute("UPDATE task SET status = 'in_progres' WHERE id = ?", (task_id,))
            con.commit()
            con.close()

            print(f"Pobrano zadanie: {task_id}")
            print(f"Praca nad {task_id} trwa (30s)...")

            time.sleep(30)

            con = sqlite3.connect('tasks.db')
            cur = con.cursor()
            cur.execute("UPDATE task SET status = 'done' WHERE id = ?", (task_id,))
            con.commit()
            con.close()

            print(f"Zadanie {task_id} wykonane.")
        
        else:
            con.close()
            print("Brak zadań 'pending'. Czekam 5s...")
            time.sleep(5)

if __name__ == "__main__":
    process_tasks()