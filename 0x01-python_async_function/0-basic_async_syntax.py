#!/usr/bin/env python3

import random 
import asyncio

""" Write an asynchronous coroutine that takes in an integer argument that waits for a random time 
    before it returns it
"""

async def wait_random(max_delay=10, type=float):
    await asyncio.sleep(random.randint(0, max_delay))
    return max_delay