from django.contrib.auth.mixins import UserPassesTestMixin


class OwnerOrStaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        u = self.request.user
        return u.is_authenticated and (u.is_staff or u.is_superuser or obj.organizer_id == u.id)