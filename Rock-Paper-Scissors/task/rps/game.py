import random


class RockPaperScissors:

    def __init__(self, name, score, rule):
        self.name = name
        self.score = score
        self.rule = rule


    def greet(self):
        self.name = input('Enter your name: ')
        print(f'Hello, {self.name}')

    def load_rating(self):
        with open('rating.txt') as rating_file:
            rating = [line.split() for line in rating_file.readlines()]
            rating = {self.name: int(self.score) for self.name, self.score in rating}

        if self.name in rating:
            self.score = rating[self.name]
        else:
            self.score = 0

    def ask_for_rule(self):
        rule = input()
        if not rule:
            rule = 'rock, paper, scissors'
            self.rule = rule.split(',')

    def plaer_win_moves(self, option):
        user_index = (self.rule.index(option))
        win_list = self.rule[user_index + 1:] + self.rule[:user_index]
        win_moves = win_list[:(len(self.rule) // 2)]

    def game(self):
        user = input()
        options = {"paper": "rock", "rock": "scissors", "scissors": "paper"}

        while user != "!exit":
            computer = random.choice(["rock", "paper", "scissors"])

            if options[computer] == user:
                print("Sorry, but computer chose {}".format(computer))
            elif user == computer:
                print("There is a draw ({})".format(computer))
                self.score += 50
            elif user in options and options[user] == computer:
                print("Well done. Computer chose {} and failed".format(computer))
                self.score += 100
            elif user == "!rating":
                print("Your rating: {}".format(self.score))
            else:
                print("Invalid input")

            user = input()

        print("Bye!")

    def play(self):
        self.greet()
        self.load_rating()
        self.ask_for_rule()

        option = input()
