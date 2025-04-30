from abc import ABC, abstractmethod
from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class OrganizationEntity:
    name: str
    email: str
    id: uuid.UUID | None = None
    description: str | None = None


class OrganizationRepositoryAdapter(ABC):
    @abstractmethod
    def insert_organization(self, organization_entity: OrganizationEntity) -> uuid.UUID:
        pass

    @abstractmethod
    def get_organization(self, organization_id: uuid.UUID) -> OrganizationEntity | None:
        pass

    @abstractmethod
    def update_organization(
        self,
        organization_id: uuid.UUID,
        name: str | None = None,
        email: str | None = None,
        description: str | None = None,
    ) -> OrganizationEntity:
        pass

    @abstractmethod
    def delete_organization(self, organization_id: uuid.UUID) -> None:
        pass
