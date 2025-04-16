def get_or_null(string):
    if string is None or string == '':
        string = 'Non definito'
    else:
        if type(string) == type(True):
            if string:
                string = 'Sì'
            else:
                string = 'No'
    return string