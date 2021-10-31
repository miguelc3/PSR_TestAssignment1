#!/usr/bin/python3

# Import packages
from colorama import Fore, Style, Back
import argparse
import random
import string
import time
import readchar
from pprint import pprint
from interruptingcow import timeout # install this package


parser = argparse.ArgumentParser(description='Definition of ' + Fore.LIGHTBLUE_EX + 'test ' + Style.RESET_ALL + 'mode')
parser.add_argument('-utm', '--use_time_mode', action='store_true', help='')
parser.add_argument('-mv', '--max_value', type=int, required=False, help=' Max number of secs for time mode or maximum number of inputs for number of inputs mode.')
args = vars(parser.parse_args())

#print('Welcome to our typing test!\nPress any key to start the test.')

random_letters = []
pressed_keys = []
types = []
duration_types = []


def time_mode():
    initial_time = time.time()
    total_hits = 0
    total_types = 0
    print('Test running up to ' + str(args['max_value']) + ' seconds')
    print('Press any key yo start')
    readchar.readkey()

    try:
        with timeout(args['max_value'], exception=RuntimeError):
            while True:
                start_time = time.time()

                random_letter = random.choice(string.ascii_lowercase)
                random_letters.append(random_letter)
                print('Please type ' + Fore.BLUE + random_letter + Style.RESET_ALL)

                pressed_key = readchar.readkey()
                pressed_keys.append(pressed_key)
                final_time = time.time()

                if random_letter == pressed_key:
                    total_hits += 1
                    print('You typed ' + Fore.GREEN + pressed_key + Style.RESET_ALL)
                else:
                    print('You typed ' + Fore.RED + pressed_key + Style.RESET_ALL)
                total_types += 1

                duration_type = final_time - start_time
                duration_types.append(duration_type)
                total_duration = final_time - initial_time

                result = 'Input( requested=' + random_letter + ', received=' + pressed_key + \
                    ', duration= ' + str(duration_type) + ')'
                types.append(result)

    except RuntimeError:
        print("Your time is over.")
        pass

    type_average_duration = (args['max_value'])/total_types

    total_hits_time = 0
    total_miss_time = 0
    for i in range(0, len(pressed_keys)):
        if pressed_keys[i] == random_letters[i]:
            total_hits_time += duration_types[i]
        else:
            total_miss_time += duration_types[i]

    total_miss = total_types-total_hits
    type_hit_average_duration = total_hits_time/total_hits
    type_miss_average_duration = total_miss_time/total_miss

    accuracy = total_hits/len(pressed_keys)*100
    dict_results = {'Accuracy': str(accuracy) + '%',
                    'Inputs': types,
                    'Number of hints': total_hits,
                    'Number of types': total_types,
                    'Test duration': str(args['max_value']) + 's',
                    'Test end': time.ctime(final_time),
                    'Test start': time.ctime(initial_time),
                    'Type average duration': type_average_duration,
                    'Type hit average duration': type_hit_average_duration,
                    'Type miss average duration': type_miss_average_duration
                    }

    pprint(dict_results)

def max_inputs():
    max_nletters = args['max_value']
    start_key = readchar.readkey()
    if start_key:
        counter = 0
        while True:
            random_letter = random.choice(string.ascii_lowercase)
            random_letters.append(random_letter)
            print('Type ' + Back.LIGHTRED_EX + str(random_letter) + Style.RESET_ALL)
            pressed_key = readchar.readkey()
            if pressed_key == random_letter:
                counter += 1
                print('You typed ' + pressed_key + Fore.LIGHTGREEN_EX + ' -->RIGHT' + Style.RESET_ALL)
            else:
                counter += 1
                print('You typed ' + pressed_key + Fore.RED + ' -->WRONG' + Style.RESET_ALL)
            if counter==max_nletters:
                break

def main():

    if args['use_time_mode'] is True:
        time_mode()
    else:
        max_inputs()

if __name__ == '__main__':
    main()
