def convertstrtoint(string):
    string = string.strip()
    out = ""
    while not string[0].isdigit():
        string = string[1:]
    while string[0].isdigit():
        out += string[0]
        string = string[1:]
        if len(string) == 0:
            break
    return int(out)
