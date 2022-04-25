# -----------------------------------------------------------------------------------------
def get_not_null_str(str):
    if str is None:
        return ""
    else:
        return str
# -----------------------------------------------------------------------------------------
def get_text_between(str, startText, endText):
    startTextPosition = str.find(startText)
    endTextPosition = str.find(endText)
    if startTextPosition > 0 and endTextPosition > 0:
        str = str[startTextPosition+len(startText) : endTextPosition]
    else:
        str = ""
    return str
# -----------------------------------------------------------------------------------------
def trim_left_hidden_symbols(str):
    i=0
    while(len(str) > i and str[i] in ('\f', '\n', '\r', '\t', '\v')):
        i += 1
    return str[i:]
# -----------------------------------------------------------------------------------------
def trim_right_hidden_symbols(str):
    i=len(str)
    while(i > 0 and str[i-1] in ('\f', '\n', '\r', '\t', '\v')):
        i -= 1
    return str[:i]
# -----------------------------------------------------------------------------------------
def trim_hidden_symbols(str):
    return trim_right_hidden_symbols(trim_left_hidden_symbols(str))
# -----------------------------------------------------------------------------------------
