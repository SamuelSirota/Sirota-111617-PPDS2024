# Assignment 06 - Scheduler for coprograms

[![Python 3.10.12](https://img.shields.io/badge/python-3.10.12-purple.svg)](https://www.python.org/downloads/release/python-31012/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-purple.svg)](https://conventionalcommits.org)
[![Static Badge](https://img.shields.io/badge/CUDA_Toolkit-12.4-purple)](https://developer.nvidia.com/cuda-downloads?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local)

## Description

This is a simple Python program which implements simple scheduler for coprograms based on enhanced generators.

---

## Quick start

Before running the script, make sure you have Python 3.10.12 installed.

## Assignment

1. Implement simple scheduler for coprograms based on enhanced generators.
2. Scheduler should be able to run multiple coprograms round-robin style.
3. Scheduler should implement `add_job` method to add new coprogram to the scheduler.
4. Scheduler should also implement `start` method to run all coprograms.
5. Scheduler should respond to `StopIteration` exception and remove coprogram from the scheduler and print the message.
6. Prepare a sample program to demonstrate the scheduler implementing at least 3 coprograms, also 1 of them should end in finite time.

## Implementation

My implementation has few components:

1. Scheduler class
2. Coprogram functions
3. Main function with sample program

### Scheduler class

My implementation of the scheduler class has one internal property `jobs` which is a list of tuples containing the coroutine and its color.
It has 3 methods:

- `add_job` to add a coroutine to the scheduler, it also assigns a color to the coroutine
- `start` to start the scheduler and run the coroutines round-robin style
- `_execute_coprogram` to execute each coroutine and handle exceptions

### Coprogram functions

I have implemented 4 coprogram functions:

- `coprogram`: This coprogram prints the specified message and yields the control back to the scheduler and repeats specified number of times
- `fib`: This coprogram prints the fibonacci series number and yields the control back to the scheduler and repeats specified number of times
- `prime_numbers`: This coprogram prints the prime numbers and yields the control back to the scheduler and repeats up to specified limit
- `play_game`: This coprogram implements a simple rock-paper-scissors game and yields the control back to the scheduler it runs infinitely or until user wants to stop, this coroutine needs user input

### Main function with sample program

I have created an instance of the scheduler and added 4 coprogram functions to it. Then I started the scheduler. The scheduler will run all the coprogram functions round-robin style.

### Sample program output

```plaintext
----------Coprogram 5 created.----------
------Fibonacci sequence first(3).------
---------Prime numbers up to 5.---------
---------Rock, paper, scissors.---------
Coprogram 5 received value: Hey
fib(1): 1
prime number: 2
Enter your choice (rock, paper, scissors), or 'quit' to end the game: paper
Computer chose: scissors | Computer wins! | Your score: 0, Computer score: 1
Coprogram 5 received value: Hey
fib(2): 1
prime number: 3
Enter your choice (rock, paper, scissors), or 'quit' to end the game: lol
Invalid choice. Please choose again.
Coprogram 5 received value: Hey
fib(3): 2
--------Coprogram is terminated.--------
Enter your choice (rock, paper, scissors), or 'quit' to end the game: quit
Thanks for playing!
--------Coprogram is terminated.--------
Coprogram 5 received value: Hey
prime number: 5
--------Coprogram is terminated.--------
Coprogram 5 received value: Hey
--------Coprogram is terminated.--------
```
