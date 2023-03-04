get_summ_all = '''
create or replace function get_summ_all(answer int)
    returns INTEGER
    language plpgsql
as
$$

begin

    return (select sum(t.sum)::integer summ
            from (select oo.id, sum(pp.price)
                  from orders_order oo
                           join orders_order_items ooi on oo.id = ooi.order_id
                           join products_product pp on pp.id = ooi.product_id
                  group by oo.id, oo.paid, oo.shop_id
                  having oo.paid = true
                     and oo.shop_id = answer) t);
end;
$$;
'''

get_avarage_price = '''
CREATE OR REPLACE FUNCTION get_avarage_price(answer int)
    RETURNS INTEGER AS
$$
BEGIN
    RETURN (select cast(sum(summ) / 30 as int) summ
            from (select sum(pp.price) summ
                  from orders_order oo
                           join orders_order_items ooi on oo.id = ooi.order_id
                           join products_product pp on pp.id = ooi.product_id
                  group by oo.created_at, oo.shop_id, oo.paid
                  having oo.created_at > now() - interval '1 month'
                     and oo.shop_id = answer
                     and oo.paid = True) tb1);
END;
$$ LANGUAGE plpgsql;
'''
get_stat_sales = '''
CREATE OR REPLACE FUNCTION get_stat_sales(answer int)
    RETURNS table
            (
                sum      bigint,
                datetime timestamp
            )
as
$$
BEGIN
    RETURN query (select sum(pp.price::integer),
                         make_timestamp(extract(year from oo.created_at)::integer,
                                        extract(month from oo.created_at)::integer, 1, 0, 0,
                                        0) datetime

                  from orders_order oo
                           join orders_productorder ooi on oo.id = ooi.order_id
                           join products_product pp on pp.id = ooi.product_id
                  group by datetime, oo.shop_id
                  having oo.shop_id = answer);
END;
$$ LANGUAGE plpgsql;
'''
