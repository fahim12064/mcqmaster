from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    """
    This is a custom authentication backend.
    It allows users to log in using their email address or username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # username ভেরিয়েবলে যা আসছে (ইমেইল বা ইউজারনেম) তা দিয়ে ইউজার খোঁজা হবে
        try:
            # Q object ব্যবহার করে username অথবা email ফিল্ডে ম্যাচ খোঁজা হচ্ছে
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except User.DoesNotExist:
            # কোনো ইউজার খুঁজে না পেলে None রিটার্ন করা হবে
            return None
        except User.MultipleObjectsReturned:
            # যদি একই ইমেইল/ইউজারনেম দিয়ে একাধিক ইউজার থাকে (যা হওয়া উচিত নয়)
            user = User.objects.filter(Q(username__iexact=username) | Q(email__iexact=username)).order_by('id').first()

        # পাসওয়ার্ড চেক করা হচ্ছে এবং ইউজার অবজেক্ট রিটার্ন করা হচ্ছে
        if user and user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
