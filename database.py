import pypyodbc

def setupDB():
    ServerName = "den1.mssql5.gear.host"
    MSQLDatabase = 'tymooredb'
    username = 'tymooredb'
    password = '3I%sZCr!QcCQiPIn%06F'
    connection = pypyodbc.connect('Driver=SQL Server;Server={};Database={};uid={};pwd={}'.format(ServerName,MSQLDatabase,username,password))
    
    return connection

def finishDB(connection, cursor):
    connection.commit()
    cursor.close()
    connection.close()

def main():
    connection = setupDB()
    cursor = connection.cursor()

    cursor.execute("INSERT INTO PokerStandings VALUES(5,'Hearts',2,'Diamonds',5,'Hearts',2,'Diamonds',5,'Hearts',2,'Diamonds',2,'Diamonds','Bet',200,1)")
    cursor.execute("SELECT * FROM PokerStandings")

    results = cursor.fetchall()
    print(results)

    finishDB(connection, cursor)


if __name__ == '__main__':
    main()