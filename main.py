#!/usr/bin/python3

# Import packages
from colorama import Fore, Style
import argparse
import random
import string
import time
import readchar
from pprint import pprint
from interruptingcow import timeout  # install this package


parser = argparse.ArgumentParser(description='Definition of ' + Fore.LIGHTBLUE_EX + 'test ' + Style.RESET_ALL + 'mode')
parser.add_argument('-utm', '--use_time_mode', action='store_true', help='')
parser.add_argument('-mv', '--max_value', type=int, required=False, help='Max number of secs for time mode or maximum number of inputs for number of inputs mode.')
args = vars(parser.parse_args())


random_letters = []
pressed_keys = []
types = []
duration_types = []


def time_mode():
    # This is the time mode
    initial_time = time.time()  # Used to save test start time
    # Variables to count the number of types and hits
    total_hits = 0
    total_types = 0
    print('Test running up to ' + str(args['max_value']) + ' seconds')
    print('Press any key to start')
    # The user will press any key to make the test start, this key will not be saved for the statistics
    readchar.readkey()

    # try statement will keep running the while cycle until the time test (chosen by the user - args['max_value']) finishes
    try:
        with timeout(args['max_value'], exception=RuntimeError):
            while True:
                random_letter = random.choice(string.ascii_lowercase)
                random_letters.append(random_letter)
                print('Please type ' + Fore.BLUE + random_letter + Style.RESET_ALL)
                # save the time so that, later, its possible to calculate how long it took to press the key
                start_time = time.time()

                # Read the typed key and save it in the respective list
                pressed_key = readchar.readkey()
                pressed_keys.append(pressed_key)
                # Save the time, calculate the type duration and append it to the respective list
                final_time = time.time()
                duration_type = final_time - start_time
                duration_types.append(duration_type)

                # Verify if the pressed key was the correct one, or not
                if random_letter == pressed_key:
                    # Hit -> add one to the counter of total hits
                    total_hits += 1
                    print('You typed ' + Fore.GREEN + pressed_key + Style.RESET_ALL)
                else:
                    # Miss
                    print('You typed ' + Fore.RED + pressed_key + Style.RESET_ALL)

                # Update thw total number of types
                total_types += 1

                # Save the result and append it ro the list 'Types'
                result = 'Input( requested=' + random_letter + ', received=' + pressed_key + \
                    ', duration= ' + str(duration_type) + ')'
                types.append(result)

    # After the time is over, print a message and break the while cycle
    except RuntimeError:
        print("Your time is over.")
        print(Fore.BLUE + 'Test finished!' + Style.RESET_ALL)
        pass

    # Calculate the average type duration, with the test time (args['max_value']) and the number of types
    type_average_duration = (args['max_value'])/total_types

    # For cycle to sum the total time on hit and miss types
    total_hits_time = 0
    total_miss_time = 0
    for i in range(0, len(pressed_keys)):
        if pressed_keys[i] == random_letters[i]:
            total_hits_time += duration_types[i]
        else:
            total_miss_time += duration_types[i]

    # Clculate average miss and hit duration -> time lost on hits/number of hits (the same for miss)
    total_miss = total_types - total_hits
    type_hit_average_duration = total_hits_time/total_hits
    type_miss_average_duration = total_miss_time/total_miss

    # Percentage of accuraty
    accuracy = total_hits/len(pressed_keys)*100

    # Saving all the statistics in a dictionary and print it
    dict_results = {'Accuracy': str(accuracy) + '%',
                    'Inputs': types,
                    'Number of hits': total_hits,
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
    # This is tha maximum nunber of inputs mode

    initial_time = time.time()
    print('Test running up to ' + str(args['max_value']) + ' inputs.')
    print('Press any key yo start')
    total_hits = 0
    total_types = 0
    max_nletters = args['max_value']

    start_key = readchar.readkey()
    if start_key:
        counter = 0
        while True:
            start_time = time.time()
            random_letter = random.choice(string.ascii_lowercase)
            random_letters.append(random_letter)

            print('Please type ' + Fore.BLUE + random_letter + Style.RESET_ALL)

            pressed_key = readchar.readkey()
            pressed_keys.append(pressed_key)
            final_time = time.time()

            if pressed_key == random_letter:
                counter += 1
                total_hits += 1
                print('You typed ' + Fore.GREEN + pressed_key + Style.RESET_ALL)
            else:
                counter += 1
                print('You typed ' + Fore.RED + pressed_key + Style.RESET_ALL)
            if counter == max_nletters:
                break

            total_types += 1

            duration_type = final_time - start_time
            duration_types.append(duration_type)
            total_duration = final_time - initial_time

            result = 'Input( requested=' + random_letter + ', received=' + pressed_key + \
            ', duration= ' + str(duration_type) + ')'
            types.append(result)
        print('Maximum number of inputs reached.' + Fore.BLUE + 'Test finished!' + Style.RESET_ALL)

    type_average_duration = (args['max_value'])/total_types

    total_hits_time = 0
    total_miss_time = 0
    for i in range(0, len(pressed_keys)-1):
        if pressed_keys[i] == random_letters[i]:
            total_hits_time += duration_types[i]
        else:
            total_miss_time += duration_types[i]

    total_miss = total_types-total_hits
    type_hit_average_duration = total_hits_time/(total_hits or not total_hits)
    type_miss_average_duration = total_miss_time/(total_miss or not total_miss)

    accuracy = total_hits/len(pressed_keys)*100
    dict_results = {'Accuracy': str(accuracy) + '%',
                    'Inputs': types,
                    'Number of hits': total_hits,
                    'Number of types': total_types,
                    'Test duration': str(total_duration) + 's',
                    'Test end': time.ctime(final_time),
                    'Test start': time.ctime(initial_time),
                    'Type average duration': type_average_duration,
                    'Type hit average duration': type_hit_average_duration,
                    'Type miss average duration': type_miss_average_duration
                    }

    pprint(dict_results)

def main():

    if args['use_time_mode'] is True:
        time_mode()
    else:
        max_inputs()

if __name__ == '__main__':
    main()
