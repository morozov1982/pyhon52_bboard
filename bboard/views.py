from django.db.models import Count
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView

from bboard.forms import BbForm
from bboard.models import Bb, Rubric

# def index(request):
#     # template = loader.get_template('index.html')
#     bbs = Bb.objects.all()
#     # rubrics = Rubric.objects.all()
#     rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#     context = {'bbs': bbs, 'rubrics': rubrics}
#
#     # return HttpResponse(template.render(context, request))
#     return render(request, 'index.html', context)


# def index(request):
#     resp = HttpResponse('Здесь будет', content_type='text/plain; charset=utf-8')
#     resp.writelines((' страница', ' сайта'))
#     resp['keywords'] = 'Python, Django'
#     return resp

# def index(request):
#     bbs = Bb.objects.all()
#     rubrics = Rubric.objects.all()
#     context = {'bbs': bbs, 'rubrics': rubrics}
#     template = get_template('index.html')
#     return HttpResponse(template.render(context, request))


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs, 'rubrics': rubrics}
    return HttpResponse(render_to_string('index.html', context, request))


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    # rubrics = Rubric.objects.all()
    rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric':current_rubric}

    return render(request, 'by_rubric.html', context)


# class BbCreateView(CreateView):
#     template_name = 'create.html'
#     form_class = BbForm
#     # success_url = '/'
#     success_url = reverse_lazy('index')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # context['rubrics'] = Rubric.objects.all()
#         context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#         return context


def add(request):
    bbf = BbForm()
    context = {'form': bbf}
    return render(request, 'create.html', context)


def add_save(request):
    bbf = BbForm(request.POST)

    if bbf.is_valid():
        bbf.save()
        return HttpResponseRedirect(reverse(
            'bboard:by_rubric',
            kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
    else:
        context = {'form': bbf}
        return render(request, 'create.html', context)


def add_and_save(request):
    if request.method == 'POST':
        bbf = BbForm(request.POST)

        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse(
                'bboard:by_rubric',
                kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'create.html', context)
    else:
        bbf = BbForm()
        context = {'form': bbf}
        return render(request, 'create.html', context)
