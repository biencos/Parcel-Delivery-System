import sys
import actions as ac


def main():
    print('\n')
    print('Postman Courier App')
    print('')
    print('Press:')
    print('1 - for login')
    print('2 - for register')
    print('3 - for exit')
    option = read_options(input("Option: "), 1, 3)

    if option == 1:
        # TODO
        pass
    if option == 2:
        ac.start_register()
        print('Press:')
        print('1 - for login')
        print('2 - for exit')
        option = read_options(input("Option: "), 1, 2)
        if option == 1:
            # TODO
            pass
        if option == 2:
            print('\nSee you next time')
            sys.exit(0)
    else:
        print('\nSee you next time')
        sys.exit(0)

    print('\nSee you next time')


def read_options(inp, input_limit, input_limit1):
    try:
        inp = int(inp)
    except ValueError:
        print(
            f'Option must be a number between {input_limit} and {input_limit1}\n')
        sys.exit(0)
    if inp < input_limit or inp > input_limit1:
        print(
            f'Option must be a number between {input_limit} and {input_limit1}\n')
        sys.exit(0)
    return inp


if __name__ == "__main__":
    main()
