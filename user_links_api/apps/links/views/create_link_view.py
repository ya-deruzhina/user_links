from ..serializers import LinksSerializer
from ..models import LinksModel
from .parser_view import xpath

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

import requests, re

from django.core.files.base import ContentFile


class LinkCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        cookies = {
        '_ga_5LK9Y0PNLQ': 'GS1.1.1731794718.8.0.1731794718.60.0.0',
        '_ga': 'GA1.1.1728279502.1728934335',
        '_ym_uid': '169384474267578418',
        '_ym_d': '1728934336',
        'sessionid': 'eaz4v8pekewjiuklquj4enjgzy5chjfy',
        'csrftoken': 'g3JhO77QcBIaXDswePm7yf7yFhbxbQg7fyOl7bTUVz46D2Ab32yWXGABCdG9gJWX',
        '_ym_isad': '2',
        '_ym_visorc': 'w',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:131.0) Gecko/20100101 Firefox/131.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8',
            'Accept-Language': 'ru,en-US;q=0.7,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br, zstd',
            'Connection': 'keep-alive',
            # 'Cookie': '_ga_5LK9Y0PNLQ=GS1.1.1731794718.8.0.1731794718.60.0.0; _ga=GA1.1.1728279502.1728934335; _ym_uid=169384474267578418; _ym_d=1728934336; sessionid=eaz4v8pekewjiuklquj4enjgzy5chjfy; csrftoken=g3JhO77QcBIaXDswePm7yf7yFhbxbQg7fyOl7bTUVz46D2Ab32yWXGABCdG9gJWX; _ym_isad=2; _ym_visorc=w',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Priority': 'u=0, i',
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }


        try:
            url = request.POST['url']
            page = requests.get(url,cookies=cookies, headers=headers).content.decode('UTF-8')

            title = xpath(page, '//meta[@property="og:title"]//@content').extract_first()
            if title == '' or not title:
                title = xpath(page, '//head/title//text()').extract_first()
            
            description = xpath(page, '//meta[@property="og:description"]//@content').extract_first()
            if description == '' or not description:
                description = xpath(page, '//meta[@name="Description"]//@content').extract_first()
                if description == '' or not description:
                    description = xpath(page, '//meta[@name="description"]//@content').extract_first()
                    if description == '' or not description:
                        description = xpath(page, '//meta[@name="description"]//text()').extract_first()

            url_page = xpath(page, '//meta[@property="og:url"]//@content').extract_first()
            if url_page =='' or not url_page:
                url_page = xpath(page, '//head//@url').extract_first()
                if url_page ==''or not url_page:
                    url_page = xpath(page,'//head//link[@rel="canonical"]//@href').extract_first()
                    url_page = url
            
            url_site = re.findall(r'\/\/([\d\D]+?\.[\D]{2,3})\/',url_page)[0]
            image = xpath(page, '//meta[@property="og:image"]//@content').extract_first()
            if image == '' or not image:
                image = xpath(page, '//head//@image').extract_first()
                if image == '' or not image:
                    image = xpath(page, '//img//@src').extract_first()            
            
            if 'https://' in url_page and 'https://' not in image and 'http://' not in image:
                image = f'https://{url_site}{image}'
            elif 'http://' in url_page and 'http://' not in image and 'https://' not in image:
                image = f'http://{url_site}{image}'

            kind_link = xpath(page, '//meta[@property="og:type"]//@content').extract_first()
            
            if kind_link:
                kind_link = kind_link.upper()
                if kind_link not in LinksModel.KIND_LINKS:
                    kind_link = kind_link.split('.')[0]
                    if kind_link not in LinksModel.KIND_LINKS:
                        kind_link = 'WEBSITE'
            else:
                kind_link = 'WEBSITE'
          
            owner = request.user.id
            if image:
                id_image = int(LinksModel.objects.all().order_by('-id')[0].id)+1
                type_image = image.split('.')[-1]
                name_image = f'{id_image}.{type_image}'
                response = requests.get(image, stream=True,cookies=cookies, headers=headers)
                response.raise_for_status()
                image = ContentFile(response.content, name=name_image)

            data = {
                'title':title,
                'description':description,
                'url_page':url_page,
                'image':image,
                'kind_link':kind_link,
                'owner':owner,
            }

            if len(LinksModel.objects.filter(url_page=url_page).filter(owner=owner))>0:
                status = HTTP_400_BAD_REQUEST
                return Response ({"Status":"Link Already Used"},status=status)

            serializer = LinksSerializer(data=data)
            serializer.is_valid(raise_exception=True)

        except:
            status = HTTP_404_NOT_FOUND
            return Response({'Status':"Sent Invalid Data"},status=status)

        else:
            serializer.save()
            return Response (serializer.data)

