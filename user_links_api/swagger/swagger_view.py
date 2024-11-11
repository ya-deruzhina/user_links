from django.views import View
from django.shortcuts import render
from .swagger_json_builder import SwaggerJSONBuilder

import json


class SwaggerView(View):
    def get(self, request, *args, **kwargs):
        swagger_definition = SwaggerJSONBuilder.call()
        context = {
            'swaggerDefinition': json.dumps(swagger_definition)
        }
        return render(request, 'openapi/index.html', context=context)
