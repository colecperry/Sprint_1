import enum

class UserRole(str, enum.Enum):
    """Enumeration for user roles."""
    ADMIN = "admin"
    CASE_WORKER = "case_worker"

class GenderEnum(str, enum.Enum):
    """Enumeration for gender categories."""
    MALE = "male"
    FEMALE = "female"
