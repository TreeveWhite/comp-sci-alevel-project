import unittest
from poker.gameState.BestHandFinder import BestHandFinder

class MyTest(unittest.TestCase):

    handFinder = BestHandFinder()

    def test_pair(self):
        hand = ["AH.jpg", "AD.jpg"]
        tableCards = ["3D.jpg", "4D.jpg", "JC.jpg", "KH.jpg", "QS.jpg"]
        handStrength = self.handFinder.checkHand(hand + tableCards)
        self.assertEqual(handStrength, 2)
    
    def test_twoPair(self):
        hand = ["AH.jpg", "AD.jpg"]
        tableCards = ["3D.jpg", "4D.jpg", "3C.jpg", "KH.jpg", "QS.jpg"]
        handStrength = self.handFinder.checkHand(hand + tableCards)
        self.assertEqual(handStrength, 3)
    
    def test_threeKind(self):
        hand = ["AH.jpg", "AD.jpg"]
        tableCards = ["3D.jpg", "4D.jpg", "JC.jpg", "KH.jpg", "AS.jpg"]
        handStrength = self.handFinder.checkHand(hand + tableCards)
        self.assertEqual(handStrength, 4)
    
    def test_straight(self):
        hand = ["QH.jpg", "KC.jpg"]
        tableCards = ["JD.jpg", "10H.jpg", "9C.jpg", "KH.jpg", "AS.jpg"]
        handStrength = self.handFinder.checkHand(hand + tableCards)
        self.assertEqual(handStrength, 5)
    
    def test_flush(self):
        hand = ["9H.jpg", "7H.jpg"]
        tableCards = ["2H.jpg", "10H.jpg", "9C.jpg", "KH.jpg", "AS.jpg"]
        handStrength = self.handFinder.checkHand(hand + tableCards)
        self.assertEqual(handStrength, 6)
    
    def test_fullHouse(self):
        hand = ["9C.jpg", "9S.jpg"]
        tableCards = ["2H.jpg", "2H.jpg", "2C.jpg", "KH.jpg", "AS.jpg"]
        handStrength = self.handFinder.checkHand(hand + tableCards)
        self.assertEqual(handStrength, 7)
    
    def test_fourKind(self):
        hand = ["9H.jpg", "9C.jpg"]
        tableCards = ["2H.jpg", "10H.jpg", "9S.jpg", "KH.jpg", "9D.jpg"]
        handStrength = self.handFinder.checkHand(hand + tableCards)
        self.assertEqual(handStrength, 8)
    
    def test_straightFlush(self):
        hand = ["8H.jpg", "9H.jpg"]
        tableCards = ["10H.jpg", "JH.jpg", "9C.jpg", "QH.jpg", "AS.jpg"]
        handStrength = self.handFinder.checkHand(hand + tableCards)
        self.assertEqual(handStrength, 9)
    
    def test_royalFlush(self):
        hand = ["9H.jpg", "10H.jpg"]
        tableCards = ["JH.jpg", "QH.jpg", "9C.jpg", "KH.jpg", "AS.jpg"]
        handStrength = self.handFinder.checkHand(hand + tableCards)
        self.assertEqual(handStrength, 10)
    

if __name__ == "__main__":
    unittest.main()