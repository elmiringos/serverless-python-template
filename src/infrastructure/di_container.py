from rodi import Container
from src.infrastructure.repositories.organization_repository import OrganizationRepository
from src.domain.organization import OrganizationRepositoryAdapter
from src.application.service.organization_service import OrganizationService

container = Container()

container.register(OrganizationRepositoryAdapter, OrganizationRepository)
container.register(OrganizationService, OrganizationService)
