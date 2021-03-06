from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.paginator import Paginator
from users.urls import mypage
from .models import Store, Cake, Order, Review
from .forms import StoreForm, CakeForm, OrderForm

def home(request):
    #order_by -pub_date(최신순) pub_date(오래된순)
    stores = Store.objects.order_by('-pub_date')
    reviews = Review.objects.order_by('-pub_date')[:4]
    paginator = Paginator(stores, 4) 
    page = request.GET.get('page', 1)
    stores = paginator.get_page(page)
    return render(request, 'home.html', {'stores': stores, 'reviews':reviews})

# 가게 등록 C (필요 없을 예정)
def store_new(request):
    if request.method == 'POST':
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            store.author = request.user
            store.published_date = timezone.now()
            store.save()
            return redirect('home')
    else:
        form = StoreForm()
    return render(request, 'store_new.html', {'form': form})

# 가게 디테일 R
def store_detail(request, pk):
    store = get_object_or_404(Store, pk=pk)
    cake_list = Cake.objects.filter(referred_store=store)
    review_list = Review.objects.filter(referred_store=store)
    num = 0
    # 최신순, 별점 낮은순, 높은순의 option을 post로 받아서 해당에 따라 정렬한다.
    if request.method == "POST":
        sort = request.POST.get('sort')
        num = 2
        if sort == 'highrate':
            review_list = Review.objects.filter(referred_store=store).order_by('-rate','-pub_date')
        elif sort == 'lowerate':
            review_list = Review.objects.filter(referred_store=store).order_by('rate','-pub_date')
        else :
            review_list = Review.objects.filter(referred_store=store).order_by('-pub_date')
    return render(request, 'store_detail.html', {'store': store, 'cakelist':cake_list, 'reviewlist':review_list, 'num':num})

# 가게 수정 U
def store_edit(request, pk):
    store = get_object_or_404(Store, pk=pk)
    if request.method == "POST":
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            store = form.save(commit=False)
            store.author = request.user
            # store.pub_date = timezone.now() # 게시일자(pub_date) 대신, 새로운 필드로 수정 일자를 넣는 것을 고려 
            store.save()
            return redirect('detail', pk= pk)
    else:
        form = StoreForm(instance=store)

    return render(request, 'store_edit.html', {'form': form})

# 가게 삭제 D (필요 없을 예정, 생성과 삭제는 관리자 측)
def store_delete(request, pk):
    store = get_object_or_404(Store, pk=pk)
    store.delete()
    return redirect('home')

# 케이크 등록 C (사장님측 UX, 관리자측이 사용할 수도..)
def cake_new(request, pk): #가게 pk값
    store = get_object_or_404(Store, pk=pk)
    if request.method == 'POST':
        form = CakeForm(request.POST, request.FILES)
        if form.is_valid():
            cake = form.save(commit=False)
            cake.author = request.user # author 저장이 필요한지?
            cake.pub_date = timezone.now()
            cake.referred_store = store
            cake.save()
            return redirect('detail', pk=pk)
    else:
        form = CakeForm()

    return render(request, 'cake_new.html', {'form': form})

# 케이크 상세 R
def cake_detail(request, pk): #cake의 pk값
    cake = Cake.objects.get(pk=pk)
    return render(request, 'cake_detail.html',{'cake':cake})

# 케이크 수정 U
def cake_edit(request, pk): #cake의 pk값
    cake = get_object_or_404(Cake, pk=pk)
    if request.method == "POST":
        form = CakeForm(request.POST, request.FILES, instance=cake)
        if form.is_valid():
            cake = form.save(commit=False)
            cake.author = request.user # author 저장이 필요한지?
            # store.pub_date = timezone.now() # 게시일자(pub_date) 대신, 새로운 필드로 수정 일자를 넣는 것을 고려 
            cake.save()
            # 현재 케이크 역참조를 위해 모델에 related_name 추가 (reverse lookup of foreign keys)
            # The related_name is what we use for the reverse lookup. In general, it is a good practice to provide a related_name for all the foreign keys rather than using Django’s default-related name.
            store_pk = cake.referred_store.pk
            return redirect('store_detail', pk= store_pk) # 케이크 관리페이지, 혹은 일단 가게페이지로 가도록 구현
    else:
        form = StoreForm(instance=cake)

    return render(request, 'cake_edit.html', {'form': form})

# 케이크 삭제 D
def cake_delete(request, pk): #cake의 pk값
    cake = get_object_or_404(Cake, pk=pk)
    store_pk = cake.referred_store.pk
    cake.delete()
    return redirect('store_detail', pk= store_pk) # 케이크 관리페이지, 혹은 일단 가게페이지로 가도록 구현

# 주문 C (RUD 구현 필요!)
def order_new(request, pk): #cake의 pk값
    cake = get_object_or_404(Cake, pk=pk)
    # 가게별 요청 - 선택사항 콤마로 분리
    맛 = cake.맛.replace(" ","").split(',')
    모양 = cake.모양.replace(" ","").split(',')
    사이즈 = cake.사이즈.replace(" ","").split(',')
    크림종류 = cake.크림종류.replace(" ","").split(',')
    레터링색 = cake.레터링색.replace(" ","").split(',')
    if request.method == 'POST':
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            # get 방식으로 가져와 저장
            order.맛 = request.POST.get('맛')
            order.모양 = request.POST.get('모양')
            order.사이즈 = request.POST.get('사이즈')
            order.크림종류 = request.POST.get('크림종류')
            order.레터링색 = request.POST.get('레터링색')
            order.pub_date = timezone.now()
            order.referred_cake = cake
            order.referred_store = cake.referred_store
            order.save()
            # 주문 결과 페이지로 가도록 수정하기!
            return redirect('store_detail', pk=cake.referred_store_id)
    else:
        form = OrderForm()
    return render(request, 'order_submit.html', {'form': form, 'cake':cake, '맛':맛, '모양':모양, '사이즈':사이즈, '크림종류':크림종류, '레터링색':레터링색})

# 리뷰 페이지 C (R- 더보기 U - 수정 D- 삭제 구현 필요)
def review_page(request, pk, orderpk):
    cake = get_object_or_404(Cake, pk=pk)
    store = get_object_or_404(Store, pk=cake.referred_store_id)
    order =  get_object_or_404(Order, pk=orderpk)
    return render(request, 'review_page.html', {'cake' : cake, 'store' : store, 'order':order })

# 리뷰 별점처리
# 항목을 get으로 가져와서 Review 양식에 저장
def review_rating(request):
    if request.method == 'GET':
        order_id = request.GET.get('order')
        store_id = request.GET.get('referred_store')
        cake_id =  request.GET.get('referred_cake')
        referred_store = Store.objects.get(id = store_id)
        referred_cake = Cake.objects.get(id = cake_id)
        comment = request.GET.get('comment')
        rate = request.GET.get('rate')
        order = Order.objects.get(pk=order_id)
        Review(user=request.user, order= order, referred_store=referred_store, referred_cake=referred_cake, comment=comment, rate=rate).save()
        # 모델상의 일부 필드 변경 (임시방법, onetoOnefield - 기능찾기)
        Ord = Order.objects.get(id = order_id)
        Ord.reviewing = 2
        Ord.save()
        return redirect('mypage', pk=order.user_id)

# 리뷰 삭제 D
def review_delete(request, pk):
    order = get_object_or_404(Order,pk = pk)
    review = Review.objects.filter(order_id=pk)
    order.reviewing = 1
    order.save()
    review.delete()
    return redirect('mypage',pk=order.user_id)

# 리뷰 수정 페이지 - U
def review_edit(request, pk):
    order = get_object_or_404(Order,pk = pk)
    review = Review.objects.filter(order_id=pk)
    return render(request, 'review_edit.html', {'review' : review, 'order':order})

# 리뷰 수정 제출 - U
def review_update(request):
    review_id = request.GET.get('review')
    review = get_object_or_404(Review,pk = review_id)
    order = get_object_or_404(Order,pk = review.order_id)
    if request.method == 'GET':
        review.comment = request.GET.get('comment')
        review.rate = request.GET.get('rate')
        review.save()
        return redirect('mypage',pk=order.user_id)


# 찜 기능 구현 필요 (유저 경험: 아마.. 케이크, 케잌집 상세페이지에서 찜하기 -> 케이크, 케잌집 모델에 필드 추가 필요)
