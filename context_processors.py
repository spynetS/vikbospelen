
def site_data(request):
    return {
        "site_data": getattr(request, "site_data", None)
    }
