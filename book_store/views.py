from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Discount, Comment, Weblog, Favorite, OrderItem, Order
from .forms import CommentForm, SubscriberForm, WeblogForm, ProfileForm, OrderForm
from django.contrib import messages
import math
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from .session import Session
from azbankgateways.models import Bank

def book_home(request):
    cart_state = Session.is_book_in_cart(request)
    discounts = Discount.objects.all().order_by('-price')
    counter = 0
    header_books = []
    for discount in discounts:
        for book in discount.discount_books.all():
            if counter > 5:
                break
            counter += 1
            header_books.append(book)
    top_ten_books = Book.objects.all().order_by('-star')[:10]
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'عضویت شما در خبرنامه با موفقیت انجام شد')
        else:
            messages.error(request, 'فرم عضویت را پر کنید')
    new_top_books = Book.objects.all().order_by('-id')[0:6]            
    new_bottom_books = Book.objects.all().order_by('-id')[6:12]
    new_comments = Comment.objects.filter(is_active=True).order_by('-id')[:6]
    new_weblogs = Weblog.objects.all().order_by('-id')[:6]
    context = {
        'cart_state' : cart_state,
        'header_books' : header_books,
        'top_ten_books' : top_ten_books,
        'new_top_books' : new_top_books,
        'new_bottom_books' : new_bottom_books,
        'new_comments' : new_comments,
        'new_weblogs' : new_weblogs,
    }    
    return render(request, 'public/book_home.html', context)

def book_search(request):
    cart_state = Session.is_book_in_cart(request)
    discounts = Discount.objects.all()
    counter = 0
    header_books = []
    for discount in discounts:
        for book in discount.discount_books.all():
            if counter > 5:
                break
            header_books.append(book)
    word = request.GET.get('word')
    if word != None and len(word) > 0:
        books = Book.objects.filter(title__icontains=word).order_by('-id')
        paginator = Paginator(books, 6)
        page_number = request.GET.get('page')
        books = paginator.get_page(page_number)        
    else:  
        books = Book.objects.all().order_by('-id')
        paginator = Paginator(books, 6)
        page_number = request.GET.get('page')
        books = paginator.get_page(page_number)
    context = {
        'cart_state' : cart_state,
        'header_books' : header_books,
        'books' : books,
        'word' : word,
    }   
    return render(request, 'public/book_search.html', context)

def book_detail(request, pk):
    cart_state = Session.is_book_in_cart(request)
    discounts = Discount.objects.all()
    counter = 0
    header_books = []
    for discount in discounts:
        for book in discount.discount_books.all():
            if counter > 5:
                break
            header_books.append(book)
    book = get_object_or_404(Book, pk=pk)  
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  
            comment.user = request.user
            comment.book = book
            comment.is_active = False
            comment.save() 
            rate = 0
            for item in book.book_comments.all():
                rate += item.star
            rate = rate / len(book.book_comments.all())
            if (rate - math.floor(rate)) > 0.5:
                book.star = math.ceil(rate)
            else:    
                book.star = math.floor(rate)
            book.save()     
            messages.success(request, 'نظر شما ثبت شد')  
        else:     
            messages.error(request, 'نظر شما ثبت نشد، اطلاعات را پر کنید.')   
    context = {
        'cart_state' : cart_state,
        'header_books' : header_books,
        'book' : book,
    }   
    return render(request, 'public/book_detail.html', context)

def book_cart(request):
    books = Session.get_book_from_session(request)
    total_price = Session.calculate_cart_price(books)
    context = {
        'books' : books,        
        'total_price' : total_price,
    }
    return render(request, 'public/book_cart.html', context)

@login_required
def book_checkout(request):
    books = Session.get_book_from_session(request)
    total_price = Session.calculate_cart_price(books)
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.pay_price = total_price
            order.save()
            for book in books:
                book_object = get_object_or_404(Book, pk=book['id'])
                if book_object.discount:
                    pay_price = book_object.price - book_object.discount.price
                else:
                    pay_price = book_object.price    
                OrderItem.objects.create(
                    order = order,
                    book = book_object,
                    price = book_object.price,
                    pay_price = pay_price,
                    count = book['count'],
                    discount = book['discount'],
                )
            Session.clear_session(request)
            return redirect('try_to_pay', price=total_price, order=order)
    context = {
        'books' : books,        
        'total_price' : total_price,
        'form' : form,
    }
    return render(request, 'public/book_checkout.html',context)

def weblog_home(request):
    cart_state = Session.is_book_in_cart(request)
    discounts = Discount.objects.all()
    counter = 0
    header_books = []
    for discount in discounts:
        for book in discount.discount_books.all():
            if counter > 5:
                break
            header_books.append(book)
    weblogs = Weblog.objects.all().order_by('-id')
    paginator = Paginator(weblogs, 4)
    page_number = request.GET.get('page')
    weblogs = paginator.get_page(page_number)
    context = {
        'cart_state' : cart_state,
        'header_books' : header_books,
        'weblogs' : weblogs,
    }   
    return render(request, 'public/weblog_home.html', context)

def weblog_detail(request, pk):
    cart_state = Session.is_book_in_cart(request)
    discounts = Discount.objects.all()
    counter = 0
    header_books = []
    for discount in discounts:
        for book in discount.discount_books.all():
            if counter > 5:
                break
            header_books.append(book)
    weblog = get_object_or_404(Weblog, pk=pk)
    context = {
        'cart_state' : cart_state,
        'header_books' : header_books,
        'weblog' : weblog,
    }   
    return render(request, 'public/weblog_detail.html', context)

def change_favorite_state(request, pk):
    if request.user.is_authenticated:
        book = get_object_or_404(Book, pk=pk)
        item = Favorite.objects.filter(user=request.user).filter(book=book).first()
        if item == None:
            Favorite.objects.create(
                user = request.user,
                book = book
            )
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            item.delete()
            return redirect(request.META.get("HTTP_REFERER"))
    else:
        return redirect('login')

def dashboard_home(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).order_by('-id')
        books = []
        for favorite in favorites:
            books.append(favorite.book)
        my_favorite_genres = {}
        for book in books:
            for genre in book.genre.all():
                if my_favorite_genres.get(genre.label):
                    my_favorite_genres[genre.label] += 1
                else:
                    my_favorite_genres[genre.label] = 1
        my_favorite_genres = sorted(my_favorite_genres.items(), key=lambda x:x[1], reverse=True)
        my_favorite_genres = dict(my_favorite_genres[:5])
        comments = Comment.objects.filter(user=request.user).order_by('-id')[:5]
        weblogs = Weblog.objects.filter(author=request.user).order_by('-id')[:5]
        context = {
            'my_favorite_genres' : my_favorite_genres,
            'books' : books[:5],
            'comments' : comments,
            'weblogs' : weblogs,
        }
        return render(request, 'dashboard/dashboard_home.html', context)
    else:
        return redirect('login')

@login_required
def dashboard_blog(request):
    current_url = resolve(request.path_info).url_name
    weblogs = Weblog.objects.filter(author=request.user).order_by('-id')
    paginator = Paginator(weblogs, 5)
    page_number = request.GET.get('page')
    weblogs = paginator.get_page(page_number)
    context = {
        'current_url' : current_url,
        'weblogs' : weblogs,
    }
    return render(request, 'dashboard/dashboard_blog.html', context) 

@login_required
def dashboard_blog_add(request):
    current_url = resolve(request.path_info).url_name
    form = WeblogForm()
    if request.method == 'POST':
        form = WeblogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('dashboard_blog')
    context = {
        'current_url' : current_url,
        'form' : form,
    }
    return render(request, 'dashboard/dashboard_blog_add.html', context) 

@login_required
def dashboard_blog_update(request, pk):
    current_url = resolve(request.path_info).url_name
    weblog = get_object_or_404(Weblog, pk=pk)
    form = WeblogForm(instance=weblog)
    if request.method == 'POST':
        form = WeblogForm(request.POST, request.FILES, instance=weblog)
        if form.is_valid():
            form.save()
            return redirect('dashboard_blog')
    context = {
        'current_url' : current_url,
        'weblog' : weblog,
        'form' : form,
    }
    return render(request, 'dashboard/dashboard_blog_update.html', context) 

@login_required
def dashboard_blog_delete(request, pk):
    weblog = get_object_or_404(Weblog, pk=pk)
    if weblog.author == request.user:
        weblog.delete()
    return redirect('dashboard_blog')

@login_required
def dashboard_comment(request):
    comments = Comment.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(comments, 5)
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)
    context = {
        'comments' : comments,
    }
    return render(request, 'dashboard/dashboard_comment.html', context) 

@login_required
def dashboard_comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user == request.user:
        comment.delete()
    return redirect('dashboard_comment')
   
@login_required
def dashboard_favorite(request):
    favorites = Favorite.objects.filter(user=request.user).order_by('-id')
    books = []
    for favorite in favorites:
        books.append(favorite.book)
    paginator = Paginator(books, 5)
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    context = {
        'books' : books,
    }
    return render(request, 'dashboard/dashboard_favorite.html', context)  

@login_required
def dashboard_update_profile(request):
    form = ProfileForm(instance=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard_home')
    context = {
        'form' : form,
    }
    return render(request, 'dashboard/dashboard_update_profile.html', context)

@login_required
def dashboard_order(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(orders, 5)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)
    context = {
        'orders' : orders,
    }
    return render(request, 'dashboard/dashboard_order.html', context)

@login_required
def dashboard_order_item(request, pk):
    order = get_object_or_404(Order, pk=pk)
    previous_url = request.META.get('HTTP_REFERER')
    context = {
        'order' : order,
        'previous_url' : previous_url,
    }
    return render(request, 'dashboard/dashboard_order_item.html', context)

@login_required
def dashboard_transaction(request):
    transactions = Bank.objects.filter(user=request.user).order_by('-id')
    paginator = Paginator(transactions, 5)
    page_number = request.GET.get('page')
    transactions = paginator.get_page(page_number)
    context = {
        'transactions' : transactions,
    }
    return render(request, 'dashboard/dashboard_transaction.html', context)

def session(request, pk, task):
    match task:
        case 'add':
            Session.add(request, pk)
        case 'plus':
            Session.plus(request, pk)
        case 'mines':
            Session.mines(request, pk)
        case 'delete':
            Session.delete(request, pk)            
    return redirect(request.META.get("HTTP_REFERER"))

