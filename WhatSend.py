import pywhatkit


def sendwtsp(phone, message):
    pywhatkit.sendwhatmsg_instantly(phone, message, tab_close=True, close_time=0)

