from databases.SuperDBHandler import DataBaseHandler

class EventsDBHandler(DataBaseHandler):

    def __init__(self):
        super().__init__()
        self.clearEvents()

    def checkEventNotDuplicate(self, event, tableID, hand):
        isDuplicate = False
        sql = "SELECT event, hand FROM events WHERE tableid = %s"
        data = (tableID, )

        events = self.run_SQL(sql, data, False)

        for item in events:
            if event.split(" ")[0] == "BET":
                continue
            elif item[0] == event and item[1] == hand:
                isDuplicate = True
                break
            elif item[0].split(",")[0] == event.split(",")[0] and event.split(",")[0].split(" ")[0] == "ADD" and item[1] == hand:
                isDuplicate = True
                break  
        return isDuplicate

    def addEventADD(self, cookie, tableID, hand, money):
        event = f"ADD {cookie},{money}"
        isDuplicate = self.checkEventNotDuplicate(event, tableID, hand)
        if not isDuplicate:
            sql = """
            INSERT INTO events (tableID, hand, event)
            VALUES(%s, %s, %s)
            """
            data = (tableID, hand, event)
            self.run_SQL(sql, data)

        return not isDuplicate

    def addEventREADY(self, cookie, tableID, hand):
        event = f"READY {cookie}"
        isDuplicate = self.checkEventNotDuplicate(event, tableID, hand)
        if not isDuplicate:
            sql = """
            INSERT INTO events (tableID, hand, event)
            VALUES(%s, %s, %s)
            """
            data = (tableID, hand, event)
            self.run_SQL(sql, data)
        return not isDuplicate

    def addEventFOLD(self, cookie, tableID, hand):
        event = f"FOLD {cookie}"
        isDuplicate = self.checkEventNotDuplicate(event, tableID, hand)
        if not isDuplicate:
            sql = """
            INSERT INTO events (tableID, hand, event)
            VALUES(%s, %s, %s)
            """
            data = (tableID, hand, event)
            self.run_SQL(sql, data)
        return not isDuplicate
    
    def addEventCARDS(self, cookie, tableID, hand, cards):
        event = f"CARDS {cookie},{cards[0]},{cards[1]}"
        if not self.checkEventNotDuplicate(event, tableID, hand):
            sql = """
            INSERT INTO events (tableID, hand, event)
            VALUES(%s, %s, %s)
            """
            data = (tableID, hand, event)
            self.run_SQL(sql, data)
    
    def addEventBET(self, cookie, tableID, hand, amount):
        event = f"BET {cookie},{amount}"
        isDuplicate = self.checkEventNotDuplicate(event, tableID, hand)
        if not isDuplicate:
            sql = """
            INSERT INTO events (tableID, hand, event)
            VALUES(%s, %s, %s)
            """
            data = (tableID, hand, event)
            self.run_SQL(sql, data)
        return not isDuplicate
    
    def addEventFLOP(self, tableID, hand, flop):
        event = f"FLOP {flop[0]},{flop[1]},{flop[2]}"
        isDuplicate = self.checkEventNotDuplicate(event, tableID, hand)
        if not isDuplicate:
            sql = """
            INSERT INTO events (tableID, hand, event)
            VALUES(%s, %s, %s)
            """
            data = (tableID, hand, event)
            self.run_SQL(sql, data)
        return not isDuplicate
    
    def addEventTURN(self, tableID, hand, turn):
        event = f"TURN {turn}"
        isDuplicate = self.checkEventNotDuplicate(event, tableID, hand)
        if not isDuplicate:
            sql = """
            INSERT INTO events (tableID, hand, event)
            VALUES(%s, %s, %s)
            """
            data = (tableID, hand, event)
            self.run_SQL(sql, data)
        return not isDuplicate

    def addEventRIVER(self, tableID, hand, river):
        event = f"RIVER {river}"
        isDuplicate = self.checkEventNotDuplicate(event, tableID, hand)
        if not isDuplicate:
            sql = """
            INSERT INTO events (tableID, hand, event)
            VALUES(%s, %s, %s)
            """
            data = (tableID, hand, event)
            self.run_SQL(sql, data)
        return not isDuplicate
    
    def getAllEventsForTableHand(self, tableID, hand):
        sql = "SELECT event FROM events WHERE tableid = %s AND hand = %s"
        data = (tableID, hand)
        events = self.run_SQL(sql, data)

        return events
    
    def clearEvents(self):
        sql = "DELETE FROM events"
        self.run_SQL(sql)
