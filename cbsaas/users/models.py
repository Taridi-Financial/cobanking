from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models

from cbsaas.cin.models import CINRegistry
class User(AbstractUser):
    """
    Default custom user model for cbsaas.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    email = models.CharField(max_length=255)
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    # username = None  # type: ignore
    USERNAME_FIELD: email
    cin = models.OneToOneField(CINRegistry, on_delete=models.SET_NULL, blank=True, null=True)

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
