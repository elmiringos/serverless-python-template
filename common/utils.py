import json
import uuid

from common.constants import ResponseStatus


def format_response(status, response: dict):
    if status == ResponseStatus.SUCCESS:
        return {"status": status, "data": response}
    elif status == ResponseStatus.FAILED:
        error_data = {
            "code": response.get("code", 0000),
            "message": response.get("message", "Unexpected error"),
            "details": response.get("details", {}),
        }
        return {"status": status, "error": error_data}
    else:
        return {}


def custom_serializer(obj):
    """
    Custom serializer function to convert non-serializable types to a JSON-compatible format.
    """
    if isinstance(obj, uuid.UUID):
        return str(obj)


def generate_lambda_response(
    http_code: int, data: dict | str | list, headers: dict | None = None, cors_enabled: bool = False
):
    response = {
        "statusCode": http_code,
        "body": json.dumps(data, default=custom_serializer) if isinstance(data, dict) else data,
        "headers": {"Content-Type": "application/json"},
    }
    if cors_enabled:
        allow_headers = [
            "Access-Control-Allow-Origin",
            "Authorization",
            "X-Refresh-Token",
            "Content-Type",
            "X-Amz-Date",
            "X-Api-Key",
            "X-Requested-With",
            "Origin",
        ]
        expose_headers = ["Authorization", "X-Refresh-Token", "X-Amzn-Remapped-Authorization"]
        allow_methods = ["GET", "OPTIONS", "PUT", "POST", "DELETE"]
        response["headers"].update(
            {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": "true",
                "Access-Control-Allow-Headers": ",".join(allow_headers),
                "Access-Control-Expose-Headers": ",".join(expose_headers),
                "Access-Control-Allow-Methods": ",".join(allow_methods),
                "X-Requested-With": "*",
            }
        )
    if headers is not None:
        response["headers"].update(headers)
    return response
