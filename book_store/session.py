from .models import Book

class Session:
    def is_book_in_cart(request):
        carts = request.session.get("cart", None)
        if carts == None:
            return False
        else:
            return True
        
    def add(request, pk):
        flag_for_Loop = True
        quantity = 1
        if 'cart' in request.session:
            if len(request.session['cart']) > 0:
                for item in request.session['cart']:
                    if item[0] == pk: 
                        request.session['cart'][request.session['cart'].index(item)][1] += quantity
                        flag_for_Loop = False
                        break
                if flag_for_Loop:
                    request.session['cart'].append([pk, quantity])
            else:
                request.session['cart'].append([pk, quantity])
        else:
            request.session['cart'] = [[pk, quantity]]
        request.session.modified = True

    def plus(request, pk):
        if 'cart' in request.session:
            for item in request.session['cart']:
                if item[0] == pk:
                    request.session['cart'][request.session['cart'].index(item)][1] += 1  
        request.session.modified = True
        
    def mines(request, pk):
        if 'cart' in request.session:
            for item in request.session['cart']:
                if item[0] == pk:
                    if request.session['cart'][request.session['cart'].index(item)][1] > 1:
                        request.session['cart'][request.session['cart'].index(item)][1] -= 1
                    else:
                        del request.session['cart'][request.session['cart'].index(item)]
        request.session.modified = True
        if len(request.session['cart']) == 0:
            Session.clear_session(request)
    
    def delete(request, pk):
        if 'cart' in request.session:
            for item in request.session['cart']:
                if item[0] == pk:
                    del request.session['cart'][request.session['cart'].index(item)]
        request.session.modified = True
        if len(request.session['cart']) == 0:
            Session.clear_session(request)
        
    def get_book_from_session(request):
        carts = request.session.get("cart", None)
        IDs = []
        if not carts == None:
            for cart in carts:
                IDs.append(cart[0])
        books = Book.objects.filter(id__in=IDs)
        session_books = []
        for book in books:
            for cart in carts:
                if book.id == cart[0]:
                    session_books.append(
                        {
                            "id": book.id,
                            "cover": book.cover,
                            "title": book.title,
                            "author": book.author,
                            "description": book.description,
                            "price": book.price,
                            "discount": book.discount,
                            "count": cart[1],
                        }
                    )
        return session_books
    
    def calculate_cart_price(books):
        total_price = 0
        for book in books:
            if book['discount']:
                total_price += (book['price'] - book['discount'].price) * book['count']
            else:
                total_price += book['price'] * book['count']
        return total_price 
    
    def clear_session(request):
        del request.session['cart']
        request.session.modified = True
