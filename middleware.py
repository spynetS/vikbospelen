#!/usr/bin/env python3

from pages.models import Page


class SiteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        pages: Page = Page.objects.filter(url=request.path)

        if len(pages) > 0:
            request.site_data = {"main_text":pages[0].main_text}

        response = self.get_response(request)
        return response
