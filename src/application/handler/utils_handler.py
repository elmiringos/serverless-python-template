from common.utils import generate_lambda_response
from common.exception_handler import exception_handler
import logging

logger = logging.getLogger(__name__)

@exception_handler
def health_handler(event, context):
    """
    Health check handler that returns the health status of the service.
    """
    logger.info("Performing health check.")
    
    # Simple health check logic
    health_status = {
        'status': 'healthy',
        'message': 'Service is running smoothly.'
    }
    
    logger.info("Health check passed.")
    return generate_lambda_response(200, health_status)
