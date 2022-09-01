from django.shortcuts import render, redirect 
from markdown2 import Markdown 

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
        "content": Markdown().convert(content)
    })

def search(request):
    query = request.GET.get("q", "")
    entries = util.list_entries()
    found_entries = [ 
        valid_entry
        for valid_entry in entries
        if query.lower() in valid_entry.lower()
    ]
    
    if query is None or query == "":
        return render(
            request, 
            "encyclopedia/search.html",
            {"found_entries": "",
             "query": query
            }
        )
        
    if len(found_entries) == 1:
        return redirect("wiki", found_entries[0])
    
    return render(
        request, 
        "encyclopedia/search.html",
        {"found_entries": found_entries, "query": query}
    )