from django.shortcuts import redirect


class SubscriptionRequiredMixin:
    """Verify that the current user has subscription."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.subscription.is_active():
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('billing')
