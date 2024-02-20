# Assignment 01 - Who had breakfast first?

[![Python 3.10.12](https://img.shields.io/badge/python-3.10.12-purple.svg)](https://www.python.org/downloads/release/python-31012/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-purple.svg)](https://conventionalcommits.org)

## Description

This is a simple Python program that uses semaphores to solve the 'Who had breakfast first?' problem.

---

## Quick start
Before running the script, make sure you have Python 3.10.12 installed.
Also install `fei.ppds` module (`pip install --upgrade fei.ppds`)

## Assignment

1. Implement "Who had breakfast first?" problem from lecture.
2. Simulate sleep, hygiene, call and breakfast processes.
3. Ensure that subject (Jano) eats first before the other subject (Fero). 
   Use scheme from the lecture.
4. Write a documentation. Include all important details about the problem and the solution. Add output from the console to the documentation.

## Implementation

- Implementation consists of few dummy functions that simulate the processes of sleep, hygiene, call and breakfast. They `sleep()` for 0.1 seconds and print the name of the process.
- Function `person()` runs all the morning routine processses. Using semaphores it ensures that Jano eats first before Fero.
- if the `person()` is Fero it waits for the semaphore to be signaled by Jano. Only then Fero can eat.
    ```python
    shared.semaphore.wait()
    receive_call(name)
    breakfast(name)
    shared.semaphore.signal()
    ```
- The main function `main()` creates the 2 threads, Jano and Fero, creates semaphore and shared object and starts the threads.
    ```python
    n_threads = 2
    semaphore = Semaphore(0)
    shared = Shared(semaphore)
    threads = [Thread(person, shared, i) for i in range(n_threads)]
    [t.join() for t in threads]

    ```
## Console Output

If you run the script, you should see the following output in the console:


![Console output](https://cdn.discordapp.com/attachments/766251086855274529/1209605158808326185/image.png?ex=65e78797&is=65d51297&hm=8fa68189ad2c34d108c4755226deaf0b348032bb0e83eb185cea7170115c7a21&)

Its not importatnt who woke up first and who did his hygiene first, the important thing is that Jano eats first, calls Fero. Fero recieves the call and only then Fero can eat his breakfast.