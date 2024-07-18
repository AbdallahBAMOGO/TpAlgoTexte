from django import forms

class DocumentForm(forms.Form):
    document1 = forms.FileField(label='Document 1', widget=forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx,.txt'}))
    document2 = forms.FileField(label='Document 2', widget=forms.ClearableFileInput(attrs={'accept': '.pdf,.doc,.docx,.txt'}))