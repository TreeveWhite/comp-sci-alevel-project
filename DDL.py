from databases.SuperDBHandler import DataBaseHandler

if __name__ == "__main__":
    dbHandler = DataBaseHandler()

    dbHandler.deleteTables()
    dbHandler.generateTables()