from django.db.models.functions import Abs, Round
from django.db.models import F, Value, DecimalField, Q
from django.http import HttpResponseRedirect
from .forms import AddRest
from .models import Rest
from django.contrib.auth import get_user_model
User = get_user_model()

def reached_max(user, rest_limit):
    rest_count = Rest.objects.filter(user=user).count()
    if rest_count >= rest_limit:
        return True
    return False


def user_has_rests(user):
    rests = Rest.objects.filter(user=user)
    if rests:
        return True
    return False


def get_categories(rests):
    if rests:
        categories = rests.values('category')
        category_list = sorted(set([row["category"]
                                for row in categories]), key=str.casefold)
        return category_list
    return []

def rest_post(request, initial_obj=None):
    if initial_obj:
        form = AddRest(request.POST, instance=initial_obj)
    else:
        form = AddRest(request.POST)
    if request.POST.get('category_dropdown'):
        category = request.POST.get('category_dropdown', None)
    else:
        category = request.POST.get('category_text', None)

    if id:
        if not request.POST.get('latitude'):
            lat = initial_obj.latitude
            long = initial_obj.longitude
            address = initial_obj.address
            rating = initial_obj.rating
            rest = initial_obj.rest

        else:
            lat = request.POST.get('latitude', None)
            long = request.POST.get('longitude', None)
            address = request.POST.get('address', None)
            rating = request.POST.get('rating', None)
            if rating == 'undefined':
                rating = None
            rest = request.POST.get('rest', None)

    my_rating = None
    if request.POST.get('tried_radio') == 'true':
        my_rating = request.POST.get('my_rating')

    if form.is_valid():
        new_obj = form.save(commit=False)
        new_obj.latitude = lat
        new_obj.notes = request.POST.get('notes')
        new_obj.longitude = long
        new_obj.address = address
        new_obj.rating = rating
        new_obj.rest = rest
        new_obj.category = category
        new_obj.my_rating = my_rating
        new_obj.user = str(request.user)
        new_obj.save()

def get_start_lat(request):
    startLat = request.GET.get("startLat")
    if startLat:
        return float(startLat)
    return None


def get_start_long(request):
    startLong = request.GET.get("startLong")
    if startLong:
        return float(startLong)
    return None


def set_miles_bool(request):
    if request.POST.get("measurement") == "true":
        miles_bool = True
    else:
        miles_bool = False
    User.objects.filter(username=request.user).update(miles=miles_bool)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_order_list_str(request):
    order = request.GET.get('order')
    order_list = []
    acceptable_values = ["category", "rest", "rating", "my_rating", "distance"]
    negative_values = []
    for value in acceptable_values:
        negative_values.append("-"+value)
    acceptable_values.extend(negative_values)

    if order:
        for col in order.split(','):
            if col not in acceptable_values:
                raise Exception(f"Invalid value for order parameter:{col}")
            if col.startswith('-'):
                order_list.append(
                    f"F('{str(col.replace('-',''))}').desc(nulls_last=True)")
            else:
                order_list.append(f"F('{str(col)}').asc(nulls_first=True)")
    else:
        order_list.append("F('id').asc(nulls_last=True)")
    order_list = "[" + ",".join(order_list) + "]"
    return order_list


def filter_search(request, rests):
    if rests:
        search_query = request.GET.get("search")
        if search_query:
            rests = rests.filter(Q(rest__icontains=search_query) |
                                 Q(category__icontains=search_query) |
                                 Q(address__icontains=search_query))
    return rests


def filter_categories(request, rests):
    if rests:
        category_filter = request.GET.get("categories")

        # using this rather than get_categories() to save on queries
        categories = [category['category']
                      for category in list(rests.values('category'))]
        categories = sorted(set(categories))

        if category_filter:
            if category_filter == "none":
                return None
            else:
                category_filter = category_filter.split(",")
            rests = rests.filter(category__in=category_filter)
    return rests


def set_distance(request, rests):
    if rests:
        startLat = get_start_lat(request)
        startLong = get_start_long(request)
        if startLat and startLong:
            rests = rests.annotate(
                distance=Round(Abs(F('latitude') - Value(startLat, DecimalField())) + Abs(F('longitude') - Value(startLong, DecimalField())), precision=2, output_field=DecimalField(max_digits=5, decimal_places=2)))
        else:
            rests = rests.annotate(
                distance=Value(None, output_field=DecimalField()))
    return rests

def get_page(request):
    page = request.GET.get("page")
    if not page:
        return 1
    else:
        return int(page)


def get_start_index(page, rows_per_page):
    if page > 1:
        start_index = ((page - 1) * rows_per_page)
        return start_index
    return 0