from django import forms

class InvitionForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'size': 32,
                                                          'placeholder': 'Введите Email друга',
                                                          'class': 'form-control'}
                                                   )
                            )


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Введите имя пользователя',
                                                             'class': 'form-control'
                                                             }
                                                      ),
                               required=True
                               )
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput)