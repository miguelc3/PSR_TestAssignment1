#!/usr/bin/python3

# Import packages
from colorama import Fore, Style
import argparse
import random
import string
import time
import readchar
from pprint import pprint
from interruptingcow import timeout # install this package


def time_mode(t):

    random_letters = []
    pressed_keys = []
    types = []
    duration_types = []

    initial_time = time.time()
    total_hits = 0
    total_types = 0

    print('Test running up to ' + str(t) + ' seconds')
    print('Press any key yo start')
    readchar.readkey()

    try:
        with timeout(t, exception=RuntimeError):
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
        print("You're time is over.")
        pass

    type_average_duration = t/total_types

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
                    'Test duration': str(t) + 's',
                    'Test end': time.ctime(final_time),
                    'Test start': time.ctime(initial_time),
                    'Type average duration': type_average_duration,
                    'Type hit average duration': type_hit_average_duration,
                    'Type miss average duration': type_miss_average_duration
                    }

    pprint(dict_results)


def main():
    time_mode(10)


if __name__ == '__main__':
    main()
