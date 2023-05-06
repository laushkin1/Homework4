from handler import hello, add, change, phone, show, contacts

exit_command = ['goodbye', 'close', 'exit', '.']

dict_of_commands = {'add': add,
                    'change': change,
                    'phone': phone,
                    'hello': hello,
                    'show': show}


while True:
    command, *date = input('Enter command: ').strip().split(' ', 1)
    command = command.lower()

    if command in exit_command:
        print('Good bye!')
        break
    
    elif dict_of_commands.get(command):
        handler = dict_of_commands.get(command)
        if date:
            date = date[0].split(', ')
            print(handler(*date))
        else:
            print(handler())

    else:
        print('Unknown command!')
