# Assignment 02 - The dining savages problem.

[![Python 3.10.12](https://img.shields.io/badge/python-3.10.12-purple.svg)](https://www.python.org/downloads/release/python-31012/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-purple.svg)](https://conventionalcommits.org)

## Description

This is a simple Python program that uses mutexes, semaphores and barriers to solve the dining savages problem.

---

## Quick start

Before running the script, make sure you have Python 3.10.12 installed.
Also install `fei.ppds` module (`pip install --upgrade fei.ppds`)

## Assignment

1. Implement the dining savages problem using semaphores and mutexes.
2. There are `N` savages and one cook. They start the feast only when all of them are present.
3. The savages eat one by one from the pot, which can hold `M` portions of food. They eat until the pot is empty.
4. The savage who finds the pot empty wakes up the cook, who fills the pot with `M` portions of food.
5. They wait for the cook to fill the pot and then start eating again.
6. After eating, they wait for the next meal and repeat the process indefinitely.

![illustration of the dining savages problem](https://media.discordapp.net/attachments/766251086855274529/1212111580364546118/image.png?ex=65f0a5e0&is=65de30e0&hm=163d155fc53edec6674be493c9d17eecc524cd918bbac58fe3254814509f0ee6&=&format=webp&quality=lossless&width=738&height=362)
Illustration of the problem.

## Implementation

My implementation has 7 savage threads, one cook thread and pot size of 10 portions.

The code is using mechanism called `barrier` to wait for all savages to be present before starting the feast. I used the code below.

```python
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
```

> Barrier is synchronization primitive that requires a minimum number of threads to reach a common point before any are allowed to progress. [^1]

- It essentially waits until the counter is equal to the number of savages, then it resets the counter and signals the turnstile `7` times to let all savages pass.
- At the end of function turnstile, which is `semaphore` initialized to 0. Is used to wait for all savages to be present before starting the feast again.
- When manipulating with shared resources, it uses `mutex` to lock the critical section.
- We are using 2 barriers, to make sure that the savage threads won't skip the waiting at first barrier and start eating before all of them are gathered.
- In first barrier we print which sage is waiting for others, and in second barrier we print that the feast has started as all of them are present.

---
The code for the `savage` thread is as follows:

```python
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
```

- The savage threads are running infinite loop
- 2 barrier make sure all of them are gathered
- One by one they look if the pot has any food left if not, they wake up the cook and eat after the pot is filled
- If there is food, they eat and sleep for a while
- Again we are using the `mutex` to lock the critical section
- 'emptyPot' and 'fullPot' are `semaphores` used to signal the cook and wait for the pot to be filled
- There is also a sleep function to simulate the eating process

> Mutex is a thread synchronization primitive that can be used to provide mutually exclusive access to a critical section. [^2]

---

The code for the `cook` thread is as follows:

```python
shared.emptyPot.wait()
print("Cook is cooking.")
sleep(0.1)
shared.servings = 10
print("Cook is putting the pot on the table.")
shared.fullPot.signal()
```

- The cook thread is running infinite loop
- 'emptyPot' `semaphore` is used to wait for the savage to wake it up when the pot is empty
- It cooks the food and fills the pot with 10 portions
- Then it signals the 'fullPot' `semaphore` to let the savages know that the pot is full

> Semaphore is an integer with atomic operations for incrementing and decrementing the value; if the result of decrementing the value is negative, the current process becomes blocked until another process increments the value. [^3]

## Console output

This is a short sample output of the program.

```plaintext
Savage (0) is waiting for others. (1/7)
Savage (1) is waiting for others. (2/7)
Savage (2) is waiting for others. (3/7)
Savage (3) is waiting for others. (4/7)
Savage (4) is waiting for others. (5/7)
Savage (5) is waiting for others. (6/7)
Savage (6) is waiting for others. (7/7)
Savage (2) starts the feast.
Savage (2) is looking into the pot. (10) servings left.
Savage (2) is taking a portion.
Savage (0) is looking into the pot. (9) servings left.
Savage (0) is taking a portion.
Savage (5) is looking into the pot. (8) servings left.
Savage (5) is taking a portion.
Savage (6) is looking into the pot. (7) servings left.
Savage (6) is taking a portion.
Savage (1) is looking into the pot. (6) servings left.
Savage (1) is taking a portion.
Savage (3) is looking into the pot. (5) servings left.
Savage (3) is taking a portion.
Savage (4) is looking into the pot. (4) servings left.
Savage (4) is taking a portion.
Savage (1) is munching.
Savage (1) is waiting for others. (1/7)
Savage (2) is munching.
Savage (2) is waiting for others. (2/7)
Savage (5) is munching.
Savage (6) is munching.
Savage (5) is waiting for others. (3/7)
Savage (6) is waiting for others. (4/7)
Savage (0) is munching.
Savage (0) is waiting for others. (5/7)
Savage (3) is munching.
Savage (3) is waiting for others. (6/7)
Savage (4) is munching.
Savage (4) is waiting for others. (7/7)
Savage (5) starts the feast.
Savage (5) is looking into the pot. (3) servings left.
Savage (5) is taking a portion.
Savage (0) is looking into the pot. (2) servings left.
Savage (0) is taking a portion.
Savage (3) is looking into the pot. (1) servings left.
Savage (3) is taking a portion.
Savage (2) is looking into the pot. (0) servings left.
Savage (2) is waking up the cook.
Cook is cooking.
Savage (0) is munching.
Savage (0) is waiting for others. (1/7)
```


[^1]: [Barriers](https://w3.cs.jmu.edu/kirkpams/OpenCSF/Books/csf/html/Barriers.html)
[^2]: [Mutex](https://w3.cs.jmu.edu/kirkpams/OpenCSF/Books/csf/html/Glossary.html#term-mutex)
[^3]: [Semaphore](https://w3.cs.jmu.edu/kirkpams/OpenCSF/Books/csf/html/Glossary.html#term-semaphore)