import time

def process_tasks():
    while True:
        task_found = False
        task_index = -1
        lines = []
        try:
            with open("tasks.txt","r") as file:
                lines = file.readlines()

            for index, line in enumerate(lines):
                if 'pending' in line:
                    task_index = index
                    task_found = True
        except FileNotFoundError:
            print("Brak pliku tasks.txt")
            time.sleep(5)
            continue
        
        if task_found:
            task_id, _ = lines[task_index].strip().split(',')
            print(f"Pobrano zadanie: {task_id}")

            lines[task_index] = f"{task_id},in_progress\n"

            with open('tasks.txt','w') as file:
                file.writelines(lines)

            print(f"Praca nad {task_id} trwa...")
            time.sleep(30)

            with open('tasks.txt','r') as file:
                current_lines = file.readlines()
            
            current_lines[task_index] = f"{task_id},done\n"
            
            with open('tasks.txt','w') as file:
                file.writelines(current_lines)
            
            print(f"Zadanie {task_id} wykonane.")

        else:
            print("Brak zadan. Czekam...")
            time.sleep(5)

if __name__ == "__main__":
    process_tasks()