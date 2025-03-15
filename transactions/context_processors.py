from transactions.models import Transaction


def pending_withdrawals(request):
    if request.user.is_authenticated and request.user.is_staff:
        withdrawals = Transaction.objects.filter(transaction_type='WITHDRAWAL', status='PENDING')
    else:
        withdrawals = []
    return {'withdrawals': withdrawals}
