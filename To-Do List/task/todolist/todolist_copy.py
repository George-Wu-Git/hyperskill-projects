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


class ToDoList:

    def __init__(self):
        self.engine = create_engine('sqlite:///todo.db?check_same_thread=False')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()
        self.today = datetime.today().date()

    def start_menu(self):
        while True:
            command = input(f"1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Add task\n0) Exit\n")
            if command == '1':
                self.today_tasks()
            if command == '2':
                self.week_tasks()
            if command == '3':
                self.all_tasks()
            elif command == '4':
                self.add_task()
            elif command == '0':
                print('Bye!')
                exit()

    def today_tasks(self):
        rows = self.session.query(Table).filter(Table.deadline == self.today).all()
        print(f"Today {self.today.strftime('%d %b')}:")
        if rows:
            for row in rows:
                print(f'{row.id}. {row.task}. {row.deadline}')
        else:

            print('Nothing to do')
        pass

    def week_tasks(self):
        start_date = datetime.today().date()
        end_date = start_date + timedelta(days=7)
        rows = self.session.query(Table).filter(Table.deadline.between(start_date, end_date)).all()
        while start_date < end_date:
            print(f"{start_date.strftime('%A %d %b')}:")
            task_list = list(row.task for row in rows if row.deadline == start_date)
            if task_list:
                for count, task in enumerate(task_list, 1):
                    print(f'{count}. {task}')
            else:
                print("Nothing to do!")

            print('')

            start_date += timedelta(days=1)
        pass

    def all_tasks(self):
        rows = self.session.query(Table).order_by(Table.deadline).all()
        if rows:
            for row in rows:
                row.deadline_format = row.deadline.strftime('%#d %b')
                print(f'{row.id}. {row.task}. {row.deadline_format}')  # Will print value of the string_field
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
