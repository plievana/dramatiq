from functools import reduce

from dramatiq.middleware import CurrentMessage
from dramatiq.results import ResultTimeout
from flask import current_app
import time
import random
from app import dramatiq, cache
from dramatiq.rate_limits import ConcurrentRateLimiter
from dramatiq.rate_limits.backends import RedisBackend


@dramatiq.actor
def test():
    current_app.logger.info('test actor')


@dramatiq.actor(max_retries=0)
def single_task(name: str, duration: int):
    current_app.logger.info(f'[{name}] Starting single-task of {duration} secs')
    for i in range(duration):
        current_app.logger.info(f'[{name}] ... Current value {i}')
        time.sleep(1)
    current_app.logger.info(f'[{name}] Finishing single-task')


@dramatiq.actor(max_retries=0)
def parent_task(name: str, n_subtasks: int):
    current_app.logger.info(f'[{name}] Starting parent-task with {n_subtasks} subtasks')
    t1 = time.time()
    pipe = dramatiq.pipeline(
        (
            create_subtasks.message(name, n_subtasks),
            close_task.message_with_options(pipe_ignore=True, kwargs=dict(name=name, started=t1))
        )
    ).run()


@dramatiq.actor(max_retries=0, store_results=True)
def run_subtask(msg_id, parent_name: str, i: int):
    try:
        to_sleep = random.randint(1, 5)
        current_app.logger.info(f'[{parent_name}] ... [{i}] Starts ({to_sleep})')
        time.sleep(to_sleep)
        current_app.logger.info(f'[{parent_name}] ... [{i}] Ends ({to_sleep})')
        return to_sleep
    finally:
        cache.decr(msg_id, 1)


@dramatiq.actor(max_retries=0, store_results=True)
def create_subtasks(parent_name: str, n_subtasks):
    msg_id = CurrentMessage.get_current_message().message_id
    cache.set(msg_id, n_subtasks)
    current_app.logger.info(f'[{parent_name}] Creating subtasks')
    g = dramatiq.group(
        (run_subtask.message(msg_id, parent_name, i) for i in range(n_subtasks))
    ).run()

    while int(cache.get(msg_id)) > 0:
        try:
            g.wait(timeout=10_000)
            res = g.get_results()
            total = reduce(lambda x, y: x + y, res)
        except ResultTimeout:
            current_app.logger.warn(f'[{parent_name}] timeout')

    current_app.logger.info(f'[{parent_name}] Subtasks created. Should take {total} seconds')
    return None


@dramatiq.actor(max_retries=0)
def close_task(name: str, started: time):
    current_app.logger.info(f'[{name}] Finished parent-task in {time.time() - started} secs')


@dramatiq.actor()
def one_at_a_time(locker):
    backend = RedisBackend()
    mutex = ConcurrentRateLimiter(backend, f"locker::{locker}", limit=1)
    with mutex.acquire():
        current_app.logger.info(f"[{locker}] - Starts")
        time.sleep(20)
        current_app.logger.info(f"[{locker}] - Done")
