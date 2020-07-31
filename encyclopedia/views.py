from django.shortcuts import render, redirect
from . import util
import markdown2
from django.core.files import File

def index(request):
    editcheck = False
    listentries = False
    customcheck = False
    if request.method == "POST":     
        return util.searchfunction(util.Newsearch(request.POST),request)
    else:
        listentries = True
        return render(request, "encyclopedia/index.html", {"editcheck":editcheck,"customcheck":customcheck,"entries": util.list_entries(),"listcheck": listentries,"searchcont": util.Newsearch()})

def content(request,titleinp):
    editcheck = False
    listentries = False
    customcheck = False
    return render(request,"encyclopedia/index.html",{"editcheck":editcheck,"customcheck":customcheck,"titleurl":titleinp,"fulltxt": markdown2.markdown(util.get_entry(titleinp)),"listcheck": listentries,"searchcont": util.Newsearch()})

def custom(request):
    editcheck = False
    listentries = False
    customcheck = True
    if request.method == "POST":
        return util.customfunction(util.customdata(request.POST),request)
    else:
        return render(request, "encyclopedia/index.html", {"editcheck":editcheck,"customcheck":customcheck,"listcheck": listentries,"customapp": util.customdata(),"searchcont": util.Newsearch()})

def edit(request):
    titleini="Title"
    dataini="Use Markdown2 Format"
    pathvar = request.META.get('HTTP_REFERER')
    if pathvar == None:
        pathvar = "addoredit"
    else:
        pathvar = util.removeextrapath(pathvar)
    customcheck = False
    listentries = False
    editcheck = True
    existingitem = False
    for item in util.list_entries():
        if str.lower(pathvar) == str.lower(item):
            existingitem = True
    if request.method == "POST":
        tit = util.tfunc(titleini)(request.POST)
        cont = util.dfunc(dataini)(request.POST)
        if cont.is_valid():
            datainp = cont.cleaned_data["editapp"] 
        if tit.is_valid():
            titleinp =  tit.cleaned_data["titleapp"]
                  
        #add new post
        righthead = f"Add New Entry"
        with open(f'entries/{titleinp}.md','w') as f:
            currentfile = File(f)
            currentfile.write(datainp)
        
        return redirect(f'/wiki/{titleinp}')

    else:
        #modify existing get
        if existingitem:
            titleini = pathvar
            dataini = util.get_entry(pathvar)
            righthead = f"Edit Entry for <strong>{str.upper(pathvar)}</strong>"
            return render(request, "encyclopedia/index.html", {"righthead":righthead,"editcheck":editcheck,"fulltxt":f"getmod:{pathvar}","customcheck":customcheck,"listcheck": listentries,"editapp": util.dfunc(dataini),"searchcont": util.Newsearch(),"title": util.tfunc(titleini)})
        #add new get
        else:
            righthead = f"Add new entry"
            return render(request, "encyclopedia/index.html", {"righthead":righthead,"editcheck":editcheck,"fulltxt":f"getadd:{pathvar}","customcheck":customcheck,"listcheck": listentries,"editapp": util.dfunc(dataini),"searchcont": util.Newsearch(),"title": util.tfunc(titleini)})


    


