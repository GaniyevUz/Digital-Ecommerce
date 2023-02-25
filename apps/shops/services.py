from django.db.models import Count
from django.db.models.expressions import RawSQL

from orders.models import Order


def __get_order_cost(pk: int):
    orders = Order.objects.filter(items__order__shop_id=pk).annotate(total_items=Count('items'))
    total_orders = sum(orders.values_list('total_items', flat=True))

    paid_orders = orders.filter(paid=True).annotate(total_items=Count('items'))
    paid_orders_cost = sum(paid_orders.values_list('total_items', flat=True))

    return total_orders, paid_orders_cost


def main_stat_service(pk: int) -> dict:
    total_orders, paid_orders_cost = __get_order_cost(pk)

    _ = Order.objects.values('id').annotate(
        summ=RawSQL("SELECT get_summ_all(%s)", (1,)),
        avg=RawSQL("SELECT get_avarage_price(%s)", (1,))
    ).first()

    revenue, avg = _['summ'], _['avg']
    # total_customers = Client.objects.filter(shop_id=pk).count() # client chala
    data = {
        'id': pk,
        'total_orders': total_orders,
        'paid_orders': paid_orders_cost,
        'total_revenue': revenue,
        'total_customers': 'chala',
        'average_price': avg
    }
    return data
