from decimal import Decimal
from django.db.models import Sum, Case, When, DecimalField, Value


def customer_totals(customer):
    agg = customer.entries.aggregate(
        given=Sum(Case(
            When(type='given', then='amount'),
            default=Value(0), output_field=DecimalField(max_digits=12, decimal_places=2)
        )),
        received=Sum(Case(
            When(type='received', then='amount'),
            default=Value(0), output_field=DecimalField(max_digits=12, decimal_places=2)
        )),
    )
    given = agg['given'] or Decimal('0')
    received = agg['received'] or Decimal('0')
    return {
        'given': given,
        'received': received,
        'balance': given - received,
    }


def business_totals(business):
    given = Decimal('0')
    received = Decimal('0')
    due = Decimal('0')
    advance = Decimal('0')
    for customer in business.customers.all():
        tt = customer_totals(customer)
        given += tt['given']
        received += tt['received']
        if tt['balance'] > 0:
            due += tt['balance']
        elif tt['balance'] < 0:
            advance += -tt['balance']
    return {'given': given, 'received': received, 'due': due, 'advance': advance}


def outstanding_summary(business):
    rows = []
    for customer in business.customers.all():
        tt = customer_totals(customer)
        rows.append({
            'customer_id': customer.id,
            'customer_name': customer.name,
            'balance': tt['balance'],
        })
    rows.sort(key=lambda r: r['balance'], reverse=True)
    return rows
