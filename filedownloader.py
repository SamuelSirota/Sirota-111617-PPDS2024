"""This program implements a simple asynchronous file downloader
using aiohttp and asyncio libraries for the assignment 07.

The program downloads files from the given URLs
and saves them to the local directory.
The program uses asyncio.Queue to store the URLs
and asyncio.gather to run the tasks concurrently.
It also uses tqdm to display the progress bar of the download.

My code is highly inspired by the source code
from the 13th week's seminar, which is inspired by RealPython. 
I have modified the code to download files from the given URLs
and save them to the local directory.
https://realpython.com/python-async-features/
https://elearn.elf.stuba.sk/moodle/pluginfile.php/77491/mod_resource/content/0/2024-12.async.pdf
"""

__author__ = "Samuel Martin Sirota"
__email__ = "xsirotas@stuba.sk"

import asyncio
import aiohttp
import time
from urllib.parse import urlparse
from tqdm import tqdm


async def task(name, work_queue):
    """Download files from the given URLs and save them to the local directory.

    This function uses the aiohttp library to download the files
    and tqdm to display the progress bar of the download.
    """
    async with aiohttp.ClientSession() as session:
        while not work_queue.empty():
            url = await work_queue.get()
            file_name = urlparse(url).path.split("/")[-1].replace("%20", " ")
            async with session.get(url) as response:
                file_size = int(response.headers.get("Content-Length", 0))
                with open(file_name, "wb") as file, tqdm(
                    desc=f"Task {name}: {url}",
                    total=file_size,
                    colour="#136680",
                    unit="B",
                    unit_scale=True,
                    smoothing=True,
                    dynamic_ncols=True,
                    bar_format="{l_bar}{bar}{r_bar} | {percentage:3.0f}% | {elapsed}",
                    leave=True,
                ) as progress_bar:
                    downloaded = 0
                    while True:
                        block = await response.content.read(1024)
                        if not block:
                            break
                        file.write(block)
                        downloaded += len(block)
                        progress_bar.update(len(block))


async def main():
    """Create the asyncio.Queue, add URLs to it, and run tasks concurrently.

    This function also measures the time it took to download the files.
    """
    work_queue = asyncio.Queue()

    for url in [
        "https://ploszek.com/ppds/2024-06.Paralelne_vypocty_3.pdf",
        "https://ploszek.com/ppds/2024-11.async.pdf",
    ]:
        await work_queue.put(url)
    time_start = time.perf_counter()
    await asyncio.gather(
        task("one", work_queue),
        task("two", work_queue),
    )
    elapsed = time.perf_counter() - time_start
    print(f"\nTotal elapsed time: {elapsed:.1f} seconds.")


if __name__ == "__main__":
    asyncio.run(main())
