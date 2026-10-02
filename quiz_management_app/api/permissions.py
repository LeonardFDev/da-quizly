"""Permission classes for API access control for quizzes."""

from rest_framework.permissions import BasePermission


class QuizPermission(BasePermission):
    """Permission for quiz API access."""

    def has_permission(self, request, view):
        is_authenticated = request.user.is_authenticated
        return is_authenticated

    def has_object_permission(self, request, view, obj):
        is_owner = self.check_owner(request, obj)

        if view.action in ("retrieve", "partial_update", "destroy"):
            return is_owner
        
        return True
    
    def check_owner(self, request, obj):
        """checks whether the logged in user is the owner of the quiz"""
        request_user = request.user
        is_owner = obj.owner == request_user

        return is_owner