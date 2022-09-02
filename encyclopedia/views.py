from django.shortcuts import render, redirect 
from markdown2 import Markdown 
from django import forms 
from django.core.files.storage import default_storage
import random
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
    
class new_entry_form(forms.Form):
    title = forms.CharField(
        required = True,
        label = "Title",
        widget = forms.TextInput()
    )
    content = forms.CharField(
        required = True,
        label = "Content",
        widget=forms.Textarea())
        
def new_entry(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_entry.html", {
            "form": new_entry_form().as_p
        })
        
    form = new_entry_form(request.POST)
    if form.is_valid():
        title = form.cleaned_data.get("title")
        content = form.cleaned_data.get("content")
        filename = f"entries/{title}.md"
        if default_storage.exists(filename):
            return render(request, "encyclapedia/new_entry.html", {
                "error": "Entry already exist",
                "form": form.as_p
            })
        else:
            with open(f"entries/{title}.md", "w") as file:
                file.write(content)
            return redirect("wiki", title)
    else:
        return render(request, "encyclpedia/new_entry.html", {
            "form": form.as_p
        })
        
def random_entry(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return redirect("wiki", entry)

def edit(request, entry):
    if request.method == "GET":
        title = entry
        content = util.get_entry(title)
        form = new_entry_form({
            "title": title,
            "content": content
        })
        return render(
            request, 
            "encyclopedia/edit.html",
            {
                "title": title,
                "form": form.as_p
             },
        )
        
    form = new_entry_form(request.POST)
    if form.is_valid(): 
        title = form.cleaned_data.get("title")
        content = form.cleaned_data.get("content")
        util.save_entry(title=title, content=content)
        return redirect("wiki", title)