from sqlalchemy import create_engine, Column, Integer, String, Date, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()
metadata = MetaData(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    deadline = Column(Date, default=datetime.today(), nullable=False)

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)


def process_input(inp):
    if inp == "0":
        print("Bye!")
        exit()
    elif inp == "1":
        todo_list = session.query(Task).all()
        if todo_list:
            print(f"Today {datetime.today()}:")
            for index, task in enumerate(todo_list):
                print(f'{index+1}. {task}')
        else:
            print("Nothing to do!")
    elif inp == "2":
        for i in range(0, 7, 1):
            today = datetime.today() + timedelta(days=i)
            week_tasks = session.query(Task).filter(Task.deadline == today.date()).all()
            print(f"\n{today.strftime('%A %d %b')}:")
            if week_tasks:
                for index, task in enumerate(week_tasks):
                    print(f"{index + 1}. {task.task}")
            else:
                print("Nothing to do!")
    elif inp == "3":
        print("All tasks:")
        all_tasks = query_all_tasks()
        print_tasks(all_tasks)
    elif inp == "4":
        tasks = session.query(Task).filter(Task.deadline < datetime.today().date()).order_by(Task.deadline).all()
        print("Missed tasks:")
        if tasks:
            print_tasks(tasks)
        else:
            print("All tasks have been completed!")
        print("")
    elif inp == "5":
        task = input("Enter a task")
        deadline = input("Enter a deadline ")
        add_task(task, deadline)
        print("The task has been added!")
    elif inp == "6":
        print("Choose the number of the task you want to delete:")
        all_tasks = query_all_tasks()
        print_tasks(all_tasks)
        inp = input()
        session.delete(all_tasks[int(inp) - 1])
        session.commit()
        print("The task has been deleted!")


def query_all_tasks():
    all_tasks = session.query(Task).order_by(Task.deadline).all()
    return all_tasks

def print_tasks(tasks):
    for index, task in enumerate(tasks):
        print(f"{index + 1}. {task}. {task.deadline.strftime('%e %b').strip()}")

def add_task(task, deadline):
    task = Task(task=task, deadline=datetime.strptime(deadline, "%Y-%m-%d"))
    session.add(task)
    session.commit()


menu = "1) Today's tasks", "2) Week's tasks", "3) All tasks", "4) Missed tasks", "5) Add a task", "6) Delete a task", "0) Exit"
while True:
    for task in menu:
        print(f'{task}')
    inp = input()
    process_input(inp)
