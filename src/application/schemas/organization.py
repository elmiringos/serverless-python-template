import json
import uuid
from src.application.schemas.common import PayloadValidationError
from src.domain.organization import OrganizationEntity
from pydantic import BaseModel, Field, EmailStr


class CreateOrganizationRequest(BaseModel):
    name: str
    email: EmailStr
    description: str | None = Field(default=None)

    @classmethod
    def validate_event(cls, event):
        try:
            assert event.get("body") is not None, "Invalid event body"
            body = json.loads(event["body"])
            return cls.model_validate(body)
        except (AssertionError, json.JSONDecodeError):
            raise PayloadValidationError()

    def map_to_entity(self) -> OrganizationEntity:
        """
        Maps the request data to an entity.
        """
        return OrganizationEntity(
            name=self.name,
            email=self.email,
            description=self.description,
        )


class GetOrganizationRequest(BaseModel):
    organization_id: uuid.UUID

    @classmethod
    def validate_event(cls, event):
        try:
            assert event.get("pathParameters") is not None, "Invalid event path parameters"
            path_parameters = event["pathParameters"]
            assert path_parameters.get("organization_id") is not None, "Missing organization ID"
            return cls.model_validate(path_parameters)
        except (AssertionError, json.JSONDecodeError):
            raise PayloadValidationError()


class GetOrganizationResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    description: str | None = Field(default=None)

    @classmethod
    def from_entity(cls, entity: OrganizationEntity) -> "GetOrganizationResponse":
        return cls(
            id=str(entity.id),
            name=entity.name,
            email=entity.email,
            description=entity.description,
        )
