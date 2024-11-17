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
        'ps_l': '1',
        'ps_n': '1',
        'mid': 'Zq9BaAAEAAELVEwsoL3EovszmcLZ',
        'datr': 'Z0GvZr0dT1zjDZEDPpK8xdB3',
        'ig_did': '4D0A7D2B-2A33-47DA-A941-D99376C803C5',
        'ig_nrcb': '1',
        'csrftoken': 't7pHgrErNIBIyi67qsTsIyaaCKzkhTYY',
        'ds_user_id': '4492254664',
        'sessionid': '4492254664%3AelPXos7AnVHWvr%3A7%3AAYdJvpRyl1slhHH55kgTawswNof6QWSA5Y1XT418gpk',
        'wd': '1920x431',
        'ig_direct_region_hint': '"PRN\\0544492254664\\0541763332619:01f7e56ad77bcc523c3ff6360f5287487231e1be83e028ef4fb749778de23e767518ab2f"',
        'rur': '"CLN\\0544492254664\\0541763401394:01f7caccc48a7cb92aab35aac80c529f5413c7a675a5767c71975e58bfed6d5f0a13540b"',
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
          
            owner = request.user.id
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
            # import pdb; pdb.set_trace()
            serializer = LinksSerializer(data=data)
            serializer.is_valid(raise_exception=True)

        except:
            status = HTTP_404_NOT_FOUND
            return Response({'Status':"Sent Invalid Data"},status=status)

        else:
            serializer.save()
            return Response (serializer.data)

