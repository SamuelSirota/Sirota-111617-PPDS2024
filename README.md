# Assignment 03 - The Roller coaster problem

[![Python 3.10.12](https://img.shields.io/badge/python-3.10.12-purple.svg)](https://www.python.org/downloads/release/python-31012/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-purple.svg)](https://conventionalcommits.org)

## Description

This is a simple Python program that uses mutexes, semaphores and barriers to solve the Roller coaster problem.

---

## Quick start

Before running the script, make sure you have Python 3.10.12 installed.
Also install `fei.ppds` module (`pip install --upgrade fei.ppds`)

## Assignment

1. Implement the Roller coaster problem using semaphores, mutexes and barriers.
2. There are `N` passengers and one train. The train has a limited capacity `C`. (C < N)
3. The passengers are boarding the train one by one. The last passenger to board signals the train to depart.
4. The train can only depart when it is full.
5. After the ride, the passengers are leaving the train one by one. Again last passenger signals the train to start loading new passengers.
6. This process is repeated indefinitely.

## Implementation

My implementation has 20 passenger threads, the train capacity is 8 passengers.

The code is using mechanism called `barrier` to wait for all passengers to be present before starting the ride. I used the code below.
I am also passing boolean values `boarded` and `unboarded` to the barrier to signal the train to depart and to signal the train to start loading new passengers.

```python
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
```

---
The code for the `passenger` thread is as follows:

```python
shared.boardQ.wait()
shared.boardB.board(tid)
shared.boardB.wait(shared, True, False, tid)
shared.unboardQ.wait()
shared.boardB.unboard(tid)
shared.unboardB.wait(shared, False, True, tid)
```

- The passenger threads are running infinite loop
- They are waiting for the `boardQ` semaphore to signal that the train is ready to board
- Then they are boarding the train and signaling the `boardB` barrier to wait for all passengers to board
- After the ride, they are waiting for the `unboardQ` semaphore to signal that the train is ready to unboard
- Then they are unboarding the train and signaling the `unboardB` barrier to wait for all passengers to unboard

---

The code for the `train` thread is as follows:

```python
shared.boardB.load()
shared.boardQ.signal(shared.train_capacity)
shared.boarded.wait()
shared.boardB.run()
shared.boardB.unload()
shared.unboardQ.signal(shared.train_capacity)
shared.unboarded.wait()
```

- The train thread is running infinite loop
- It is loading the passengers and signaling the `boardQ` semaphore to signal that the train is ready to board
- Then it is waiting for the `boarded` semaphore to signal that all passengers have boarded
- Then it is running the ride
- Then it is unloading the passengers and signaling the `unboardQ` semaphore to signal that the train is ready to unboard
- Then it is waiting for the `unboarded` semaphore to signal that all passengers have unboarded

### Starvation problem

Similiarly to the dining philosophers problem, the Roller coaster problem has a starvation problem. The passengers are boarding the train randomly, there is no queue. This means that the same passengers could board the train over and over again and the some other could never get a chance to board the train. This could be solved by implementing FIFO queue for the passengers.

## Console output

This is a short sample output of the program.

```plaintext
Loading passengers.
Passenger number: 16 is boarding.
Passenger number: 10 is boarding.
Passenger number: 9 is boarding.
Passenger number: 14 is boarding.
Passenger number: 4 is boarding.
Passenger number: 18 is boarding.
Passenger number: 7 is boarding.
Passenger number: 6 is boarding.
Passenger (6) is the last to board. HERE WE GO!
Running.
Unloading passengers.
Passenger number: 16 is unboarding.
Passenger number: 18 is unboarding.
Passenger number: 9 is unboarding.
Passenger number: 10 is unboarding.
Passenger number: 7 is unboarding.
Passenger number: 4 is unboarding.
Passenger number: 6 is unboarding.
Passenger number: 14 is unboarding.
Passenger (14) is the last to unboard. Until next time!
Loading passengers.
Passenger number: 6 is boarding.
Passenger number: 10 is boarding.
Passenger number: 16 is boarding.
Passenger number: 17 is boarding.
Passenger number: 5 is boarding.
Passenger number: 3 is boarding.
Passenger number: 11 is boarding.
Passenger number: 12 is boarding.
Passenger (12) is the last to board. HERE WE GO!
Running.
Unloading passengers.
Passenger number: 6 is unboarding.
Passenger number: 5 is unboarding.
Passenger number: 10 is unboarding.
Passenger number: 17 is unboarding.
Passenger number: 12 is unboarding.
Passenger number: 3 is unboarding.
Passenger number: 16 is unboarding.
Passenger number: 11 is unboarding.
Passenger (11) is the last to unboard. Until next time!
Loading passengers.
```
