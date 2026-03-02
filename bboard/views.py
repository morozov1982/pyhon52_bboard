from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy, reverse
from django.views.generic.base import View, TemplateView
from django.views.generic import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.decorators.http import require_GET, require_POST, require_safe, require_http_methods

from bboard.forms import BbForm, RubricFormSet, SearchForm
from bboard.models import Bb, Rubric


def index(request):
    # rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)

    bbs = Bb.objects.all()
    paginator = Paginator(bbs, 2)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)

    # context = {'bbs': page.object_list, 'page': page, 'rubrics': rubrics}
    context = {'bbs': page.object_list, 'page': page}
    return render(request, 'index.html', context)


def by_rubric(request, rubric_id):
    # bbs = get_list_or_404(Bb, rubric_id)
    bbs = Bb.objects.filter(rubric=rubric_id)
    # rubrics = Rubric.objects.all()
    # rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric':current_rubric}

    return render(request, 'by_rubric.html', context)


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


# @require_GET()
# @require_POST()
# @require_safe()
@require_http_methods(['GET', 'POST'])
def add_and_save(request):
    if request.method == 'POST':
        bbf = BbForm(request.POST)

        if bbf.is_valid():
            if bbf.has_changed():
                bbf.save()
            return HttpResponseRedirect(reverse(
                'bboard:by_rubric',
                kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf}
            return render(request, 'create.html', context)
    else:
        bbf = BbForm()
        # bbf = BbForm(initial={'price': 1000.0})
        context = {'form': bbf}
        return render(request, 'create.html', context)


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


# class BbCreateView(View):
#     def get(self, request, *args, **kwargs):
#         form = BbForm()
#         context = {'form': form, 'rubrics': Rubric.objects.all()}
#         return render(request, 'create.html', context)
#
#     def post(self, request, *args, **kwargs):
#         form = BbForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse(
#                 'bboard:by_rubric',
#                 kwargs={'rubric_id': form.cleaned_data['rubric'].pk}))
#         else:
#             context = {'form': form, 'rubrics': Rubric.objects.all()}
#             return render(request, 'create.html', context)


class BbCreateView(CreateView):
# class BbCreateView(LoginRequiredMixin, CreateView):
# class BbCreateView(UserPassesTestMixin, CreateView):
# class BbCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'create.html'
    form_class = BbForm
    initial = {'price': 0}
    success_url = '/'
    # permission_required = ('bboard.add_bb', 'bboard.change_bb')

    # def test_func(self):
    #     return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        return context


class BbUpdateView(UpdateView):
    model = Bb
    template_name = 'bboard/bb_form.html'
    form_class = BbForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = '/{rubric_id}/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        return context


# class BbRubricBbsView(TemplateView):
#     template_name = 'by_rubric.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
#         context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
#         context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
#         return context


class BbRubricBbsView(ListView):
    template_name = 'by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context


def bb_detail(request, bb_id):
    bb = get_object_or_404(Bb, pk=bb_id)

    # rubrics = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
    context = {'bb': bb, 'rubrics': rubrics}

    return render(request, 'bb_detail.html', context)


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['rubrics'] = Rubric.objects.annotate(cnt=Count('bb')).filter(cnt__gt=0)
        return context


def rubrics(request):
    if request.method == 'POST':
        formset = RubricFormSet(request.POST)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                if form.cleaned_data:
                    rubric = form.save(commit=False)
                    if rubric in formset.deleted_objects:
                        rubric.delete()
                    else:
                        if form['ORDER'].data:
                            rubric.order = form['ORDER'].data
                        rubric.save()

            return redirect('bboard:index')
    else:
        formset = RubricFormSet()
    context = {'formset': formset}
    return render(request, 'bboard/rubrics.html', context)


# @login_required
# @login_required(login_url='/login/')
# @user_passes_test(lambda user: user.is_staff)
# @permission_required('bboard.add_rubric')
# @permission_required(('bboard.add_rubric', 'bboard.add_bb'))
def bbs(request, rubric_id):
    BbsFormSet = inlineformset_factory(Rubric, Bb, form=BbForm, extra=1)
    rubric = Rubric.objects.get(pk=rubric_id)
    if request.method == 'POST':
        formset = BbsFormSet(request.POST, instance=rubric)
        if formset.is_valid():
            formset.save()
            return redirect('bboard:index')
    else:
        formset = BbsFormSet(instance=rubric)
    context = {'formset': formset, 'current_rubric': rubric}
    return render(request, 'bboard/bbs.html', context)


def search(request):
    if request.method == 'POST':
        sf = SearchForm(request.POST)
        if sf.is_valid():
            keyword = sf.cleaned_data['keyword']
            rubric_id = sf.cleaned_data['rubric'].pk
            # bbs = Bb.objects.filter(title__icontains=keyword,
            #                         rubric=rubric_id)
            bbs = Bb.objects.filter(title__iregex=keyword,
                                    rubric=rubric_id)
            context = {'bbs': bbs, 'form': sf}
            return render(request, 'bboard/search.html', context)
    else:
        sf = SearchForm()
    context = {'form': sf}
    return render(request, 'bboard/search.html', context)
