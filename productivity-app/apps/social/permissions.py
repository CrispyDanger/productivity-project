from rest_framework.permissions import BasePermission


class isPostAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user.socialprofile


class isCommentAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.created_by == request.user.socialprofile
