from common.utils import generate_lambda_response

def health_check_handler(event, context):
    # Here, you would typically check the status of your application's dependencies
    # For demonstration, we'll assume all services are operational
    health_status = {
        'status': 'ok',
        'services': {
            'database': 'operational',
            'external_api': 'operational'
        }
    }
    
    # Generate a response using the utility function
    return generate_lambda_response(200, health_status)