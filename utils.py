from color_function import error


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.lower()
    return cmd, args



def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError:
            return error("Give me name and phone please.")

        except KeyError:
            return error("Contact not found.")

        except IndexError:
            return error("Enter name.")

        except AttributeError:
            return error("Something went wrong with the contact data.")

    return inner