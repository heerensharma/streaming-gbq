from queue_monitor.monitoring import check_queue_size


# Checking queue size checker based on threshold value specified in QUEUE_LIMIT config var
def test_check_queue_size():
    assert check_queue_size(10) == "Queue health checks passed"
    assert check_queue_size(157) == "ALERT: QUEUE FILLING UP -> 157"
    assert check_queue_size(100) == "Queue health checks passed"
