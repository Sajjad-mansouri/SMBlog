from blog.models import IpAddress


class SaveIpAddressMiddleWare:

    def __init__(self,get_response):
        self.get_response=get_response

    def __call__(self,request):

        x_forwarded_for=request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address=x_forwarded_for.split(',')[0]
        else:
            ip_address=request.META.get('REMOTE_ADDR')

        try:
            ip_address=IpAddress.objects.get(ip=ip_address)
        except IpAddress.DoesNotExist:
            ip_address=IpAddress(ip=ip_address)
            ip_address.save()

        request.ip_address=ip_address


        response=self.get_response(request)


        return response