import json
import random
from colorama import Fore, Style
import time

    
def get_player(name):
    with open("players_data.json", "r", encoding='utf-8') as players_data_file:
        data = json.load(players_data_file)

    if data:
        for player in data:
            if player["name"] == name:
                return player
                
    player = {
        "name": name,
        'current_money': 0,
        "total_money": 0,
        "wins": 0,
        "losses": 0,
        "correct_answers": 0,
        "question_list": get_question_list(),
        "current_question": 0,
        "guaranteed_money": 0,
        'hints': {
            "50/50": True,
            "Call": True,
            "Ask": True,
            },
    }

    return player


def save_player(player):
    with open("players_data.json", "r", encoding='utf-8') as players_data_file:
        data = json.load(players_data_file)
    if data:
        for index, p in enumerate(data):
            if p["name"] == player["name"]:
                data[index] = player
                break
        else:
            data.append(player)
    else:
        data.append(player)

    with open("players_data.json", "w", encoding='utf-8') as players_data_file:
        json.dump(data, players_data_file, ensure_ascii=False, indent=4)


def get_question_list():
    with open("questions.json", "r", encoding='utf-8') as questions_file:
        questions = json.load(questions_file)
    
    return random.sample(questions, 15)


def get_current_question(current_question):
    print(current_question['question'])
    print("Варіанти: ")

    for variant, value in current_question['options'].items():
        print(f'{variant}: {value}')

    print("--------------------------")


def get_statistics(player):
    print("--------------------------")
    print("Статистика:")
    print(f"Ім'я: {player['name']}")
    print(f"Виграні ігри: {Fore.GREEN + str(player['wins']) + Style.RESET_ALL}")
    print(f"Програні ігри: {Fore.RED + str(player['losses']) + Style.RESET_ALL}")
    print(f"Правильні відповіді: {Fore.GREEN + str(player['correct_answers']) + Style.RESET_ALL}")
    print(f"Виграно грошей: {Fore.YELLOW + str(player['total_money']) + Style.RESET_ALL}$")
    print("--------------------------")
    time.sleep(5)


def get_instructions():
    print("--------------------------")
    print("Інструкція:")
    print("Гравець відповідає на питання, вибираючи один з варіантів відповідей: A, B, C або D.")
    print("Гравець може використовувати підказки: 50/50, Ask, Call.")
    print("Гравець може вийти з гри в меню, натиснувши '0'.")
    print("Гравець може переглянути статистику в меню або після закінчення гри.")
    print("--------------------------")
    time.sleep(5)


def menu(player):
    while True:
        print("--------------------------")
        print(Fore.YELLOW + "Ласкаво просимо до гри 'Хто хоче стати мільйонером'!" + Style.RESET_ALL)
        print(Fore.YELLOW + f"Вітаємо, {player['name']}!" + Style.RESET_ALL)
        print("Виберіть пункт меню:")
        print("1. Грати")
        print("2. Статистика")
        print("3. Інструкція")
        print("0. Вихід")
        print("--------------------------")

        choice = input("Ваш вибір: ").strip()
        
        match choice:
            case '1':
                game(player)

            case '2':
                get_statistics(player)

            case '3':
                get_instructions()

            case '0':
                return
            
            case _:
                print(Fore.RED + "Невірний вибір! (Можливі варіанти: 1, 2, 3, 0)" + Style.RESET_ALL)
                time.sleep(2)


def get_hint_50_50(allowed, question):
    if allowed:
        allowerd_keys = [key for key in question["options"].keys() if key != question['correct_answer']]
        hint_keys = random.sample(allowerd_keys, 2)
        hint_keys[1] = question['correct_answer']
        question['options'] = {
                hint_keys[0]: question['options'][hint_keys[0]],
                hint_keys[1]: question['options'][hint_keys[1]]
            }
        
        return question
    
    else:
        print(Fore.RED + "Підказка 50/50 вже використана." + Style.RESET_ALL)
        time.sleep(2)

        return  


def get_hint_ask(allowed, question):
    if allowed:
        correct_votes = random.randint(50, 80)
        question['options'][question['correct_answer']] += f" {str(correct_votes)}% "
        wrong_votes = 100 - correct_votes
        for key in question['options'].keys():
            if key != question['correct_answer']:
                question['options'][key] += f" {str(wrong_votes//3)}% "    

        return question
    
    else:
        print(Fore.RED + "Підказка 'Запитати у глядачів' вже використана." + Style.RESET_ALL)
        time.sleep(2)

        return


def get_hint_call(allowed, question):
    if allowed:
        hint_answer = random.choice(list(question['options'].keys()))
        
        print(Fore.CYAN + f"Дякую за дзвінок. я гадаю, що це варіант {hint_answer}" + Style.RESET_ALL)
        question['options'][hint_answer] += ' (порада друга) '
        time.sleep(2)

        return question
    else:
        print(Fore.RED + "Підказка 'Телефонний дзвінок' вже використана." + Style.RESET_ALL)
        time.sleep(2)

        return
    

def game(player):
    if not player['question_list']:
        player['question_list'] = get_question_list()

    questions_money = {
        1: 100,
        2: 200,
        3: 300,
        4: 500,
        5: 1000,
        6: 2000,
        7: 4000,
        8: 8000,
        9: 16000,
        10: 32000,
        11: 64000,
        12: 125000,
        13: 250000,
        14: 500000,
        15: 1000000,
    }

    guaranteed_money = (5, 10, 15)

    if player['current_question'] >= 1 or len(player['question_list']) < 15:
        ask_to_continue = input("Ви вже грали. Продовжити гру (відмова вважатиметься програшем)?  (так/ні): ").strip().lower()

        if ask_to_continue == "ні":
            player['current_question'] = 0
            player['current_money'] = 0
            player['question_list'] = get_question_list()

            for hint in player['hints']:
                player['hints'][hint] = True

            player['guaranteed_money'] = 0
            player['losses'] += 1

    while len(player['question_list']) > 0:
        question = player['question_list'][0]
        print("--------------------------")
        print(f"Питання {player['current_question'] + 1} на {Fore.YELLOW + str(questions_money[player['current_question'] + 1]) + Style.RESET_ALL}$:")
        get_current_question(question)

        answer = input("Ваша відповідь: ").capitalize()

        match answer:

            case '0':
                save_player(player)

                return
            
            case '50/50':
                question = get_hint_50_50(player['hints']['50/50'], question)

                if question:
                    player['question_list'][0] = question
                    player['hints']['50/50'] = False

                continue

            case 'Ask':
                question = get_hint_ask(player['hints']['Ask'], question)

                if question:
                    player['question_list'][0] = question
                    player['hints']['Ask'] = False

                continue

            case 'Call':
                question = get_hint_call(player['hints']['Call'], question)

                if question:
                    player['question_list'][0] = question
                    player['hints']['Call'] = False

                continue

            case 'A' | 'B' | 'C' | 'D':
                if answer == question['correct_answer']:
                    player['current_question'] += 1
                    print("--------------------------")
                    print(Fore.GREEN + "Правильно!" + Style.RESET_ALL)
                    player['current_money'] = questions_money[player['current_question']]
                    print(f"Ваш виграш: {Fore.YELLOW + str(player['current_money']) + Style.RESET_ALL}$")

                    if player['current_question'] in guaranteed_money:
                        player['guaranteed_money'] = questions_money[player['current_question']]
                        
                    if player['guaranteed_money']:
                        print(f"Ваша гарантована сума: {Fore.YELLOW + str(player['guaranteed_money']) + Style.RESET_ALL}$")

                    print("--------------------------")
                    time.sleep(3)
                    player['correct_answers'] += 1
                    del player['question_list'][0]

                    continue

                else:
                    player['total_money'] += player['guaranteed_money']
                    print(Fore.RED + "Неправильно!" + Style.RESET_ALL)
                    print(Fore.RED + "Гра закінчена!" + Style.RESET_ALL)
                    print(f'Ви виграли {Fore.YELLOW + str(player["guaranteed_money"]) + Style.RESET_ALL}$')
                    player['losses'] += 1
                    player['current_question'] = 0
                    player['current_money'] = 0
                    player['guaranteed_money'] = 0
                    player['question_list'] = []

                    for hint in player['hints']:
                        player['hints'][hint] = True

                    time.sleep(4)
                    save_player(player)
                    get_statistics(player)
                    return
            case _:
                print(Fore.RED + "Неправильний варіант! (Можливі варіанти: А, B, C, D, 50/50, Ask, Call, 0)" + Style.RESET_ALL)
                time.sleep(2)
                continue

    player['total_money'] += player['guaranteed_money']    
    player['wins'] += 1
    player['current_question'] = 0
    player['current_money'] = 0

    for hint in player['hints']:
        player['hints'][hint] = True

    player['guaranteed_money'] = 0
    player['question_list'] = []
    print(f"Вітаємо! Ви виграли " + Fore.YELLOW + "1000000" + Style.RESET_ALL + "$ !!!")
    time.sleep(3)

    get_statistics(player)
    save_player(player)


def main():
    name = input("Введіть ваше ім'я: ")
    player = get_player(name)
    menu(player)


main()