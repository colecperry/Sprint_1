import enum


class UserRole(str, enum.Enum):
    """Enumeration for user roles."""

    ADMIN = "admin"
    CASE_WORKER = "case_worker"
    CLIENT = "client"


class GenderEnum(str, enum.Enum):
    """Enumeration for gender categories."""

    MALE = 1
    FEMALE = 2
