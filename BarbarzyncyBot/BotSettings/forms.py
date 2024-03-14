# w pliku forms.py w twojej aplikacji
from django import forms

class BotTokenForm(forms.Form):
    DISCORD_BOT_TOKEN = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Token Discord Bot', required=True)

class ServerIDForm(forms.Form):
    GUILD_ID = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Serwer',
        required=True
    )

    def __init__(self, *args, **kwargs):
        guilds = kwargs.pop('guilds', None)
        super(ServerIDForm, self).__init__(*args, **kwargs)
        if guilds:
            self.fields['GUILD_ID'].choices = guilds

class ChannelsSettingsForm(forms.Form):
    RECRUITMENT_CHANNEL_ID = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}), label='Kanał Rekrutacyjny', required=True)
    RECRUITMENT_CATEGORY_ID = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}), label='Kategoria Rekrutacyjna', required=True)
    ACCEPTED_CHANNEL_ID = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}), label='Zaakceptowane', required=True)
    DECLINED_CHANNEL_ID = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}), label='Odrzucone', required=True)
    NO_RESPONSE_CHANNEL_ID = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}), label='Bez odpowiedzi', required=True)

    def __init__(self, *args, **kwargs):
        channels = kwargs.pop('channels', None)
        categories = kwargs.pop('categories', None)
        super(ChannelsSettingsForm, self).__init__(*args, **kwargs)
        if channels:
            self.fields['RECRUITMENT_CHANNEL_ID'].choices = channels
            self.fields['RECRUITMENT_CATEGORY_ID'].choices = categories
            self.fields['ACCEPTED_CHANNEL_ID'].choices = channels
            self.fields['DECLINED_CHANNEL_ID'].choices = channels
            self.fields['NO_RESPONSE_CHANNEL_ID'].choices = channels

class RolesSettingsForm(forms.Form):
    OFFICER_ROLE_ID = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}), label='Rola Oficera', required=True)

    def __init__(self, *args, **kwargs):
        roles = kwargs.pop('roles', None)
        super(RolesSettingsForm, self).__init__(*args, **kwargs)
        if roles:
            self.fields['OFFICER_ROLE_ID'].choices = roles
