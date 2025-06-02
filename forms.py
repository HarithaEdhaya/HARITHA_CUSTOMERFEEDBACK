from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=Feedback.CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'custom-dropdown'})
    )

    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(1, 6)],
        widget=forms.RadioSelect()
    )

    class Meta:
        model = Feedback
        fields = ['name', 'email', 'category', 'message', 'rating']
