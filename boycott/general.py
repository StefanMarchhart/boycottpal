from uszipcode import ZipcodeSearchEngine


def suffix(d):
    return 'th' if 11 <= d <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')


def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

def process_zip(zipcode):
    if zipcode == "":
        location = " "
    else:
        search = ZipcodeSearchEngine()
        location = search.by_zipcode(zipcode)

        location = "(" + str(location.City) + ", " + str(location.State) + ")"
    return location

