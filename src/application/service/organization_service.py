from typing import Dict
from common.exceptions import BadRequestException
from common.logger import get_logger
from src.application.schemas.organization import (
    CreateOrganizationRequest,
    GetOrganizationRequest,
    GetOrganizationResponse,
)
from src.domain.organization import OrganizationRepositoryAdapter

logger = get_logger(__name__)


class OrganizationService:
    organization_repo: OrganizationRepositoryAdapter

    def create_organization(self, organization_data: CreateOrganizationRequest) -> Dict[str, str]:
        organization_entity = organization_data.map_to_entity()

        try:
            organization = self.organization_repo.insert_organization(organization_entity)
        except UnboundLocalError as e:
            logger.error(f"Repository is not implemented: {e}")
            raise BadRequestException("Unable to create organization")

        return {"status": "success", "data": str(organization)}

    def get_organization(self, request: GetOrganizationRequest) -> GetOrganizationResponse:
        organization = self.organization_repo.get_organization(request.organization_id)
        if not organization:
            raise BadRequestException("Organization not found")

        return GetOrganizationResponse.from_entity(organization)
