MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}


def start_operation(earning):
    while(True):
        choice = input("What would you like to have (espresso/latte/cappuccino): ")
        if choice == "off":
            exit()
        elif choice == "report":
            print(f"Water: {resources.get('water')} ml")
            print(f"Milk: {resources.get('milk')} ml")
            print(f"Coffee: {resources.get('coffee')} g")
            print(f"Money: {earning} USD")
        else:
            water_left = resources.get('water') - MENU[choice]['ingredients']['water']
            if choice.lower() != 'espresso':
                milk_left = resources.get('milk') - MENU[choice]['ingredients']['milk']
            else:
                milk_left = resources.get('milk')
            coffee_left = resources.get('coffee') - MENU[choice]['ingredients']['coffee']
            if water_left <= 0:
                print("Machine low on water. Order cant be fulfilled.")
                exit()
            else:
                resources['water'] = water_left
            if milk_left <= 0:
                print("Machine low on milk. Order cant be fulfilled.")
                exit()
            else:
                resources['milk'] = milk_left
            if coffee_left <= 0:
                print("Machine low on coffee. Order cant be fulfilled.")
                exit()
            else:
                resources['coffee'] = coffee_left
            quarters = int(input("How many quarters?: "))
            dimes = int(input("How many dimes?: "))
            nickles = int(input("How many nickles?: "))
            pennies = int(input("How many pennies?: "))
            total_money = (quarters * .25) + (dimes * .10) + (nickles * .05) + (pennies * 0.01)
            earning = earning + MENU[choice].get('cost')

            balance = total_money - MENU[choice].get('cost')
            if balance < 0:
                print("You entered less money as input, please start again. Current transaction stopped and money refunded")
                start_operation()
            elif balance > 0:
                print("Change: {:0.2f} USD".format(balance))
                print(f"Here is your {choice} ☕")
            else:
                print(f"Here is your {choice} ☕")

earning = 0
start_operation(earning)
