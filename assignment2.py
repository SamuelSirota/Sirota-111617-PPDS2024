"""This module implements the dining savages problem for the 
assignment 02. 

All savages meet for a feast.
Only when all of them are ready to eat can they start eating.
They eat in a round-robin style.
When the pot is empty, the cook is woken up to cook more food.
When they are done eating, 
they go back to the beginning and meet for another feast."""

__authors__ = "Samuel Martin Sirota"
__email__ = "xsirotas@stuba.sk"

from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep
from random import randint

class Barrier:
    """This class represents a barrier."""
    def __init__(self, n):
        """Initializes the barrier."""
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)
        
    def wait(self, tid, string):
        """Waits for all threads to reach the barrier."""
        self.mutex.lock()
        self.counter += 1
        if string == "one by one":
            print(f"Savage ({tid}) is waiting for others. ({self.counter}/{self.n})")
        if self.counter == self.n:
            self.counter = 0
            if string == "all at once":
                print(f"Savage ({tid}) starts the feast.")
            self.turnstile.signal(self.n)
        self.mutex.unlock()
        self.turnstile.wait()

class Shared:
    """This class represents shared data."""
    def __init__(self, n_threads):
        """Initializes shared data."""
        self.mutex = Mutex()
        self.fullPot = Semaphore(0)
        self.emptyPot = Semaphore(0)
        self.servings = 10
        self.barrier1 = Barrier(n_threads)
        self.barrier2 = Barrier(n_threads)
        

def savage(shared, tid):
    """This function simulates a savage.
    It waits for all savages to be ready to eat.
    Then it eats in a round-robin style.
    When the pot is empty, it wakes up the cook.
    Waits for the cook to fill the pot.
    Eats again in a round-robin style.
    After everyone is done eating, it goes back to the beginning."""
    while True:
        shared.barrier1.wait(tid, "one by one")
        shared.barrier2.wait(tid, "all at once")
        shared.mutex.lock()
        print(f"Savage ({tid}) is looking into the pot. ({shared.servings}) servings left.")
        if shared.servings == 0:
            print(f"Savage ({tid}) is waking up the cook.")
            shared.emptyPot.signal()
            shared.fullPot.wait()
        print(f"Savage ({tid}) is taking a portion.")
        shared.servings -= 1
        shared.mutex.unlock()
        sleep(randint(1, 5) / 10)
        print(f"Savage ({tid}) is munching.")
        
def cook(shared):
    """This function simulates a cook.
    It waits the pot to be empty.
    Then it cooks the food and fills the pot."""
    while True:
        shared.emptyPot.wait()
        print("Cook is cooking.")
        sleep(0.1)
        shared.servings = 10
        print("Cook is putting the pot on the table.")
        shared.fullPot.signal()
    
    
def main():
    """This function initializes the shared data,
    creates the thread for the savages and the cook"""
    n_threads = 7
    shared = Shared(n_threads)
    savages = [Thread(savage, shared, i) for i in range(n_threads)]
    cooks = Thread(cook, shared)
    [t.join() for t in savages]
    cooks.join()


if __name__ == "__main__":
    main()