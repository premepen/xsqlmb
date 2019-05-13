import logging
from fluent import handler

custom_format = {
  'host': '%(hostname)s',
  'where': '%(module)s.%(funcName)s',  #具体到文件、函数
  'type': '%(levelname)s',
  'stack_trace': '%(exc_text)s'
}

logging.basicConfig(level=logging.DEBUG)

l = logging.getLogger('fluent.test')

h = handler.FluentHandler('mongo.test', host='192.168.2.41', port=24224)
formatter = handler.FluentRecordFormatter(custom_format)
h.setFormatter(formatter)

l.addHandler(h)

def funcs():
    l.warning("hello111")
    l.error("hello  error111")

def test2():
    logger = logging.getLogger('fluent.test')
    _handler = handler.FluentHandler('mongo.txt', host='192.168.2.41', port=24224)
    logger.addHandler(_handler)

    l.info('1232103982103821/dx/xx/xx/x/x/x')
    l.warning(bytes(44444))

if __name__ == '__main__':
    test2()