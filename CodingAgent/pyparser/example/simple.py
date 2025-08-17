import os
import sys

HELLO = "123456"

def hello():
    print("Hello world")
    i = 300

class TestClass():
    def __init__(self):
        self.time = "20250505"
    
    def run(self):
        print("This class is running!")

class TestClass2(TestClass):
    def __init__(self):
        super().__init__()
        self.another_time = "233"
    
    def run(self):
        print("This class is running!")

if __name__ == "__main__":
    test = TestClass()
    hello()
    test.run()