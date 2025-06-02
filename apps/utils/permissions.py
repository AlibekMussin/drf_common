# Vendor
from rest_framework.permissions import BasePermission
from rest_framework import status

# Local
# from . import utils as utils
from ..utils.exceptions import CustomException


class MixedPermission:
    """ Миксин permissions для action
    """
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]

