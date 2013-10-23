from datetime import *

def ticks_since_epoch(start_time = datetime.utcnow()):
    ticks_per_ms = 10000
    ms_per_second = 1000
    ticks_per_second = ticks_per_ms * ms_per_second
    span = start_time - datetime(1, 1, 1)
    ticks = str(span.total_seconds() * ticks_per_second)
    return ticks


