from django.db import transaction
from django.db.transaction import atomic
from django.shortcuts import render

# @transaction.non_atomic_requests
# @transaction.atomic
# def my_view(request):
#     if formset.is_valid():
#         with atomic():
#             pass
