from src.application.handler.utils_handler import health_check_handler

def test_health_check_handler_healthy():
    status, code = health_check_handler()
    assert status['status'] == 'healthy'
    assert code == 200

# Additional tests can be added for different scenarios
# def test_health_check_handler_unhealthy():
#     # Simulate a failure condition
#     pass
