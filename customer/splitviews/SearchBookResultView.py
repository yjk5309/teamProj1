from .common import *

def SearchBookResultView(request):
    cursor = connection.cursor()

    title = request.GET.get('title')
    author = request.GET.get('author')
    publisher = request.GET.get('publisher')

    search_keyword = {'title': title,
                      'author': author,
                      'publisher': publisher,}

    search_datas = execute_and_get("SELECT book_name, author, publisher, book_img, price, isbn FROM book" +
                             " WHERE book_name LIKE '%" + title + "%' AND author LIKE '%" + author + "%' AND publisher LIKE '%" + publisher + "%' GROUP BY book_name")

    search_list = []
    for search_data in search_datas:
        store_id = execute_and_get("SELECT max(store_id) FROM book_inven WHERE book_isbn = (%s)", (search_data[5],))
        row = {'book_name': search_data[0],
               'author': search_data[1],
               'publisher': search_data[2],
               'book_img': search_data[3],
               'price': search_data[4],
               'book_isbn': search_data[5],
               'store_id': store_id[0][0],
            }
        search_list.append(row)

    connection.commit()
    connection.close()

    result = 1  # 검색결과가 있을 때와 없을 때 구분
    if len(search_list) == 0:
        result = 0

    # 검색키워드가 아무것도 입력되지 않았을 때
    if title == "" and author == "" and publisher == "":
        messages.error(request, '검색 키워드를 하나 이상 입력해주세요.')
        return redirect('customer:search_book')

    return render(request, 'search_book_result.html', {'search_list': search_list, 'search_keyword': search_keyword,
                                                       'result': result})
