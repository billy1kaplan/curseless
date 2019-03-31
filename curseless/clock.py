import asyncio


def clock(interval, messenger):
    """
    Creates an asyncronous clock
    for comsumption by the curseless
    main loop.

    The interval is interpreted in seconds.

    The messenger produces a message at the
    specified interval.
    """
    async def on_tick(observer):
        while True:
            await asyncio.sleep(interval)
            observer.notify(messenger.make_message())
    return on_tick
