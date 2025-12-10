import uuid

def produce_taks():
    with open('tasks.txt','a') as file:
        for i in range(100):
            task_id = uuid.uuid4()
            file.write(f"{task_id},pending\n")

if __name__ == "__main__":
    produce_taks()