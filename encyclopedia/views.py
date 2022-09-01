from django.shortcuts import render

from . import util

# Create Views Here 

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, entry):
    content = util.get_entry(entry)
    
    return render(request, "encyclopedia/wiki.html", {
        "title": entry,
        "content": content
    })
