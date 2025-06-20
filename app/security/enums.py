from enum import Enum

class UserRole(str, Enum):
    superuser = "superuser"
    admin = "admin"
    manager = "manager"
    user = "user"
    