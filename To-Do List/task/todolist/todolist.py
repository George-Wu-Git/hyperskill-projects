from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# initialising the parent class for a table
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return f"{self.id}. {self.task}"


class ToDoList:

    def __init__(self):
        self.engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.today = datetime.today().date()

    def start_menu(self):
        while True:
            command = input(f"1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n"
                            f"5) Add task\n6) Delete task\n0) Exit\n")
            if command == '1':
                self.today_tasks()
            elif command == '2':
                self.week_tasks()
            elif command == '3':
                self.all_tasks()
            elif command == '4':
                self.missed_tasks()
            elif command == '5':
                self.add_task()
            elif command == '6':
                self.delete_task()
            elif command == '0':
                print('Bye!')
                exit()

    def missed_tasks(self):
        today = datetime.today()
        rows = self.session.query(Table).filter(Table.deadline < today.date()).all()
        print("Missed task:")
        if rows:
            for row in rows:
                print(f"{row}. {row.deadline.strftime('%#d %b')}")
        else:
            print('Nothing is missed!')
        print('')

        pass

    def delete_task(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        if len(rows) == 0:
            print("Nothing to delete")
        else:
            print("Choose the number of the task you want to delete:")
            self.all_tasks()
            task_id = int(input())
            self.session.query(Table).filter(Table.id == task_id).delete()
            self.session.commit()
            print("The task has been deleted!")

    def today_tasks(self):
        today = datetime.today()
        rows = self.session.query(Table).filter(Table.deadline == today.date()).all()
        print(f"Today {today.strftime('%d %b')}:")
        if rows:
            for row in rows:
                print(row)
        else:
            print('Nothing to do')

    def week_tasks(self):
        for day in (datetime.today() + timedelta(n) for n in range(7)):
            rows = self.session.query(Table).filter(Table.deadline == day.date()).all()
            print(f"{day.strftime('%A %d %b')}:")
            if rows:
                for count, task in enumerate(rows, 1):
                    print(f'{count}. {task}\n')
            else:
                print("Nothing to do!\n")

    def all_tasks(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        if rows:
            for row in rows:
                print(f"{row}. {row.deadline.strftime('%#d %b')}")  # Will print value of the string_field
        else:
            print('Nothing to do!')
        pass

    def add_task(self):
        task = input('Enter task')
        time_string = input('Enter deadline')
        deadline = datetime.strptime(time_string, '%Y-%m-%d')

        self.session.add(Table(task=task, deadline=deadline))
        self.session.commit()
        print('The task has been added!')


ToDoList().start_menu()
