from .common import *

@login_required

def OrderCreateView (request):

    if request.method == 'POST':

        name = request.POST.get("name")
        address = request.POST.get("address")
        p_num = request.POST.get("p_number")
        e_mail = request.POST.get("e_mail")
        memo = request.POST.get("memo")

        user_id = request.user

        orderSql = "INSERT INTO order_info(user_id, order_name, " \
                   "order_address, order_p_num, order_email, order_memo) " \
                   "VALUES ((%s),(%s),(%s),(%s),(%s),(%s))"

        execute(orderSql, (user_id, name, address, p_num, e_mail, memo,))
        idSql = "SELECT id FROM order_info " \
                "where user_id = (%s) and order_name =(%s) and order_address = (%s) " \
                "and order_p_num = (%s) and order_email = (%s) and order_memo =(%s) " \
                "order by buy_date desc limit 1"
        id = execute_and_get(idSql, (user_id, name, address, p_num, e_mail, memo,))
        if len(id) != 0:
            store = request.POST.get("store")
            book = request.POST.get("book")
            price = request.POST.get("price")
            is_ajax = request.POST.get('is_ajax')
            list = request.POST.getlist('list[]')

            storeIdSql = "SELECT id FROM bookstore where store_name=(%s)"
            store_id = execute_and_get(storeIdSql, (store,))

            isbnSql = "SELECT book_isbn FROM book_inven " \
                      "where book_name = (%s) and store_id = (%s)"
            isbn = execute_and_get(isbnSql, (book, store_id,))

            listSql = "INSERT INTO order_info_list(order_info_id, store_id, isbn, price) " \
                      "VALUES ((%s),(%s),(%s),(%s))"
            execute(listSql, (id, store_id, isbn, price,))

            return redirect('customer:main')