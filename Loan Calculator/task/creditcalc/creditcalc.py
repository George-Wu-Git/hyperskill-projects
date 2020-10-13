import math


class Parameter:
    '''Calculation parameter template.'''
    def __init__(self, value, type_, prompt):
        self.value = value
        self.type_ = type_
        self.prompt = prompt


class CreditCalculator:
    '''Credit calculator is able to work with annual type of payment.'''

    def __init__(self):
        self.main_prompt = 'What do you want to calculate?'
        self.option_prompt = (
            'type "n" - for count of months,\n'
            'type "a" - for annuity monthly payment,\n'
            'type "p" - for credit principal:\n'
        )

        self.parameters = {
            'credit_principal': Parameter(None, int, 'Enter credit principal'),
            'monthly_payment': Parameter(None, float, 'Enter monthly payment'),
            'credit_interest': Parameter(None, float, 'Enter credit interest'),
            'count_of_month': Parameter(None, int, 'Enter count of periods'),
        }

    def run(self):
        print(self.main_prompt)
        option = input(self.option_prompt)

        if option == 'n':  # count of month
            self.get_parameters('credit_principal', 'monthly_payment', 'credit_interest')
            self.print_count_of_month(self.calculate_count_of_month())

        elif option == 'a':  # annuity monthly payment
            self.get_parameters('credit_principal', 'count_of_month', 'credit_interest')
            print(f'Your annuity payment = {self.calculate_monthly_payment()}!')

        elif option == 'p':  # credit principal
            self.get_parameters('monthly_payment', 'count_of_month', 'credit_interest')
            print(f'Your credit principal = {self.calculate_credit_principal()}!')

        else:
            print(f'You enter wrong option: "{option}"')

    def get_parameters(self, *parameter_names):
        '''Get calculation parameters by theirs names from the input.'''
        for p_name in parameter_names:
            p = self.parameters[p_name]
            p.value = p.type_(input(p.prompt + ':\n'))

    def calculate_count_of_month(self):
        '''Calculate count of month for return a credit with annuity payments.'''
        p = self.parameters
        interest_rate = p['credit_interest'].value / (12 * 100)
        count_of_month = math.log(
            (
                p['monthly_payment'].value
                /  # -----------------------divide the top by the bottom-----------------
                (p['monthly_payment'].value - interest_rate * p['credit_principal'].value)
            ),
            1 + interest_rate
        )
        return math.ceil(count_of_month)  # count_of_month

    def calculate_monthly_payment(self):
        '''Calculate monthly payment for return a credit with annuity payments.'''
        p = self.parameters
        interest_rate = p['credit_interest'].value / (12 * 100)
        monthly_payment = p['credit_principal'].value * interest_rate * (1 + interest_rate) ** p['count_of_month'].value
        monthly_payment /= (1 + interest_rate) ** p['count_of_month'].value - 1

        return math.ceil(monthly_payment)

    def calculate_credit_principal(self):
        '''Calculate credit principal for return a credit with annuity payments.'''
        p = self.parameters
        interest_rate = p['credit_interest'].value / (12 * 100)
        credit_principal = p['monthly_payment'].value * ((1 + interest_rate) ** p['count_of_month'].value - 1)
        credit_principal /= interest_rate * (interest_rate + 1) ** p['count_of_month'].value

        return math.floor(credit_principal)

    @staticmethod  # we use a static method when we dont't refer to 'self'
    def print_count_of_month(count_of_month):
        '''Convert number of month to years, months form and print'''
        years, months = int(count_of_month // 12), math.ceil(count_of_month % 12)
        msg = f'You need'
        msg += '' if years == 0 else ' 1 year' if years == 1 else f' {years} years'
        msg += '' if months == 0 else ' and 1 month' if months == 1 else f' {months} months'
        msg += ' to repay this credit!'
        print(msg)


if __name__ == '__main__':

    calc = CreditCalculator()
    calc.run()
