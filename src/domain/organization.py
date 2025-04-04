from dataclasses import dataclass
import uuid


@dataclass(frozen=True)
class OrganizationEntity:
    name: str
    email: str
    id: uuid.UUID | None = None
    description: str | None = None
