from django.db.models import Q
from .models import Business


def get_user_businesses(user):
    """Businesses the user owns or is a staff member of."""
    return Business.objects.filter(
        Q(owner=user) | Q(memberships__user=user)
    ).distinct()


def get_user_role(business, user):
    if business.owner_id == user.id:
        return 'owner'
    membership = business.memberships.filter(user=user).first()
    return membership.role if membership else None


def user_can_access_business(business, user):
    return get_user_role(business, user) is not None
