from rest_framework import permissions

class IsSeller(permissions.BasePermission):
    """
    Allows access only to users in the 'Seller' group.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Seller').exists()

class IsCustomer(permissions.BasePermission):
    """
    Allows access only to users in the 'Customer' group.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.groups.filter(name='Customer').exists()

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'store'):
             if hasattr(obj.store, 'owner'):
                 return obj.store.owner == request.user
        
        return False

class IsStoreOwner(permissions.BasePermission):
    """
    Custom permission for store checking. 
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        return False
