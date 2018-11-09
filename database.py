import pyodbc


def setupDB():
    ServerName = "den1.mssql5.gear.host"
    MSQLDatabase = 'tymooredb'
    username = 'tymooredb'
    password = '3I%sZCr!QcCQiPIn%06F'
    connection = pyodbc.connect(
        'Driver=SQL Server;Server={};Database={};uid={};pwd={}'.format(
            ServerName, MSQLDatabase, username, password))

    return connection


def finishDB(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()


def getRows(table_name):
    connection = setupDB()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM " + str(table_name))
    results = cursor.fetchall()
    finishDB(connection, cursor)
    return results


def main():
    print(getRows('PokerStandings'))


if __name__ == '__main__':
    main()
