"""This program implements a simple scheduler 
which can run multiple coroutines round-robin style 
for the assignment 06.

It creates a scheduler that can run multiple coroutines,
each coroutine uses the yield statement to pause its execution
and the scheduler resumes it later.
It uses ANSI escape codes to color the output of each coroutine.

I have implemented 4 coroutines:
1. coprogram(x) - prints a message and then prints a message x times
2. fib(x) - prints the first x Fibonacci numbers,
inspired by code from Roderik Ploszek for PPDS 2024 course
3. prime_numbers(x) - prints the prime numbers up to number x
4. play_game() - a simple rock, paper, scissors game with infinite rounds
"""

__author__ = "Samuel Martin Sirota"
__email__ = "xsirotas@stuba.sk"

from typing import Callable
import random

"""ANSI escape codes for terminal colors"""
COLORS = [
    "\u001b[38;5;" + str(i * 16 + j) + "m" for i in range(0, 16) 
    for j in range(0, 16)
]


class Scheduler:
    """Scheduler class to run multiple coroutines.
    implements a simple round-robin scheduler for coroutines.
    maintains a list of coroutines and their colors.

    :jobs: List of tuples containing the coroutine and its color.
    :method add_job: Add a coroutine to the scheduler.
    :method start: Start the scheduler and run the coroutines.
    :method _execute_coprogram: Execute a coroutine and handle exceptions."""

    def __init__(self):
        self.jobs = []

    def add_job(self, it):
        color = random.choice(COLORS)
        COLORS.remove(color)
        self.jobs.append((it, color))

    def start(self):
        while self.jobs:
            for job, color in self.jobs:
                self._execute_coprogram(job, color)

    def _execute_coprogram(self, it, color):
        try:
            print(f"{color}", end="")
            next(it)
        except StopIteration:
            print(f"{color}--------Coprogram is terminated.--------\033[0m")
            it.close()
            self.jobs.remove((it, color))


def coprogram(num: int, word: str = "Hey"):
    """Prints the word string, num times.

    :param num: Number of times to print the message.
    :param word: Message to print."""
    print(f"----------Coprogram {num} created.----------")
    n = 0
    while n < num:
        n += 1
        yield
        print(f"Coprogram {num} received value:", word)


def fib(limit: int):
    """Generate Fibonacci sequence.

    :param limit: Number of Fibonacci numbers to generate."""
    print(f"------Fibonacci sequence first({limit}).------")
    i = 0
    a, b = 0, 1
    while i < limit:
        i += 1
        yield
        print(f"fib({i}): {b}")
        a, b = b, a + b


def prime_numbers(limit: int):
    """Generate prime numbers up to a specified limit.

    :param limit: Upper limit for prime numbers."""
    print(f"---------Prime numbers up to {limit}.---------")
    primes = []
    num = 2
    while True:
        if all(num % i != 0 for i in primes):
            yield
            primes.append(num)
            print(f"prime number: {num}")
        num += 1
        if num > limit:
            break


def play_game():
    """Simple rock, paper, scissors game with infinite rounds."""
    choices = ["rock", "paper", "scissors"]
    user_score = 0
    computer_score = 0
    print("---------Rock, paper, scissors.---------")
    while True:
        yield
        user_choice = input(
            "Enter your choice (rock, paper, scissors), "
            + "or 'quit' to end the game: "
        ).lower()
        computer_choice = random.choice(choices)

        if user_choice == "quit":
            break
        if user_choice not in choices:
            print("Invalid choice. Please choose again.")
            continue
        print(f"Computer chose: {computer_choice}", end=" | ")

        if user_choice == computer_choice:
            print("It's a tie!", end=" | ")
        elif (
            (user_choice == "rock" and computer_choice == "scissors")
            or (user_choice == "paper" and computer_choice == "rock")
            or (user_choice == "scissors" and computer_choice == "paper")
        ):
            print("You win!", end=" | ")
            user_score += 1
        else:
            print("Computer wins!", end=" | ")
            computer_score += 1
        print(f"Your score: {user_score}, Computer score: {computer_score}")
    print("Thanks for playing!")


def main():
    """Main function to run the scheduler with the coroutines."""
    scheduler = Scheduler()
    scheduler.add_job(coprogram(5))
    scheduler.add_job(fib(3))
    scheduler.add_job(prime_numbers(5))
    scheduler.add_job(play_game())
    scheduler.start()


if __name__ == "__main__":
    main()