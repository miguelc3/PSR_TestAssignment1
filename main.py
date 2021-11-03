#!/usr/bin/python3

# Import packages
from colorama import Fore, Style
import argparse
import random
import string
import time
import readchar
from pprint import pprint
from collections import namedtuple

# Named tuple to use for saving all the inputs
inputs = namedtuple('inputs', ['requested', 'received', 'duration'])

# Global variables
random_letters = []
pressed_keys = []
types = []
duration_types = []


def time_mode(t):
    # This is the time mode

    # Variables to count the number of types and hits
    total_hits = 0
    total_types = 0
    print('Test running up to ' + str(t) + ' seconds')
    print('Press any key to start')
    # The user will press any key to make the test start, this key will not be saved for the statistics
    readchar.readkey()

    print(Fore.LIGHTMAGENTA_EX + 'Press space if you want to exit' + Style.RESET_ALL)
    initial_time = time.time()  # Used to save test start time

    total_duration = 0
    while True:
        random_letter = random.choice(string.ascii_lowercase)
        random_letters.append(random_letter)
        print('Please type ' + Fore.BLUE + random_letter + Style.RESET_ALL)
        # save the time so that, later, it is possible to calculate how long it took to press the key
        start_time = time.time()

        # Read the typed key and save it in the respective list
        pressed_key = readchar.readkey()
        pressed_keys.append(pressed_key)
        # Save the time, calculate the type duration and append it to the respective list
        final_time = time.time()
        duration_type = final_time - start_time
        duration_types.append(duration_type)

        # Update the total duration of the test
        total_duration += duration_type

        # Break cycle if total duration > test duration
        if total_duration > t:
            print("Current test duration (" + str(round(total_duration, 3)) + ') exceeds maximum of ' + str(t))
            break

        # Exit if the user presses space
        if pressed_key == ' ':
            print(Fore.RED + 'You pressed space to exit!' + Style.RESET_ALL)
            exit(0)

        # Verify if the pressed key was the correct one, or not
        if random_letter == pressed_key:
            # Hit -> add one to the counter of total hits
            total_hits += 1
            print('You typed ' + Fore.GREEN + pressed_key + Style.RESET_ALL)
        else:
            # Miss
            print('You typed ' + Fore.RED + pressed_key + Style.RESET_ALL)

        # Update the total number of types
        total_types += 1

        # Save the result and append it to the list 'Types'
        result = inputs(requested=random_letter, received=pressed_key, duration=round(duration_type, 3))
        types.append(result)

    print(Fore.BLUE + 'Test finished!' + Style.RESET_ALL)

    # Calculate the average type duration, with the test time (t) and the number of types
    type_average_duration = total_duration / total_types

    # For cycle to sum the total time on hit and miss types
    total_hits_time = 0
    total_miss_time = 0
    for i in range(0, len(pressed_keys)):
        if pressed_keys[i] == random_letters[i]:
            total_hits_time += duration_types[i]
        else:
            total_miss_time += duration_types[i]

    # Calculate average miss and hit duration -> time lost on hits/number of hits (the same for miss)
    total_miss = total_types - total_hits
    if total_hits == 0:
        type_hit_average_duration = 0
    else:
        type_hit_average_duration = total_hits_time / total_hits

    if total_miss == 0:
        type_miss_average_duration = 0
    else:
        type_miss_average_duration = total_miss_time/total_miss

    # Percentage of accuracy
    accuracy = total_hits/(len(pressed_keys)-1)*100

    # Saving all the statistics in a dictionary and print it
    dict_results = {'Accuracy': str(accuracy) + '%',
                    'Inputs': types,
                    'Number of hits': total_hits,
                    'Number of types': total_types,
                    'Test duration': str(round(total_duration, 3)) + 's',
                    'Test end': time.ctime(final_time),
                    'Test start': time.ctime(initial_time),
                    'Type average duration': round(type_average_duration, 3),
                    'Type hit average duration': round(type_hit_average_duration, 3),
                    'Type miss average duration': round(type_miss_average_duration, 3)
                    }
    pprint(dict_results)


def max_inputs(n):
    # This is the maximum number of inputs mode

    print('Test running up to ' + str(n) + ' inputs.')

    # Initialize variables
    total_hits = 0
    total_types = 0

    # The program starts after any key is pressed
    print('Press any key to start')
    readchar.readkey()

    print(Fore.LIGHTMAGENTA_EX + 'Press space if you want to exit' + Style.RESET_ALL)
    initial_time = time.time()  # Used to save test start time

    # The program will run n times - required by the user
    for total_types in range(0, n):

        # Save the initial time each time to then calculate the type duration
        start_time = time.time()
        # Generate a random letter and save it
        random_letter = random.choice(string.ascii_lowercase)
        random_letters.append(random_letter)

        # read the pressed key and add it to the list
        print('Please type ' + Fore.BLUE + random_letter + Style.RESET_ALL)
        pressed_key = readchar.readkey()
        pressed_keys.append(pressed_key)

        # Exit if the user presses space
        if pressed_key == ' ':
            print(Fore.RED + 'You pressed space to exit!' + Style.RESET_ALL)
            exit(0)

        # save the time and calculate type duration
        final_time = time.time()
        duration_type = final_time - start_time
        duration_types.append(duration_type)

        # Increment the total number of types
        total_types += 1

        # Verify if the type was correct
        if pressed_key == random_letter:
            # Hit -> Increment the total_hits counter
            total_hits += 1
            print('You typed ' + Fore.GREEN + pressed_key + Style.RESET_ALL)
        else:
            # Miss
            print('You typed ' + Fore.RED + pressed_key + Style.RESET_ALL)

        # Save the result and append it ro the list 'Types'
        result = inputs(requested=random_letter, received=pressed_key, duration=round(duration_type, 3))
        types.append(result)

    # Calculate the total duration of the test
    total_duration = final_time - initial_time
    print('Maximum number of inputs reached.' + Fore.BLUE + 'Test finished!' + Style.RESET_ALL)

    # Calculate average type duration
    type_average_duration = total_duration / n

    # For cycle to sum the total time on hit and miss types
    total_hits_time = 0
    total_miss_time = 0
    for i in range(0, len(pressed_keys)):
        if pressed_keys[i] == random_letters[i]:
            total_hits_time += duration_types[i]
        else:
            total_miss_time += duration_types[i]

    # Calculate average miss and hit duration -> time lost on hits/number of hits (the same for miss)
    total_miss = n - total_hits
    if total_hits == 0:
        type_hit_average_duration = 0
    else:
        type_hit_average_duration = total_hits_time / total_hits

    if total_miss == 0:
        type_miss_average_duration = 0
    else:
        type_miss_average_duration = total_miss_time / total_miss

    # Percentage of accuracy
    accuracy = total_hits/len(pressed_keys)*100

    # Saving all the statistics in a dictionary and print it
    dict_results = {'Accuracy': str(accuracy) + '%',
                    'Inputs': types,
                    'Number of hits': total_hits,
                    'Number of types': total_types,
                    'Test duration': str(round(total_duration, 3)) + 's',
                    'Test end': time.ctime(final_time),
                    'Test start': time.ctime(initial_time),
                    'Type average duration': round(type_average_duration, 3),
                    'Type hit average duration': round(type_hit_average_duration, 3),
                    'Type miss average duration': round(type_miss_average_duration, 3)
                    }
    pprint(dict_results)


def main():

    # Create a argparser and add arguments for time mode and max value mode
    parser = argparse.ArgumentParser(description='Definition of ' + Fore.LIGHTBLUE_EX + 'test '
                                                 + Style.RESET_ALL + 'mode')
    parser.add_argument('-utm', '--use_time_mode', action='store_true', help='Max number of secs for time mode '
                        'or maximum number of inputs for number of inputs mode.')
    parser.add_argument('-mv', '--max_value', type=int, required=False,
                        help='Max number of secs for time mode or maximum number of inputs for number of inputs mode.')
    args = vars(parser.parse_args())

    if args['max_value'] == None:
        print(Fore.RED + 'Impossible to start. You need to introduce a maximum value.' + Style.RESET_ALL)
        exit(0)

    # Redirect the code to the right function
    if args['use_time_mode'] is True:
        # Use time mode
        time_mode(args['max_value'])
    else:
        # Use max inputs mode
        max_inputs(args['max_value'])


if __name__ == '__main__':
    main()
