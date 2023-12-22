from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["HEAD", "OPTIONS"]:
            return True

        return obj.user == request.user


class JWTCookieAuthenticated(BasePermission):
    def has_permission(self, request, view):
        cookie = request.COOKIES.get("access_token")

        if not cookie:
            return False

        try:
            access_token = AccessToken(cookie)
        except:
            return False

        return True


class JWTCookieIsOwnerorReadOnly(BasePermission):
    def has_permission(self, request, view):
        cookie = request.COOKIES.get("access_token")

        if not cookie:
            return False

        try:
            access_token = AccessToken(cookie)
        except:
            return False

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        user = get_user_id(request)

        return obj.user.pk == user


def get_user_id(request):
    token = AccessToken(request.COOKIES.get("access_token"))
    user_id = token.payload["user_id"]
    return user_id

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user