
from xsqlmb.src.dao.xmodel import SqlModeClass



def test():
    SqlModeClass.get_demo_model()._create()

def test2():
    from xsqlmb.src.dao.Xfilter import WrapperFilter
    WrapperFilter.test_wrapped()

def test3():
    from xsqlmb.src.dao.Xfilter import GroupbyFilter
    GroupbyFilter.get_demo_sqldata()

if __name__ == '__main__':
    # test()
    #test2()
    test3()




