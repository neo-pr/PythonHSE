import aiohttp
import aiofiles
import asyncio
import pathlib
from functools import wraps
import time
import argparse


def async_measure_time(func):
    @wraps(func)
    async def wrap(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"Executed {func} in {elapsed:0.3f} seconds")
        return result

    return wrap


async def download_picture(url, session, file):
    async with session.get(url) as response:
        # verbose
        print(f"Saving file {file.name} to {file.parent}")
        async with aiofiles.open(file, "wb") as f:
            await f.write(await response.read())


@async_measure_time
async def main():
    parser = argparse.ArgumentParser(
        description="Saves NUM_FILES pictures to FOLDER from the website https://picsum.photos",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("num_files", type=int)
    parser.add_argument("folder")
    parser.add_argument("--width", default="536", help="The width of the picture")
    parser.add_argument("--height", default="354", help="The height of the picture")

    args = parser.parse_args()

    file_path = pathlib.Path(args.folder)
    if not file_path.exists():
        file_path.mkdir()

    prefix = max(4, len(str(args.num_files)))  # number of digits
    sites = [
        "https://picsum.photos/",
    ] * args.num_files
    async with aiohttp.ClientSession() as session:
        tasks = []
        for img_num, site in enumerate(sites):
            url = f"{site}{args.width}/{args.height}"
            fname = file_path.joinpath(f"img{img_num:0{prefix}d}.jpg")
            task = asyncio.create_task(download_picture(url, session, fname))

            tasks.append(task)

        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as ex:
            print(repr(ex))


if __name__ == "__main__":
    asyncio.run(main())
