from django import forms


class TweetForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(attrs={'cols': 85,
                                                        'rows': 1,
                                                        'class': 'form-control post-tweet',
                                                        'id': 'tweet',
                                                        'placeholder': 'Опубликовать новый твит'
                                                        })
                           , max_length=160)
    country = forms.CharField(widget=forms.HiddenInput(attrs={'class': 'form-control', 'id': 'country'}), required=False)

    def __unicode__(self):
        return self.text


class SearchForm(forms.Form):
    query = forms.CharField(label="Введите слово для поиска:",
                            widget=forms.TextInput(attrs={'class': 'form-control search-query'}))