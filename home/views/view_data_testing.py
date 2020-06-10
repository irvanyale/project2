from django.shortcuts import render, redirect, get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import ListView, DetailView
from pyexcel_xls import get_data as xls_get
from pyexcel_xlsx import get_data as xlsx_get

from home.forms import DataTestingForm
from home.models import DataTesting
from home.views import testing


def dashboard(request):
    return render(request, 'home.html', {})


class IndexView(ListView):
    template_name = 'home_data_testing.html'
    context_object_name = 'data_list'

    def get_queryset(self):
        return DataTesting.objects.all()


class DataDetailView(DetailView):
    model = DataTesting
    template_name = 'home_data_testing_detail.html'


def detail(request, pk, template_name='home_data_testing_detail.html'):
    data = get_object_or_404(DataTesting, pk=pk)
    return render(request, template_name, data)


def create(request):
    form = DataTestingForm()

    if request.method == 'POST':
        if request.POST.get("input_excel"):
            try:
                excel_file = request.FILES['file-excel']
            except MultiValueDictKeyError:
                return render(request, 'home_data_testing_create.html', {'form': form})

            if str(excel_file).split('.')[-1] == 'xls':
                data = xls_get(excel_file, column_limit=5)
            elif str(excel_file).split('.')[-1] == 'xlsx':
                data = xlsx_get(excel_file, column_limit=5)
            else:
                return render(request, 'home_data_testing_create.html', {'form': form})

            if data is not None:
                save_excel_to_db(data)
                return redirect('home:data-testing')
        else:
            form = DataTestingForm(request.POST)
            if form.is_valid():
                form.save()

                # Testing
                testing.proses_training()

                return redirect('home:data-testing')

    return render(request, 'home_data_testing_create.html', {'form': form})


def edit(request, pk, template_name='edit.html'):
    data = get_object_or_404(DataTesting, pk=pk)
    form = DataTestingForm(request.POST or None, instance=data)
    if form.is_valid():
        form.save()

        # Testing
        testing.proses_training()

        return redirect('home:data-testing')
    return render(request, template_name, {'form': form})


def delete(request, pk, template_name='confirm_delete.html'):
    contact = get_object_or_404(DataTesting, pk=pk)
    if request.method == 'POST':
        contact.delete()
        return redirect('home:data-testing')
    return render(request, template_name, {'object': contact})


def save_excel_to_db(data_excel):
    for d_sheet in data_excel:
        sheet = data_excel[d_sheet]
        if len(sheet) > 1:  # data sheet
            for data in sheet:
                if len(data) > 0:  # check row tidak kosong
                    if str(data[0]).lower() != 'no':  # check bukan header
                        
                        # Check jika ada data yg kosong
                        if len(data) < 5:
                            i = len(data)
                            while i < 5:
                                data.append('')
                                i += 1

                        # Simpan data
                        no = data[0]
                        db = DataTesting.objects.filter(no=str(no))

                        if len(db) == 0:
                            DataTesting.objects.create(
                                no=data[0],
                                persen_ch4=data[1],
                                persen_c2h4=data[2],
                                persen_c2h2=data[3],
                                fault=data[4]
                            )
                        else:
                            dt = db[0]
                            dt.no = data[0]
                            dt.persen_ch4 = data[1]
                            dt.persen_c2h4 = data[2]
                            dt.persen_c2h2 = data[3]
                            dt.fault = data[4]
                            dt.save()