from django.shortcuts import render

from data_center.models import FlatPrerequisite


def prerequisite(request):
    return render(
        request,
        'table/prerequisites.html',
        {'data': FlatPrerequisite.objects.get()}
    )
