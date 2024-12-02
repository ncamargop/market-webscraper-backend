from collections import defaultdict
from django.db import connection
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Index
from .serializers import ProductSerializer, IndexSerializer
from django.db.models import Max


@api_view(['GET'])
def product_list(request):
    search_term = request.GET.get('search', '')
    latest = request.GET.get('latest', 'false') == 'true'

    if latest:
        # Get the max created_at date
        max_date = Product.objects.aggregate(Max('uploaded_at'))['uploaded_at__max']

        # Get the products created on the latest date
        products = Product.objects.filter(
            product_name__icontains=search_term,
            uploaded_at=max_date
        )
    else:
        products = Product.objects.filter(product_name__icontains=search_term)

    return JsonResponse(list(products.values()), safe=False)




@api_view(['GET'])
def product_detail(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
    serializer = ProductSerializer(product)
    return Response(serializer.data)




@api_view(['GET'])
def product_summary(request, product_name):
    # Extract the first word of the product name
    first_word = product_name.split()[0] 
    
    # Query table for price data per store and date
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT store, DATE(uploaded_at) as date, AVG(average_price) as average_price
            FROM average_products
            WHERE product_name = %s
            GROUP BY store, date
            ORDER BY date, store
        """, [first_word])
        rows = cursor.fetchall()

    # Group data by date
    grouped_data = {}
    for row in rows:
        store = row[0]
        date = row[1]
        average_price = float(row[2])


        if date not in grouped_data:
            grouped_data[date] = {"date": date}


        grouped_data[date][store] = average_price


    formatted_data = list(grouped_data.values())
    # Return the formatted data as a JSON response
    return JsonResponse(formatted_data, safe=False)





@api_view(['GET'])
def index_prices_view(request):
    index_prices = Index.objects.all().order_by('date')
    serializer = IndexSerializer(index_prices, many=True)
    return Response(serializer.data)
