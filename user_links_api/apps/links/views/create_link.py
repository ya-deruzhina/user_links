from ..serializers import LinksSerializer
from ..models import LinksModel
# from ..forms import ImageForm

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import requests, re
from .parser import xpath

            # form = ImageForm(request.POST, request.FILES)
  
        #     # if form.is_valid():
        # 
        #         # form.save()

class LinkCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        try:
            url = request.POST['url']
            page = requests.get(url).content.decode('UTF-8')

            title = xpath(page, '//meta[@property="og:title"]//@content').extract_first()
            if title == '' or not title:
                title = xpath(page, '//head/title//text()').extract_first()
            
            description = xpath(page, '//meta[@property="og:description"]//@content').extract_first()
            if description == '' or not description:
                description = xpath(page, '//meta[@name="Description"]//@content').extract_first()
                if description == '' or not description:
                    description = xpath(page, '//meta[@name="description"]//@content').extract_first()

            url_page = xpath(page, '//meta[@property="og:url"]//@content').extract_first()
            if url_page =='' or not url_page:
                url_page = xpath(page, '//head//@url').extract_first()
                if url_page ==''or not url_page:
                    url_page = xpath(page,'//head//link[@rel="canonical"]//@href').extract_first()
                    url_page = url
            
            url_site = re.findall(r'\/\/([\d\D]+?\.[\D]{2,3})\/',url_page)[0]
            image = xpath(page, '//meta[@property="og:image"]//@content').extract_first()
            if image == '' or not image:
                xpath(page, '//head//@image').extract_first()
                if image == '' or not image:
                    image = xpath(page, '//img//@src').extract_first()
            
            if 'https://' in url_page and 'https://' not in image:
                image = f'https://{url_site}{image}'
            elif 'http://' in url_page and 'http://' not in image:
                image = f'http://{url_site}{image}'

            kind_link = xpath(page, '//meta[@property="og:type"]//@content').extract_first()
            print(kind_link)
            
            if kind_link:
                kind_link = kind_link.upper()
                if kind_link not in LinksModel.KIND_LINKS:
                    kind_link = kind_link.split('.')[0]
                    if kind_link not in LinksModel.KIND_LINKS:
                        kind_link = 'WEBSITE'
            else:
                kind_link = 'WEBSITE'
            
            owner = request.user.id

            data = {
                'title':title,
                'description':description,
                'url_page':url_page,
                'image':image,
                'kind_link':kind_link,
                'owner':owner
            }
            if len(LinksModel.objects.filter(url_page=url_page).filter(owner=owner))>0:
                return Response ({"Link":"Already Used"})
            serializer = LinksSerializer(data=data)
            serializer.is_valid(raise_exception=True)

        except:
            return Response ({"NO":"data"})

        else:
            serializer.save()
            return Response (serializer.data)

