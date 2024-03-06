"""This module implements the Roller coaster problem for the 
assignment 03. 

There are N passengers and one train. 
The train has a capacity of C passengers.
N > C
The train can ride only when it is full.
The passengers board and unboard the train in a round-robin style.
Last one to board and signals the train to start running.
Last one to unbord signals the train to stop running."""

__authors__ = "Samuel Martin Sirota"
__email__ = "xsirotas@stuba.sk"

from fei.ppds import Thread, Mutex, Semaphore, print
from time import sleep
from random import randint


class Shared:
    """This class represents shared data."""
    def __init__(self, train_capacity):
        """Initializes shared data."""
        self.mutex = Mutex()
        self.servings = 10
        self.train_capacity = train_capacity
        self.boarded = Semaphore(0)
        self.unboarded = Semaphore(0)
        self.boardQ = Semaphore(0)
        self.unboardQ = Semaphore(0)
        self.boardB = Barrier(train_capacity)
        self.unboardB = Barrier(train_capacity)


class Barrier:
    """This class represents a barrier."""
    def __init__(self, n):
        """Initializes the barrier."""
        self.n = n
        self.counter = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)
        
    def wait(self, shared, boarded=None, unboarded=None, tid=None):
        """Waits for all threads to reach the barrier."""
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.n:
            self.counter = 0
            self.barrier.signal(self.n)
            if boarded:
                print(f"Passenger ({tid}) is the last to board. HERE WE GO!")
                shared.boarded.signal()
            if unboarded:
                print(f"Passenger ({tid}) is the last to unboard. Until next time!")
                shared.unboarded.signal()
        self.mutex.unlock()
        self.barrier.wait()
        
    def load(self):
        """Simulates loading the passengers into the train."""
        sleep(randint(1, 5) / 10)
        print("Loading passengers.")
        
    def run(self):
        """Simulated running the train."""
        sleep(randint(5, 10) / 10)
        print("Running.")
        
    def unload(self):
        """Simulates unloading the passengers from the train."""
        sleep(randint(1, 5) / 10)
        print("Unloading passengers.")
        
    def board(self, tid):
        """Simulates the passengers boarding the train."""
        sleep(randint(1, 5) / 10)
        print(f"Passenger number: {tid} is boarding.")
    
    def unboard(self, tid):
        """Simulates the passengers unboarding the train."""
        sleep(randint(1, 5) / 10)
        print(f"Passenger number: {tid} is unboarding.")


def passenger(shared, tid):
    """This function simulates a passenger.
    Simulates boarding and unboarding the train."""
    while True:
        shared.boardQ.wait()
        shared.boardB.board(tid)
        shared.boardB.wait(shared, True, False, tid)
        shared.unboardQ.wait()
        shared.boardB.unboard(tid)
        shared.unboardB.wait(shared, False, True, tid)

  
def train(shared):
    """This function simulates a train.
    Simulates loading, running and unloading the passengers."""
    while True:
        shared.boardB.load()
        shared.boardQ.signal(shared.train_capacity)
        shared.boarded.wait()
        shared.boardB.run()
        shared.boardB.unload()
        shared.unboardQ.signal(shared.train_capacity)
        shared.unboarded.wait()
    
    
def main():
    """This function initializes the shared data,
    creates the thread for the passengers and the train"""
    n_passengers = 20
    train_capacity = 8
    shared = Shared(train_capacity)
    passengers = [Thread(passenger, shared, i) for i in range(n_passengers)]
    trains = Thread(train, shared)
    [t.join() for t in passengers]
    trains.join()


if __name__ == "__main__":
    main()