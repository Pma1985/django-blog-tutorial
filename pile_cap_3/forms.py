from django import forms

class InputForm(forms.Form):
    project = forms.CharField(required=False)
    job = forms.CharField(required=False)
    version = forms.CharField(required=False)
    designer = forms.CharField(required=False)
    checked = forms.CharField(required=False)
    approved = forms.CharField(required=False)
    date1 = forms.CharField(required=False)
    date2 = forms.CharField(required=False)
    date3 = forms.CharField(required=False)

    fc = forms.FloatField(initial=40, min_value=0.0)
    fy = forms.FloatField(initial=415, min_value=0.0)
    gamma = forms.FloatField(initial=24, min_value=0.0)

    Cx = forms.FloatField(initial=600, min_value=0.0)
    Cy = forms.FloatField(initial=400, min_value=0.0)

    dp = forms.FloatField(initial=450, min_value=0.0)
    S = forms.FloatField(initial=1350, min_value=0.0)
    H = forms.FloatField(initial=900, min_value=250)
    c = forms.FloatField(initial=175, min_value=175)
    e = forms.FloatField(initial=500, min_value=250)
    t = forms.FloatField(initial=50, min_value=0.0)
    Pc = forms.FloatField(initial=750, min_value=0.0)
    Pt = forms.FloatField(initial=-500, max_value=0)


    Fzd = forms.FloatField(initial=1250)
    Myd = forms.FloatField(initial=0)
    Mxd = forms.FloatField(initial=0)

    Fzl = forms.FloatField(initial=425)
    Myl = forms.FloatField(initial=0)
    Mxl = forms.FloatField(initial=0)

    Fzw = forms.FloatField(initial=0)
    Myw = forms.FloatField(initial=0)
    Mxw = forms.FloatField(initial=0)

    Fze = forms.FloatField(initial=0)
    Mye = forms.FloatField(initial=0)
    Mxe = forms.FloatField(initial=0)