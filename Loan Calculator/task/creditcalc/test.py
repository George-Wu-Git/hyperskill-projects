import math


def annuity_payment():
    calculate = input('''What do you want to calculate? 
type "n" for number of monthly payments,
type "a" for annuity monthly payment amount,
type "p" for loan principal:''')

    if calculate == 'n':
        loan_principal = float(input('Enter the loan principal:'))
        monthly_payment = float(input('Enter the monthly payment:'))
        loan_interest = float(input('Enter the loan interest:')) / 100
        nominal_interest_rate = loan_interest / 12
        number_of_months = math.ceil(
            math.log(monthly_payment / (monthly_payment - nominal_interest_rate * loan_principal),
                     1 + nominal_interest_rate))
        # if number_of_months <= 12:
        #     print(f'{number_of_months} months')
        # else:
        #     if number_of_months % 12 == 0:
        #         if number_of_months / 12 == 1:
        #             print(f'1 year')
        #         else:
        #             print(f'{number_of_months // 12} years')
        #     else:
        # print(f'{number_of_months}')
        # print(f'It will take {number_of_months // 12} years and {number_of_months % 12} months to repay this loan!')

        if number_of_months % 12 == 0:
            print(f"You need {number_of_months / 12} years to repay this credit!")
        elif number_of_months < 12:
            print(f'You need {number_of_months} months to repay this credit!')
        else:
            print(f'You need {number_of_months // 12} years and {number_of_months % 12} months to repay this credit!')

        pass
    elif calculate == 'a':
        loan_principal = float(input('Enter the loan principal:'))
        number_of_periods = float(input('Enter the number of periods:'))
        loan_interest = float(input('Enter the loan interest:')) / 100
        nominal_interest_rate = loan_interest / 12

        top = nominal_interest_rate * loan_principal * (nominal_interest_rate + 1) ** number_of_periods
        bottom = (nominal_interest_rate + 1) ** number_of_periods - 1

        print(f'Your monthly payment = {math.ceil(top / bottom)}!')
        pass
    elif calculate == 'p':
        monthly_payment = float(input('Enter the annuity payment:'))
        number_of_months = float(input('Enter the number of periods:'))
        nominal_interest_rate = float(input('Enter the loan interest:')) / (12 * 100)

        loan_principal = monthly_payment / (
                (nominal_interest_rate * math.pow(1 + nominal_interest_rate, number_of_months)) /
                (math.pow(1 + nominal_interest_rate, number_of_months) - 1))

        print(f'Your loan principal = {round(loan_principal)}!')

        pass


annuity_payment()