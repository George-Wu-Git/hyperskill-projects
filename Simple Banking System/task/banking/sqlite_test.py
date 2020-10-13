import sqlite3

conn = sqlite3.connect(':memory:')

cur = conn.cursor()

with conn:
    cur.execute("""
    CREATE TABLE card (
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0
    )
    """)

card1 = [0, '4000123', '0000', 200]
card2 = [1, '4001456', '1000', 10]
card3 = [2, '4002789', '2000', 1000]
card4 = [3, '4003124', '5010', 10000]


def update(card):
    with conn:
        cur.execute("INSERT INTO card(id, number, pin, balance) VALUES (:id, :number, :pin, :balance)",
                    {'id': card[0], 'number': card[1], 'pin': card[2], 'balance': card[3]})


def balance(number):
    with conn:
        cur.execute("SELECT balance FROM card WHERE number = ?", (number,))
        return cur.fetchone()


def deposit(card):
    deposit = int(input('Enter income:'))
    card[3] += deposit
    query = "UPDATE card SET balance = :balance WHERE number = :number"
    with conn:
        cur.execute(query, {'balance': card[3], 'number': card[1]})

    # print(card[3])
    print('Income was added!')


def get_check_sum(account_number):
    num_sum = sum(int(c) if i % 2 != 0 else
                  2 * int(c) if int(c) < 5 else
                  2 * int(c) - 9
                  for i, c in enumerate(account_number))

    if num_sum % 10 == 0:
        return '0'
    else:
        return str(10 - num_sum % 10)


def transfer(number):
    transfer_to = input('Transfer\nEnter card number:')

    account_numbers = cur.execute("SELECT number FROM card")
    account_numbers = (list(i[0] for i in account_numbers))

    print(account_numbers)

    if transfer_to[-1] != get_check_sum(transfer_to[:-1]):
        print('almost right')

    elif transfer_to not in list(account_numbers):
        # print('wrong number')
        # for account in account_numbers:
        #     if transfer_to[:-1] == account[:-1]:
        #         print('almost right')
        #         return
        # else:
        print('completely wrong')

    else:
        print('right nunmber')
        if transfer_to == number[1]:
            print('error, same account')
        else:
            # transfer_amount = int(input('Enter how much money you want to transfer:'))
            transfer_amount = 400
            print(balance[1])
            print(transfer_amount)
            if transfer_amount > balance[1]:
                print('not enough money')
            else:
                print('money transfered')

    # for account in account_numbers:
    #     if transfer_to not in account:
    #         print(transfer_to[:-1])
    #         print(account[1][:-1])
    #         if transfer_to[:-1] == account[1][:-1]:
    #             print('Probably you made a mistake in the card number. Please try again!')
    #     else:
    #         print('Such a card does not exist.')
    #
    # else:
    #     transfer_amount = int(input('Enter how much money you want to transfer:'))
    #     number[3] -= transfer_amount
    #     transfer_to_balance = balance(transfer_to)[0]
    #     transfer_to_balance += transfer_amount
    #     print(transfer_to_balance)
    #
    # with conn:
    #     query = "UPDATE card SET balance = :balance WHERE number = :number"
    #     cur.execute(query, {'balance': number[3], 'number': number[1]})
    #     cur.execute(query, {'balance': transfer_to_balance, 'number': transfer_to})


def login():
    input_card_number = input('Enter your card number:')
    input_pin = input('Enter your PIN:')

    bank_list = cur.execute("SELECT * FROM card")

    for lst in bank_list:
        if input_card_number in lst and input_pin in lst:
            print('You have successfully logged in!')
            break
    else:
        print('Wrong card number or PIN!')
        # self.account_menu()


def close_account():
    pass


def show_all():
    cur.execute("SELECT * FROM card")
    print(cur.fetchall())


def delete_account():
    query = 'DELETE FROM card WHERE number = :number'


update(card1)
update(card2)
update(card3)
update(card4)
transfer(card1)
balance(card2[1])
# show_all()
