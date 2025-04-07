from typing import Dict
from common.exceptions import BadRequestException
from src.infrastructure.repositories.organization_repository import OrganizationRepository
from src.application.schemas.organization import (
    CreateOrganizationRequest,
    GetOrganizationRequest,
    GetOrganizationResponse,
)


class OrganizationService:
    def __init__(self) -> None:
        self.organization_repo = OrganizationRepository()

    def create_organization(self, organization_data: CreateOrganizationRequest) -> Dict[str, str]:
        organization_entity = organization_data.map_to_entity()
        organization = self.organization_repo.insert_organization(organization_entity)

        return {"status": "success", "data": str(organization)}

    def get_organization(self, request: GetOrganizationRequest) -> GetOrganizationResponse:
        organization = self.organization_repo.get_organization(request.organization_id)
        if not organization:
            raise BadRequestException("Organization not found")

        return GetOrganizationResponse.from_entity(organization)
