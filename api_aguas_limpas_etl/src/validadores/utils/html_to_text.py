import read

def convert_one_html(path):

    try:
        soup = read.read_html(path)
        text = soup.get_text()
    except TypeError and UnicodeDecodeError:
        return ""

    return text
