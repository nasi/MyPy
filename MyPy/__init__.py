

def Connect(*args, **kwargs):
    from MyPy.core.connection import Connection
    return Connection(*args, **kwargs)

connect = Connection = Connect