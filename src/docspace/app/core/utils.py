from django.http import HttpResponse, HttpResponseForbidden
from io import StringIO


def df_to_file(df):
    f = StringIO()
    df.to_csv(f, index=False)
    f.seek(0)
    return f


def queryset_to_df(queryset, values=[]):
    f = StringIO()
    queryset.to_csv(f, *values)
    f.seek(0)
    return pd.read_csv(f)


def download_file(request, f, name, content_type='application/pdf'):
    response = HttpResponse(f.read(), content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=' + name
    return response