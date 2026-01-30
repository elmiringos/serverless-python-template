from common.utils import format_response


def health_check_handler() -> dict:
    """
    Health check handler to verify the service status.

    Returns:
        dict: A formatted response indicating the health status.
    """
    # The health check logic can be extended as needed, for now, it returns a simple success message.
    status = {
        'status': 'healthy',
        'message': 'Service is running smoothly'
    }
    return format_response(status, 200)
