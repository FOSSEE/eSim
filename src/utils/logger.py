import logging


class ErrorLogHandler(logging.StreamHandler):
    '''
    Define custom handler for handling multiple arguments
    Logger can now support print(...) like calls without `Format Strings`
    `Emit` function is called to print the logging output
    It takes `record` which has all the data to print, funcName, filename, etc
    Here it takes msg along with arg to parse the msg
    But, since we are passing string in arg to print, we add that to msg
    '''

    def emit(self, record):
        '''this each method called when a log creates '''
        newMessage = [str(record.msg)]
        for i in record.args:
            newMessage.append(str(i))
        record.msg = " ".join(newMessage)
        record.args = ""
        log_entry = self.format(record)
        print(log_entry)


logger = logging.getLogger("esim")
logger.setLevel(logging.DEBUG)

ch = ErrorLogHandler()
# ch = logging.StreamHandler()

ch.setLevel(logging.DEBUG)

FORMAT = "[%(asctime)s][%(filename)s:%(lineno)s - %(funcName)s()] %(message)s"
DTFMT = "%H:%M:%S"
fromatter = logging.Formatter(fmt=FORMAT, datefmt=DTFMT)

ch.setFormatter(fromatter)

logger.addHandler(ch)
