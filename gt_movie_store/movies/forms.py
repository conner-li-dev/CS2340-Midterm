from django import forms

class RatingForm(forms.Form):
    score = forms.TypedChoiceField(
        choices = [
            (1, "★"),
            (2, "★★"),
            (3, "★★★"),
            (4, "★★★★"),
            (5, "★★★★★"),
        ],
        coerce = int,
        widget = forms.RadioSelect,
        label = "Your rating:",
    )