import random
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


class SimpleBankingSystem:
    def __init__(self):
        self.card_number = ''
        self.pin = ''
        self.balance = 0
        pass

    def create_account(self):
        # generate card number
        issuer_identification_number = '400000'

        customer_account_number = random.sample(range(10), 9)
        customer_account_number = ''.join(map(str, customer_account_number))

        check_digit_number = self.get_check_sum(issuer_identification_number + customer_account_number)
        self.card_number = issuer_identification_number + customer_account_number + check_digit_number
        return self.card_number

    @staticmethod
    def update(id, number, pin, balance):
        with conn:
            cur.execute("INSERT INTO card(id, number, pin, balance) VALUES (?, ?, ?, ?)", (id, number, pin, balance))

    def create_pin(self):
        # generate pin
        pin = random.sample(range(10), 4)
        self.pin = ''.join(map(str, pin))
        return self.pin

    def login(self):
        input_card_number = input('Enter your card number:')
        input_pin = input('Enter your PIN:')
        bank_list = cur.execute("SELECT * FROM card")

        for lst in bank_list:
            if input_card_number in lst and input_pin in lst:
                print('You have successfully logged in!')
                self.card_number = input_card_number
                pin = cur.execute('SELECT pin FROM card WHERE number = :number', {'number': self.card_number})
                self.pin = (list(pin)[0][0])
                balance = cur.execute('SELECT balance FROM card WHERE number = :number', {'number': self.card_number})
                self.balance = int(list(balance)[0][0])
                return self.account_menu()
        else:
            print('Wrong card number or PIN!')
            return self.start_menu()

    @staticmethod
    def show_balance(number):
        cur.execute("SELECT balance FROM card WHERE number = ?", (number,))
        return cur.fetchone()[0]
        # print(cur.fetchall())

    def deposit(self):
        deposit = int(input('Enter income:'))
        self.balance += deposit
        query = "UPDATE card SET balance = :balance WHERE number = :number"
        with conn:
            cur.execute(query, {'balance': self.balance, 'number': self.card_number})

        print('Income was added!')

    def transfer(self):
        transfer_to = input('Transfer\nEnter card number:')

        account_numbers = cur.execute("SELECT number FROM card")
        account_numbers = (list(i[0] for i in account_numbers))

        # print(account_numbers)
        if transfer_to[-1] != self.get_check_sum(transfer_to[:-1]):
            print('Probably you made a mistake in the card number. Please try again!')

        elif transfer_to not in list(account_numbers):
            print('Such a card does not exist.')
        else:
            if transfer_to == self.card_number:
                print("You can't transfer money to the same account!")
            else:
                transfer_amount = int(input('Enter how much money you want to transfer:'))
                if transfer_amount > self.balance:
                    print(self.balance)
                    print('Not enough money!')
                else:
                    self.balance -= transfer_amount

                    transfer_to_balance = self.show_balance(transfer_to)
                    transfer_to_balance += transfer_amount
                    print(transfer_to_balance)

                    with conn:
                        query = "UPDATE card SET balance = :balance WHERE number = :number"
                        cur.execute(query, {'balance': self.balance, 'number': self.card_number})
                        cur.execute(query, {'balance': transfer_to_balance, 'number': transfer_to})

    def delete_account(self):
        query = 'DELETE FROM card WHERE number = :number'
        with conn:
            cur.execute(query, {'number': self.card_number})
        return self.start_menu()

    @staticmethod
    def get_check_sum(account_number):
        num_sum = sum(int(c) if i % 2 != 0 else
                      2 * int(c) if int(c) < 5 else
                      2 * int(c) - 9
                      for i, c in enumerate(account_number))

        if num_sum % 10 == 0:
            return '0'
        else:
            return str(10 - num_sum % 10)

    def start_menu(self):
        while True:
            command = input('1. Create an account\n2. Log into account\n0. Exit')
            if command == '1':
                print(f'Your card number:\n{self.create_account()}')
                print(f'Your card PIN:\n{self.create_pin()}')
                self.update('', self.card_number, self.pin, self.balance)
            elif command == '2':
                self.login()

            elif command == '3':
                self.show_all()
            elif command == '0':
                exit()

    def account_menu(self):
        while True:
            command = input("""
1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit""")
            if command == '1':
                # print(self.card_number)
                print(f'Balance: {self.show_balance(self.card_number)}')
            elif command == '2':
                self.deposit()
            elif command == '3':
                self.transfer()
            elif command == '4':
                self.delete_account()
            elif command == '5':
                print('You have successfully logged out!')
                return self.start_menu()
            elif command == '0':
                print('Bye')
                exit()

    @staticmethod
    def show_all():
        cur.execute("SELECT * FROM card")
        print(cur.fetchall())


SimpleBankingSystem().start_menu()
