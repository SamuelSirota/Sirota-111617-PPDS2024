# Assignment 07 - Asynchronous file downloader

[![Python 3.12.3](https://img.shields.io/badge/python-3.12.3-purple.svg)](https://www.python.org/downloads/release/python-3123/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-purple.svg)](https://conventionalcommits.org)

## Description

This is a simple Python program that uses python libraries asyncio
and aiohttp to download files from a list of URLs.
It also uses the `tqdm` library to display a progress bar.

---

## Quick start

Before running the script, make sure you have Python 3.12.3 installed.
Install the required libraries using `pip install aiohttp`
and `pip install tqdm`.

## Assignment

1. Implement asynchronous application which uses HTTP(S) to download files.
2. It should be able to download multiple files at the same time.
3. Additionally, it should display a progress bar for each download.
4. Progress bar shows url of the file being downloaded.
5. The file should be saved to disk.

## Implementation

My implementation has few components:

1. `task` function - downloads a single file from the given URL. Also the tqdm progress bar is being displayed inside this function.
2. `main` function - creates an `asyncio.Queue`, adds URLs to it, and runs tasks concurrently.

## Example

```bash
$ python3 filedownloader.py
Task two: https://ploszek.com/ppds/2024-11.async.pdf: 100%|████████████████████████████████████| 410k/410k [00:03<00:00, 131kB/s] | 100% | 00:03
Task one: https://ploszek.com/ppds/2024-06.Paralelne_vypocty_3.pdf: 100%|████████████████████| 1.18M/1.18M [00:11<00:00, 106kB/s] | 100% | 00:11

Total elapsed time: 12.9 seconds.
```
