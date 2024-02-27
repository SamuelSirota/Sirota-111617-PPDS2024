"""This module implements 'Who had breakfast first?' problem for the 
assignment 01. 

Both Jano and Fero wake up, do morning hygiene,
Jano eats first and then calls Fero.
Only after Fero receives the call can he eat his breakfast."""

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
        
    def wait(self, tid):
        """Waits for all threads to reach the barrier."""
        self.mutex.lock()
        self.counter += 1
        print(f"Savage ({tid}) is waiting for others. ({self.counter}/{self.n})")
        if self.counter == self.n:
            self.counter = 0
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
    while True:
        shared.barrier1.wait(tid)
        shared.barrier2.wait(tid)
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
    while True:
        shared.emptyPot.wait()
        print("Cook is cooking.")
        sleep(0.1)
        shared.servings = 10
        print("Cook is putting the pot on the table.")
        shared.fullPot.signal()
    
def main():
    """This function uses semaphores to solve the 'Who had breakfast
    first' problem.
    """
    n_threads = 7
    shared = Shared(n_threads)
    savages = [Thread(savage, shared, i) for i in range(n_threads)]
    cooks = Thread(cook, shared)
    [t.join() for t in savages]
    cook.join()


if __name__ == "__main__":
    main()