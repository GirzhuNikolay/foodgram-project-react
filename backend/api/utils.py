import io

from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.response import Response


def post(request, pk, get_object, models, serializer):
    obj = get_object_or_404(get_object, id=pk)
    if models.objects.filter(
        recipe=obj, user=request.user
    ).exists():
        return Response(
            {'message':
                f'Рецепт уже добавлен {obj}.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    serializer = serializer(
        obj, context={request: 'request'}
    )
    models.objects.create(
        recipe=obj, user=request.user
    )
    return Response(
        serializer.data, status=status.HTTP_201_CREATED
    )


def delete(request, pk, get_object, models):
    obj = get_object_or_404(get_object, id=pk)
    if not models.objects.filter(
        recipe=obj, user=request.user
    ).exists():
        return Response(
            {'message':
                f'Вы не добавляли рецепт {obj}.'}
        )
    models.objects.filter(
        recipe=obj, user=request.user
    ).delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


def render_pdf(ingredients):
    grocery_list = {}
    download = io.BytesIO()
    pdfmetrics.registerFont(
        TTFont('verdana', 'fonts/verdana.ttf', 'UTF-8'))
    for ingredient in ingredients:
        if ingredient[0] not in grocery_list:
            grocery_list[ingredient[0]] = {
                'measurement_unit': ingredient[1],
                'amount': ingredient[2]
            }
        else:
            grocery_list[ingredient[0]]['amount'] += ingredient[2]
    report = canvas.Canvas(download)
    report.setFont('verdana', 22)
    report.drawString(20, 800, 'Cписок покупок:')
    height = 770
    report.setFont('verdana', 14)
    for i, (name, data) in enumerate(grocery_list.items(), 1):
        report.drawString(40, height, (f'{i}. {name.capitalize()} - '
                                       f'{data["amount"]} '
                                       f'{data["measurement_unit"]}'))
        height -= 30
    report.setFont('verdana', 16)
    report.setFillColorRGB(0.25, 0.25, 0.25)
    report.drawCentredString(
        300, 30, 'Продуктовый помощник.'
    )
    report.showPage()
    report.save()
    download.seek(0)
    return download
