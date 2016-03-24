from django import forms


class TweetForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'cols': 85,
                                                        'rows': 1,
                                                        'class': 'form-control'
                                                        })
                           , max_length=160)
    country = forms.CharField(widget=forms.HiddenInput(), required=False)

