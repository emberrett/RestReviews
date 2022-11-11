import os 

def export_vars(request):
    data = {}
    data['MAPS_API_KEY'] = os.environ['MAPS_API_KEY']
    data['FA_KEY'] = os.environ['FA_KEY']
    return data