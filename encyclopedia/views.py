from django.shortcuts import render
from . import util
import markdown2

#htmconvertedmd = markdown2.markdown(util.get_entry("Git"))
#htmconvertedmd = to_htm(util.get_entry("Git"))
    
def index(request):
    listentries = False
    if request.method == "POST":
        return util.searchfunction(util.Newsearch(request.POST),request)
    else:
        listentries = True
        return render(request, "encyclopedia/index.html", {"entries": util.list_entries(),"listcheck": listentries,"searchcont": util.Newsearch()})

def content(request,titleinp):
    listentries = False
    return render(request,"encyclopedia/index.html",{"titleurl":titleinp,"fulltxt": markdown2.markdown(util.get_entry(titleinp)),"listcheck": listentries,"searchcont": util.Newsearch()})





