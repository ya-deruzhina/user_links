from ..serializers import LinksSerializer
from ..models import LinksModel
from .parser_view import xpath
from ..services.headers import headers
from ..services.cookies import cookies

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST

import requests, re

from django.core.files.base import ContentFile


class LinkCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            owner = request.user.id
            url = request.POST['url']

            try:
                page = requests.get(url,cookies=cookies, headers=headers).content.decode('UTF-8')
            except:
                page = requests.get(url,cookies=cookies, headers=headers).text

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
                      
            types_image_example = ['bmp', 'dib', 'gif', 'jfif', 'jpe', 'jpg', 'jpeg', 'pbm', 'pgm', 'ppm', 'pnm', 'pfm', 'png', 'apng', 'blp', 
                           'bufr', 'cur', 'pcx', 'dcx', 'dds', 'ps', 'eps', 'fit', 'fits', 'fli', 'flc', 'ftc', 'ftu', 'gbr', 'grib', 
                           'h5', 'hdf', 'jp2', 'j2k', 'jpc', 'jpf', 'jpx', 'j2c', 'icns', 'ico', 'im', 'iim', 'mpg', 'mpeg', 'tif', 
                           'tiff', 'mpo', 'msp', 'palm', 'pcd', 'pdf', 'pxr', 'psd', 'qoi', 'bw', 'rgb', 'rgba', 'sgi', 'ras', 'tga', 
                           'icb', 'vda', 'vst', 'webp', 'wmf', 'emf', 'xbm', 'xpm']
            
            if image:
                id_image = int(LinksModel.objects.all().order_by('-id')[0].id)+1
                type_image = image.split('.')[-1]
                if type_image not in types_image_example:
                    type_image = 'jpg'    
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

