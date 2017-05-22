def read(path):
    with open(path, 'r') as file:
        return file.read()

def read_lines(path):
    with open(path, 'r') as file:
        return file.read_lines()

def read_binary(path):
    with open(path, 'rb') as file:
        return file.read()

def write(path, text):
    with open(path, 'w') as file:
        file.write(text)
