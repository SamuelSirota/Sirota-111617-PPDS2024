"""This module implements 'Who had breakfast first' problem for the 
assignment 01. 

Both Jano and Fero wake up, do morning hygiene,
Jano eats first and then calls Fero.
Only after Fero receives the call can he eat his breakfast."""

__authors__ = "Samuel Martin Sirota"
__email__ = "xsirotas@stuba.sk"

from fei.ppds import Thread, Semaphore, print
from time import sleep


class Shared:
    """This class represents shared data."""
    def __init__(self, semaphore):
        """Initializes shared data."""
        self.semaphore = semaphore


def person(shared, tid):
    """This function simulates a person's morning routine."""
    if tid == 0:
        name = "Jano"
    elif tid == 1:
        name = "Fero"
    sleeping(name)
    hygiene(name)
    if name == "Jano":
        breakfast(name)
        call_him(name)
        shared.semaphore.signal()
    if name == "Fero":
        shared.semaphore.wait()
        receive_call(name)
        breakfast(name)
        shared.semaphore.signal()


def sleeping(name):
    """This function simulates a person sleeping"""
    sleep(0.1)
    print(name + " woke up!")

def hygiene(name):
    """This function simulates a person doing morning hygiene."""
    sleep(0.1)
    print(name + " is doing morning hygiene!")   
    
def breakfast(name):
    """This function simulates a person eating breakfast."""
    sleep(0.1)
    print(" " + name + " is eating breakfast!")
    
def receive_call(name):
    """This function simulates a person receiving a call."""
    sleep(0.1)
    print("  " + name + " received a call!")

def call_him(name):
    """This function simulates a person calling another person."""
    sleep(0.1)
    print("  " + name + " is calling Fero!")


if __name__ == "__main__":
    n_threads = 2
    semaphore = Semaphore(0)
    shared = Shared(semaphore)
    threads = [Thread(person, shared, i) for i in range(n_threads)]
    [t.join() for t in threads]