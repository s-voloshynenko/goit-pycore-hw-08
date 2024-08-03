class NotValidPhoneNumberError(Exception):
    def __init__(self, message="Wrong phone number"):
        self.message = message
        super().__init__(self.message)

class ContactsError(Exception):
    def __init__(self, message="Contact doesn't exist"):
        self.message = message
        super().__init__(self.message)

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return e
        except IndexError as e:
            return e
        except KeyError as e:
            return e
        except NotValidPhoneNumberError as e:
            return e
        except ContactsError as e:
            return e

    return inner

def input_validate_args(params: list):
    def decorator(func):
        def inner(*args, **kwargs):
            if len(args[0]) != len(params):
                raise ValueError(
                    f"Enter the argument for the command. Required arguments: {", ".join(params)}."
                )
            return func(*args, **kwargs)
        return inner
    return decorator
