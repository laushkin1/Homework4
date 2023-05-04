from handler import hello, add, change, phone, show_all
import re

exit_command = ['good bye', 'close', 'exit', '.']

dict_of_commands_with_val = {'add': add,
                             'change': change,
                             'phone': phone}

dict_of_commands_without_val = {'hello': hello,
                                'show all': show_all}


def get_handler(func):
    return dict_of_commands_with_val[func]


while True:
    command = input('Enter command: ')
    command = command.strip()
    string_for_name = command
    string_for_name = string_for_name.split(' ')
    command = command.lower()

    if command in exit_command:
        print('Good bye!')
        break

    elif bool(re.search(r'^add |^change |^phone ', command)):
        command = command.split(' ')
        handler = get_handler(command[0])
        try:
            print(handler(string_for_name[1], command[2:]))
        except IndexError:
            print(handler(string_for_name[1]))

    elif command in dict_of_commands_without_val:
        print(dict_of_commands_without_val[command]())

    else:
        print('Unknown command!')

