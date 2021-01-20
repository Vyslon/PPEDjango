from django.forms import ModelForm
from .models import LigneFraisHorsForfait


class LigneFraisHorsForfaitForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.mois = kwargs.pop('mois', None)
        super(LigneFraisHorsForfaitForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LigneFraisHorsForfait
        fields = ('libelle', 'date', 'montant')

    def clean(self):
        cleaned_data = self.cleaned_data
        date = cleaned_data.get('date')
        if date is not None:
            annee_fiche = self.mois[0:4]
            mois_fiche = self.mois[4:6]
            if (date.strftime("%Y") != annee_fiche) or (date.strftime("%m") != mois_fiche):
                msg = "La date d'engagement doit être valide."
                self.add_error('date', msg)
        return super().clean()
