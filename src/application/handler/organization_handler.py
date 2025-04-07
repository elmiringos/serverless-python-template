from http import HTTPStatus

from src.application.schemas.organization import (
    GetOrganizationRequest,
    CreateOrganizationRequest,
)
from src.application.service.organization_service import OrganizationService
from common.constants import ResponseStatus
from common.exception_handler import exception_handler
from common.exceptions import BadRequestException, EXCEPTIONS_IGNORING_ALERT, NotFoundException
from common.logger import get_logger
from common.utils import generate_lambda_response, format_response
from src.config import ALERTS_PROCESSOR

from pydantic import ValidationError

logger = get_logger(__name__)
exception_handler_default_args = {
    "ALERTS_PROCESSOR": ALERTS_PROCESSOR,
    "EXCEPTIONS_IGNORING_ALERT": EXCEPTIONS_IGNORING_ALERT,
    "logger": logger,
}


@exception_handler(**exception_handler_default_args)
def get_organization(event, context):
    """
    Handler function to get organization details.
    """
    try:
        request = GetOrganizationRequest.validate_event(event)
    except ValidationError as e:
        raise BadRequestException(str(e))

    result = OrganizationService().get_organization(request)
    if result is None:
        raise NotFoundException("No record found")

    response = format_response(ResponseStatus.SUCCESS, result.model_dump())

    return generate_lambda_response(HTTPStatus.OK, response, cors_enabled=True)


@exception_handler(**exception_handler_default_args)
def create_organization(event, context):
    """
    Handler function to create a new organization.
    """
    try:
        request = CreateOrganizationRequest.validate_event(event)
    except ValidationError as e:
        raise BadRequestException(str(e))

    result = OrganizationService().create_organization(request)
    response = format_response(ResponseStatus.SUCCESS, result)

    return generate_lambda_response(HTTPStatus.CREATED, response, cors_enabled=True)
