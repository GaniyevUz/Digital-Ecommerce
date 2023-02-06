import re


class EmailValidator:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

    def __call__(self, value) -> bool:
        if re.fullmatch(self.regex, value):
            return True
        else:
            return False
