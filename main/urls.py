from django.urls import path
from main.views import MainView, IncomesView, ExpensesView, WalletDeleteView, IncomeExpenseDeleteView, \
                        CategoryDeleteView, CashFlowAddView

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('wallet/<int:pk>/delete', WalletDeleteView.as_view(), name='wallet_delete'),

    path('cash_flow/add/', CashFlowAddView.as_view(), name='cashflow_add'),  # add chash flow from incomes or expenses pages

    path('incomes/', IncomesView.as_view(), name='incomes'), # category add

    path('category/<int:pk>/delete', CategoryDeleteView.as_view(), name='category_delete'),  # deletion category income or expense pages

    path('expenses/', ExpensesView.as_view(), name='expenses'), # category add

    path('cash_flow/<int:pk>/delete', IncomeExpenseDeleteView.as_view(), name='income_delete'),   # deletion cash flow income or expense pages
]
