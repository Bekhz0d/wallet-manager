from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import Category, Wallet, IncomeExpense
from django.contrib import messages
from datetime import datetime, date, timedelta
from django.db.models import Sum


class MainView(LoginRequiredMixin, View):
    def get(self, request):
        wallets = Wallet.objects.filter(user=request.user)
        categories = Category.objects.all()
        cash_flows = IncomeExpense.objects.filter(user=request.user).order_by('-date_time')
        total_income = cash_flows.filter(is_income=True).aggregate(sum=Sum('summa'))['sum']
        total_expense = cash_flows.filter(is_income=False).aggregate(sum=Sum('summa'))['sum']
        if not total_income:
            total_income = 0
        if not total_expense:
            total_expense = 0
        context = {'cash_flows': cash_flows, 
                   'wallets': wallets, 
                   'categories': categories,
                   'total_income': total_income,
                   'total_expense': total_expense}
        return render(request, 'index.html', context)
    
    def post(self, request):
        booleans = request.POST.get('by_wallet') or request.POST.get('quick_f') or request.POST.get('from') or request.POST.get('to') or request.POST.get('by_category') or request.POST.get('income_or_expense')
        if booleans:
            wallets = Wallet.objects.filter(user=request.user)
            categories = Category.objects.all()
            cash_flows = IncomeExpense.objects.filter(user=request.user).order_by('-date_time')
            today = date.today()
            if request.POST.get('by_wallet'):
                wallets = wallets.filter(id=int(request.POST.get('by_wallet')))
                cash_flows = cash_flows.filter(wallet=int(request.POST.get('by_wallet')))
                request.GET['by_wallet'] = wallets
            if request.POST.get('quick_f'):
                if request.POST.get('quick_f') == 'daily':
                    cash_flows = cash_flows.filter(date_time__day=today.strftime("%d"))
                elif request.POST.get('quick_f') == 'weekly':
                    start_date = today - timedelta(days=7)
                    cash_flows = cash_flows.filter(date_time__range=(start_date, today))
                elif request.POST.get('quick_f') == 'monthly':
                    start_date = today - timedelta(days=30)
                    cash_flows = cash_flows.filter(date_time__range=(start_date, today))
            if request.POST.get('from'):
                from_ = datetime.strptime(request.POST.get('from'), '%Y-%m-%d')
                cash_flows = cash_flows.filter(date_time__gte=from_)
            if request.POST.get('to'):
                to = datetime.strptime(request.POST.get('to'), '%Y-%m-%d')
                cash_flows = cash_flows.filter(date_time__lte=to)
            if request.POST.get('by_category'):
                cash_flows = cash_flows.filter(category=int(request.POST.get('by_category')))
            if request.POST.get('income_or_expense'):
                print()
                print()
                print(request.POST.get('income_or_expense'))
                print()
                print()
                if request.POST.get('income_or_expense') == 'expenses':
                    cash_flows = cash_flows.filter(is_income=False)
                else:
                    cash_flows = cash_flows.filter(is_income=True)
            total_income = cash_flows.filter(is_income=True).aggregate(sum=Sum('summa'))['sum']
            if not total_income: total_income = 0
            total_expense = cash_flows.filter(is_income=False).aggregate(sum=Sum('summa'))['sum']
            if not total_expense: total_expense = 0
            context = {'cash_flows': cash_flows, 'wallets': wallets, 'categories': categories, 'total_income': total_income, 'total_expense': total_expense}
            return render(request, 'index.html', context)        

        name_uz = request.POST.get('wallet_name_uz')
        name_en = request.POST.get('wallet_name_en')
        name_ru = request.POST.get('wallet_name_ru')
        wallet_id = request.POST.get('wallet_id')

        if wallet_id:
            wallet = Wallet.objects.get(id=int(wallet_id))
            wallet.name_uz = name_uz
            wallet.name_en = name_en
            wallet.name_ru = name_ru
            wallet.user = request.user
            wallet.save()
            return redirect('main')
        if name_uz or wallet_id:
            Wallet.objects.create(name_uz=name_uz, name_ru=name_ru, name_en=name_en, user=request.user)
        return redirect('main')
    
    
class WalletDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        wallet = get_object_or_404(Wallet, pk=pk)
        wallet.delete()
        return redirect(reverse('main'))
    

class IncomesView(LoginRequiredMixin, View):
    def get(self, request):
        wallets = Wallet.objects.filter(user=request.user)
        categories = Category.objects.filter(user=request.user).filter(is_income=True).order_by('name')
        cash_flows = IncomeExpense.objects.filter(user=request.user).filter(is_income=True).order_by('-date_time')
        total_income = cash_flows.aggregate(sum=Sum('summa'))['sum']
        total_expense = cash_flows.aggregate(sum=Sum('summa'))['sum']
        context = {'cash_flows': cash_flows, 
                   'categories': categories, 
                   'wallets': wallets,
                   'total_income': total_income,
                   'total_expense': total_expense}
        return render(request, 'incomes.html', context)
    
    # add category
    def post(self, request):
        category_name_uz = request.POST.get('category_name_uz')
        category_name_ru = request.POST.get('category_name_ru')
        category_name_en = request.POST.get('category_name_en')
        category_id = request.POST.get('category_id')
        if category_id:
            category_obj = Category.objects.get(id=int(category_id))
            category_obj.name = category_name_uz
            category_obj.name_ru = category_name_ru
            category_obj.name_en = category_name_en
            category_obj.user = request.user
            category_obj.is_income = True
            category_obj.save()
            return redirect('incomes')
        Category.objects.create(name_uz=category_name_uz, name_en=category_name_en, name_ru=category_name_ru, user=request.user, is_income=True)
        return redirect('incomes')
    

class ExpensesView(LoginRequiredMixin, View):
    def get(self, request):
        wallets = Wallet.objects.filter(user=request.user)
        categories = Category.objects.filter(user=request.user).filter(is_income=False).order_by('name')
        cash_flows = IncomeExpense.objects.filter(user=request.user).filter(is_income=False).order_by('-date_time')
        total_income = cash_flows.aggregate(sum=Sum('summa'))['sum']
        total_expense = cash_flows.aggregate(sum=Sum('summa'))['sum']
        context = {'cash_flows': cash_flows, 
                   'categories': categories, 
                   'wallets': wallets,
                   'total_income': total_income,
                   'total_expense': total_expense}
        return render(request, 'expenses.html', context)
    
    # edit category
    def post(self, request):
        category_name_uz = request.POST.get('category_name_uz')
        category_name_ru = request.POST.get('category_name_ru')
        category_name_en = request.POST.get('category_name_en')
        category_id = request.POST.get('category_id')
        if category_id:
            category_obj = Category.objects.get(id=int(category_id))
            category_obj.name_uz = category_name_uz
            category_obj.name_ru = category_name_ru
            category_obj.name_en = category_name_en
            category_obj.user = request.user
            category_obj.save()
            return redirect('expenses')
        Category.objects.create(name_uz=category_name_uz, name_ru=category_name_ru, name_en=category_name_en, user=request.user)
        return redirect('expenses')


class CashFlowAddView(LoginRequiredMixin, View):
    def post(self, request):
        wallet = request.POST.get('wallet')
        category = request.POST.get('category')
        cash_flow_sum = request.POST.get('cash_flow_sum')
        cash_flow_date = request.POST.get('cash_flow_date')
        # redirect_url_add_cash_flow = request.POST.get('redirect_url_add_cash_flow', '/').split('/')
        # print()
        # print()
        # print(redirect_url_add_cash_flow)
        # print()
        # print()
        if cash_flow_date:
            cash_flow_date = datetime.strptime(request.POST.get('cash_flow_date'), '%Y-%m-%d')
            # print()
            # print()
            # print(cash_flow_date)
            # print()
            # print()
        else:
            cash_flow_date = datetime.now()
        category_obj = Category.objects.get(id=int(category))
        wallet_obj = Wallet.objects.get(id=int(wallet))

        # check, what is balance is enough to expense. and cash flow is income or expense.
        if category_obj.is_income: 
            wallet_obj.balance += int(cash_flow_sum)
            wallet_obj.save()
            IncomeExpense.objects.create(user=request.user, 
                                        wallet=wallet_obj,
                                        category=category_obj,
                                        summa=int(cash_flow_sum),
                                        date_time=cash_flow_date,
                                        is_income=True)
            return redirect('main')
            
        if wallet_obj.balance < int(cash_flow_sum):
            messages.warning(request, "Hisobingizda mablag' yetarli emas...")
            return redirect('main')
        wallet_obj.balance -= int(cash_flow_sum)
        wallet_obj.save()
        IncomeExpense.objects.create(user=request.user, 
                                     wallet=wallet_obj, 
                                     category=category_obj, 
                                     summa=int(cash_flow_sum),
                                     date_time=cash_flow_date,
                                     )
        return redirect('main')
        # return redirect(redirect_url_add_cash_flow)
        

class IncomeExpenseDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        cash_flow = get_object_or_404(IncomeExpense, pk=pk)
        cash_flow.delete()
        return redirect(reverse('main'))
    

class CategoryDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect(reverse('main'))
