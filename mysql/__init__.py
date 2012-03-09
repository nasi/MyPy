

def Connect(*args, **kwargs):
    from mysql.core.connection import Connection
    return Connection(*args, **kwargs)

connect = Connection = Connect