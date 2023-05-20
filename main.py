from handler import hello, add, change, phone, show, contacts, iterator, birthday, search

exit_command = ['goodbye', 'close', 'exit', '.']

dict_of_commands = {'add': add,
                    'change': change,
                    'phone': phone,
                    'hello': hello,
                    'show': show,
                    'iterator': iterator,
                    'birthday': birthday,
                    'search': search}


while True:
    command, *date = input('Enter command: ').strip().split(' ', 1)
    command = command.lower()

    if command in exit_command:
        contacts.serialize()
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
