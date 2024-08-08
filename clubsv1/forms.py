from django import forms

class UploadFileForm(forms.Form):
    ClubId = forms.UUIDField()
    BatchId = forms.UUIDField()
    file = forms.FileField()