import uuid
from sqlalchemy import delete, insert, select, update
from src.infrastructure.repositories.base_repository import BaseRepository
from src.domain.organization import OrganizationEntity
from src.infrastructure.models import Organization
from common.logger import get_logger

logger = get_logger(__name__)


class OrganizationRepository(BaseRepository):
    @BaseRepository.write_ops
    def insert_organization(self, organization_entity: OrganizationEntity) -> uuid.UUID:
        """Inserts a new organization and returns its UUID."""
        query = (
            insert(Organization)
            .values(
                id=uuid.uuid4(),
                name=organization_entity.name,
                email=organization_entity.email,
                description=organization_entity.description,
            )
            .returning(Organization.id)
        )

        result = self.session.execute(query)
        new_org_id = result.scalar_one()
        self.session.commit()
        return uuid.UUID(new_org_id)

    def get_organization(self, organization_id: uuid.UUID) -> OrganizationEntity | None:
        """Fetches an organization by ID and maps it to OrganizationEntity."""
        query = select(Organization).where(Organization.id == organization_id)
        result = self.session.execute(query)
        db_organization = result.scalar_one_or_none()

        if db_organization is None:
            return None

        return OrganizationEntity(
            id=uuid.UUID(db_organization.id),
            name=db_organization.name,
            email=db_organization.email,
            description=db_organization.description,
        )

    @BaseRepository.write_ops
    def update_organization(
        self,
        organization_id: uuid.UUID,
        name: str | None = None,
        email: str | None = None,
        description: str | None = None,
    ) -> OrganizationEntity:
        """Updates an organization and returns the updated entity."""
        update_values = {}

        if name is not None:
            update_values["name"] = name
        if email is not None:
            update_values["email"] = email
        if description is not None:
            update_values["description"] = description

        if not update_values:
            raise ValueError("At least one field (name, email, or description) must be provided")

        query = (
            update(Organization)
            .where(Organization.id == organization_id)
            .values(**update_values)
            .returning(Organization)
        )

        result = self.session.execute(query).scalar_one()
        self.session.commit()

        return OrganizationEntity(
            id=uuid.UUID(result.id),
            name=result.name,
            email=result.email,
            description=result.description,
        )

    @BaseRepository.write_ops
    def delete_organization(self, organization_id: uuid.UUID):
        """Deletes an organization by ID."""
        query = delete(Organization).where(Organization.id == organization_id)
        self.session.execute(query)
