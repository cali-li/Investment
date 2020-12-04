from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from invests.models import Invest, Type
# from invests.forms import DateForm
# from bootstrap_datepicker_plus import DateTimePickerInput

from django.db.models import Sum
from django.http import JsonResponse

# Create your views here.

def home(request):
    return render(request, 'invests/home.html', ctx)

def invest_chart(request):
    labels = []
    data = []

    queryset = Invest.objects.values('date').annotate(date_invest=Sum('invest')).order_by('-date_invest')
    for entry in queryset:
        labels.append(entry['date'])
        data.append(entry['date_invest'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
def invest_chart2(request):
    labels = []
    data = []

    # queryset2 = Invest.objects.all()
    queryset = Invest.objects.values('type').annotate(type_invest=Sum('invest')).order_by('-type')
    queryset2 = Type.objects.values('name').order_by('-id')

    for entry in queryset2:
    #     for key, value in model_to_dict(report).iteritems():
    #         if entry.type == report.type.pk:
    #             print key, value
    # for entry in Type.objects.all():
        labels.append(entry['name'])
    for entry in queryset:
        # for i in type_id:
        # for report in queryset2:
        #     if entry['type'] == report.type.pk:
        #         labels.append(report.type.name)

        # labels.append(entry['type_name'])
        data.append(entry['type_invest'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
class MainView(LoginRequiredMixin, View):
    def get(self, request):
        mc = Type.objects.all().count()
        al = Invest.objects.all()

        ctx = {'type_count': mc, 'invest_list': al}
        return render(request, 'invests/home.html', ctx)

class InvestView(LoginRequiredMixin, View):
    def get(self, request):
        mc = Type.objects.all().count()
        al = Invest.objects.all()

        ctx = {'type_count': mc, 'invest_list': al}
        return render(request, 'invests/invest_list.html', ctx)

class TypeView(LoginRequiredMixin, View):
    def get(self, request):
        ml = Type.objects.all()
        ctx = {'type_list': ml}
        return render(request, 'invests/type_list.html', ctx)


# We use reverse_lazy() because we are in "constructor attribute" code
# that is run before urls.py is completely loaded

class TypeCreate(LoginRequiredMixin, CreateView):
    model = Type
    fields = '__all__'
    success_url = reverse_lazy('invests:all')


class TypeUpdate(LoginRequiredMixin, UpdateView):
    model = Type
    fields = '__all__'
    success_url = reverse_lazy('invests:all')


class TypeDelete(LoginRequiredMixin, DeleteView):
    model = Type
    fields = '__all__'
    success_url = reverse_lazy('invests:all')




# Take the easy way out on the main table
# These views do not need a form because CreateView, etc.
# Build a form object dynamically based on the fields
# value in the constructor attributes
class InvestCreate(LoginRequiredMixin, CreateView):
    model = Invest
    fields = '__all__'
    success_url = reverse_lazy('invests:all')
    # def get_form(self):
    #     form = super().get_form()
    #     form.fields['date'].widget = DateTimePickerInput()
    #     return form
    # def get(self, request, pk) :
    #     x = Invest.objects.get(id=pk)
    #     # comments = Type.objects.filter(invest=x).order_by('-updated_at')
    #     date_form = DateForm()
    #     context = { 'invest' : x,  'date_form': date_form }

    # def get_form(self):
    #     '''add date picker in forms'''
    #     from django.forms.extras.widgets import SelectDateWidget
    #     form = super(EnvironmentCreateView, self).get_form()
    #     form.fields['date'].widget = SelectDateWidget()
    #     return form

class InvestUpdate(LoginRequiredMixin, UpdateView):
    model = Invest
    fields = '__all__'
    success_url = reverse_lazy('invests:all')


class InvestDelete(LoginRequiredMixin, DeleteView):
    model = Invest
    fields = '__all__'
    success_url = reverse_lazy('invests:all')

# We use reverse_lazy rather than reverse in the class attributes
# because views.py is loaded by urls.py and in urls.py as_view() causes
# the constructor for the view class to run before urls.py has been
# completely loaded and urlpatterns has been processed.

# References

# https://docs.djangoproject.com/en/3.0/ref/class-based-views/generic-editing/#createview
