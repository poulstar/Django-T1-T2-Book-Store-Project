import logging
from django.urls import reverse
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException
from django.http import Http404
from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from book_store.models import Order

@login_required
def go_to_gateway_view(request, price, order):
    amount = int(float(price))
    order = get_object_or_404(Order, pk=order)
    factory = bankfactories.BankFactory()
    try:
        bank = factory.auto_create()
        bank.set_request(request)
        bank.set_amount(amount)
        bank.set_user(request.user)
        bank.set_order(order)
        bank.set_client_callback_url(reverse('callback'))
        bank.ready()
        return bank.redirect_gateway()
    except AZBankGatewaysException as e:
        logging.critical(e)
        raise e

def callback_gateway_view(request):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    print(tracking_code)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404
    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404
    if bank_record.is_success:
        messages.success(request,'پرداخت با موفقیت انجام شد')
        order = bank_record.order
        order.is_paid = True
        order.save()
        return redirect('dashboard_transaction')

    messages.error(request,'پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما باز خواهد گشت')
    return redirect('dashboard_transaction')
