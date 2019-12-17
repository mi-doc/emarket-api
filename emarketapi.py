import asyncio
import aiohttp
import sys
from prettytable import PrettyTable
from concurrent.futures import FIRST_COMPLETED


URL = 'https://emarket-shop.herokuapp.com/api/products-list'


def prettyprint(products):
    """
    This func creates nice ASCII-based sheet to display data in terminal
    """
    keys = products[1].keys()
    table = PrettyTable(keys)
    for product in products:
        vals = [product[key] for key in keys]
        table.add_row(vals)
    print(table)


async def fetch_product_list(keys):
    """
    Asynchorously fetching products with specified params from emarket api
    :param keys: product params required to fetch (name, price, ram etc)
    """
    query = '*'.join(keys)     # name*price*processor
    params = {'q': query}
    async with aiohttp.ClientSession() as session:
        async with session.get(URL, params=params) as r:
            return await r.json()


async def timer(sec=10):
    """
    Prints seconds. It makes no real sense, just playing with asynchronous.
    """
    for s in range(sec):
        print(s)
        await asyncio.sleep(1)


async def main(keys):
    task_fetch = asyncio.ensure_future(fetch_product_list(keys))
    task_timer = asyncio.ensure_future(timer())
    tasks = [task_timer, task_fetch]

    while True:
        # Waiting untill products are fetched from emarket.
        done, pending = await asyncio.wait(tasks, return_when=FIRST_COMPLETED)
        if task_fetch in done:
            break

    # Cancel coroutine with timer.
    for future in pending:
        future.cancel()

    products = task_fetch.result()
    prettyprint(products)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        keys = sys.argv[1:]
    else:
        keys = ['name']

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(keys))
    loop.close()
