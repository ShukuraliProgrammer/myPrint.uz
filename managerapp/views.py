
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import TemplateView, ListView


from .forms import OrderForm
from .models import OrderModel
from django.contrib.auth.decorators import login_required

# from django.forms import modelformset_factory
#
#
# OrderFormSet = modelformset_factory(
#         OrderModel, fields="__all__", extra=1, max_num=5
# )


@login_required(login_url='login')
def orderView(request):
    data = request.POST.copy()
    data['manager'] = request.user.id
    order_id_number = OrderModel.objects.all().last().id
    # order = OrderModel.objects.get(id=1)
    # OrderFormSet = formset_factory(OrderForm, extra=2, max_num=1)
    # OrderFormSet = modelformset_factory(OrderModel, extra=3,
    #                                     fields=('product', 'number', 'price', 'percent', 'status_order'))
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():

            form.save()

            return redirect('order_list')
        else:
            print(form.errors)

    else:
        form = OrderForm()

    context = {
        'form': form,
        'order_number': order_id_number + 1,
    }
    return render(request, 'order.html', context=context)


def logoutView(request):
    logout(request)
    return redirect('login')


class ResultView(TemplateView):
    template_name = 'invoice.html'


def loginView(request):
    if request.user.is_authenticated:
        return redirect('order')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)


            if user is not None:
                login(request, user)

                return redirect('order')
            else:
                messages.info(request, "Sizning Username yoki Parolingiz xato")
        context = {}
        return render(request, 'login.html', context=context)


@login_required(login_url='login')
def listView(request):
    if request.user.is_authenticated:
        if OrderModel.objects.filter(manager=request.user.id):
            orders = OrderModel.objects.filter(manager=request.user.id).order_by('-id').first()
            total = 0
            all_price = orders.price * orders.number
            percent_sum = (all_price / 100) * orders.percent
            sum_list = all_price + percent_sum
            total = total + sum_list
            context = {}

            if orders.price1 and orders.percent1:
                all_price1 = orders.price1 * orders.number1

                percent_sum1 = (all_price1 / 100) * orders.percent1
                sum_list1 = all_price1 + percent_sum1
                total = total + sum_list1
                context['all_price1'] = all_price1
                context['sum_list1'] = sum_list1

            if orders.price2 and orders.percent2:
                all_price2 = orders.price2 * orders.number2

                percent_sum2 = (all_price2 / 100) * orders.percent2
                sum_list2 = all_price2 + percent_sum2
                total = total + sum_list2
                context['all_price2'] = all_price2
                context['sum_list2'] = sum_list2

            if orders.price3 and orders.percent3:
                all_price3 = orders.price3 * orders.number3

                percent_sum3 = (all_price3 / 100) * orders.percent3
                sum_list3 = all_price3 + percent_sum3
                total = total + sum_list3
                context['all_price3'] = all_price3
                context['sum_list3'] = sum_list3

            if orders.price4 and orders.percent4:
                all_price4 = orders.price4 * orders.number4

                percent_sum4 = (all_price4 / 100) * orders.percent4

                sum_list4 = all_price4 + percent_sum4
                total = total + sum_list4
                context['all_price4'] = all_price4
                context['sum_list4'] = sum_list4

            context['orders'] = orders
            context['sum_list'] = sum_list
            context['all_price'] = all_price
            context['total'] = total
            if orders.percent:
                total = total + (total*orders.percent/100)
                context['total_sum']=total
        else:
            context = {}
        return render(request, 'invoice.html', context=context)


# def export_pdf(request):
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=Expenses' + \
#                                       str(datetime.datetime.now()) + '.pdf'
#     response['Content-Transfer-Encoding'] = 'binary'
#     orders = OrderModel.objects.filter(manager=request.user.id)
#     order_id_number = OrderModel.objects.all().last().id
#     percent_sum = []
#     for summa in orders:
#         percent_sum.append(summa.price * summa.percent / 100)
#     # total = orders.aggregate(money=Coalesce(Sum('price'), 0))['price'] * orders.number
#     all_price = []
#     for i in orders:
#         all_price.append(i.price * i.number)
#     sum_list = []
#     for (item1, item2) in zip(all_price, percent_sum):
#         sum_list.append(item1 + item2)
#     all_orders = zip(orders, all_price, percent_sum, sum_list)
#     html_string = render_to_string(
#         'expenses/pdf_output.html', {'expenses': all_orders, 'total': 0, 'order_number': order_id_number})
#
#     html = HTML(string=html_string)
#     result = html.write_pdf()
#
#     with tempfile.NamedTemporaryFile(delete=True) as output:
#         output.write(result)
#         output.flush()
#         output = open(output.name, 'rb')
#         response.write(output.read())
#     return response


# class OrderDetailView(UpdateView):
#     template_name = 'order_detail.html'
#     model = OrderModel
#     fields = ['customer', 'phone', 'created', 'limit', 'product', 'number', 'price', 'percent', 'status_order']
#     success_url = '/invoice'

# from wkhtmltopdf.views import PDFTemplateView

#
# class MyPDF(PDFTemplateView):
#     filename = 'my_pdf.pdf'
#     template_name = 'expenses/pdf_output.html'
#     cmd_options = {
#         'margin-top': 3,
#     }

def update_orderView(request):
    if request.user.is_authenticated:
        if OrderModel.objects.filter(manager=request.user.id):

            orders = OrderModel.objects.filter(manager=request.user.id).order_by('-id').first()

            form = OrderForm(instance=orders)
            if request.method == "POST":
                form = OrderForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('order_list')
            context = {'form': form,
                       'order_number': orders.id}
        else:
            context = {}
        return render(request, 'order_detail.html', context)


def order_list(request):
    if request.user.is_authenticated:
        if OrderModel.objects.filter(manager=request.user.id):

            orders = OrderModel.objects.filter(manager=request.user.id).order_by('-id').first()
            order_id_number = OrderModel.objects.all().last().id
            all_price = orders.price * orders.number
            percent_sum = (all_price / 100) * orders.percent
            sum_list = all_price + percent_sum
            context = {}
            not_percent = 0
            not_price = 0
            total_all = 0
            total_all = total_all + sum_list
            not_price = not_price + all_price
            not_percent = not_percent + percent_sum
            if orders.price1 and orders.percent1:
                all_price1 = orders.price1 * orders.number1
                percent_sum1 = (all_price1 / 100) * orders.percent1
                sum_list1 = all_price1 + percent_sum1
                context['all_price1'] = all_price1
                context['percent_sum1'] = percent_sum1
                context['sum_list1'] = sum_list1
                not_percent = not_percent + percent_sum1
                not_price = not_price + all_price1
                total_all = total_all + sum_list1
            if orders.price2 and orders.percent2:
                all_price2 = orders.price2 * orders.number2
                percent_sum2 = (all_price2 / 100) * orders.percent2
                sum_list2 = all_price2 + percent_sum2
                not_percent = not_percent + percent_sum2
                context['all_price2'] = all_price2
                context['percent_sum2'] = percent_sum2
                context['sum_list2'] = sum_list2
                not_percent = not_percent + percent_sum2
                not_price = not_price + all_price2
                total_all = total_all + sum_list2
            if orders.price3 and orders.percent3:
                all_price3 = orders.price3 * orders.number3
                percent_sum3 = (all_price3 / 100) * orders.percent3
                sum_list3 = all_price3 + percent_sum3
                not_percent = not_percent + percent_sum3
                context['all_price3'] = all_price3
                context['percent_sum3'] = percent_sum3
                context['sum_list3'] = sum_list3
                not_percent = not_percent + percent_sum3
                not_price = not_price + all_price3
                total_all = total_all + sum_list3
            if orders.price4 and orders.percent4:
                all_price4 = orders.price4 * orders.number4
                percent_sum4 = (all_price4 / 100) * orders.percent4
                sum_list4 = all_price4 + percent_sum4
                not_percent += percent_sum4
                not_price = not_price + all_price4
                total_all = total_all + sum_list4

                context['all_price4'] = all_price4
                context['percent_sum4'] = percent_sum4
                context['sum_list4'] = sum_list4

            context['orders'] = orders
            context['all_price'] = all_price
            context['percent_sum'] = percent_sum
            context['sum_list'] = sum_list
            context['order_number']=order_id_number
            context['not_percent'] = not_percent
            context['not_price'] = not_price
            context['total_all'] = total_all
        else:
            context={}
        return render(request, 'order_list.html', context=context)

