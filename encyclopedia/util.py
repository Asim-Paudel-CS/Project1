import re
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from django import forms
import operator
import markdown2

class Newsearch(forms.Form):
    searchcont = forms.CharField(label="")

class itmp():
    def __init__(self,itemstr,priority):
        self.itemstr = itemstr
        self.priority = priority

def cfunc(cprog):
    class customdata(forms.Form):
        customapp = forms.CharField(widget= forms.Textarea( attrs={'class': 'customfieldcss'}), label="",required=True, initial = cprog)
    return customdata

def tfunc(titleprog):
    class titledata(forms.Form):
        titleapp = forms.CharField(label="", initial = titleprog)
    return titledata

def dfunc(datafieldprog):
    class editdata(forms.Form):
        editapp = forms.CharField(widget= forms.Textarea( attrs={'class': 'editfieldcss'}), label="",required=True,initial = datafieldprog)
    return editdata

def list_entries():
    #Returns a list of all names of encyclopedia entries.
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))

def save_entry(title, content):
    #Saves an encyclopedia entry, given its title and Markdown content. If an existing entry with the same title already exists, it is replaced.
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

def get_entry(title):
    #Retrieves an encyclopedia entry by its title. If no such entry exists, the function returns None.
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def removeextrapath(pvar):
    slashcount = 0
    phr = "" #pathhostremoved
    for char in pvar:
        if slashcount >= 3:
            phr += char
        if char == "/":
            slashcount += 1
    i = 0
    c = 0
    wiki = False
    for char in phr:
        if i==0 and char == 'w':
            c += 1
        if i==1 and char == 'i':
            c += 1
        if i==2 and char == 'k':
            c += 1
        if i==3 and char == 'i':
            c += 1
        i+=1
    pwr = "" #pathwikiremoved
    i = 0
    if  c == 4:
        for char in phr:
            if i>=5:
                pwr += char
            i+=1
    else:
        pwr = phr

    pathvar = pwr
    newpath = ""
    checkspace = 0
    for char in pathvar:
        if checkspace == 3:
            newpath += " "
            checkspace = 0
        elif char == "%" and checkspace == 0:
            checkspace += 1
        elif checkspace == 1 and char == "2":
            checkspace += 1
        elif checkspace == 2 and char == "0":
            checkspace += 1
        if checkspace == 0:
            newpath += char       
    pwr = newpath

    return pwr

def to_htm(txtgiv):
    converted=""
    hash_count=0 
    hash_counting =False
    hash_counted=False
    head_opened=False

    star_count=0 
    star_counting =False
    star_opened=False

    link_count=0 
    link_txtcount =False
    link_refcount = False
    link_opened=False
    link_txt=""
    link_ref=""

    list_texts = []
    list_text = ""
    list_itm = False
    list_opened = False
    list_return_count = 0
    ulstart = False
    headingtracked = False

    currenttrack=""
    proxy = ""
    n_count = True

    for char in txtgiv:

        #linebreak
        if (char == "\n") and not head_opened and not list_opened:
            if headingtracked == False:
                converted += "<br>"
            else:
                headingtracked = False

        #boldfacetext
        if char == "*":
            star_count += 1
            star_counting = True
        if char != "*" and star_counting:
            if star_count == 1:
                if star_opened == True:
                    converted += "</em>"
                    star_count = 0
                    star_opened = False     
                else:
                    converted += "<em>"
                    star_opened = True
                    star_counting = False
                    star_count = 0
            elif star_count == 2:
                if star_opened == True:
                    converted += "</strong>"
                    star_count = 0   
                    star_opened = False 
                else:
                    converted += "<strong>"
                    star_opened = True
                    star_counting = False
                    star_count = 0
            elif star_count == 3:
                if star_opened == True:
                    converted += "</strong></em>"
                    star_count = 0  
                    star_opened = False   
                else:
                    converted += "<strong><em>"
                    star_opened = True
                    star_counting = False
                    star_count = 0       
            else:
                for i in range(star_count):
                    converted += "*"
                    star_counting = False
                star_count = 0

        #links
        if char == "[":
            link_txtcount = True
            link_opened = True
        if link_txtcount and char != "[" and char != "]":
            link_txt += char
        if link_txtcount and char != "[" and char == "]":
            link_txtcount = False
        if char == "(" and link_opened:
            link_refcount = True
        if link_refcount and char != "(" and char != ")":
            link_ref += char
        if link_refcount and char != "(" and char == ")":
            link_refcount = False
            link_opened = False
            converted += f"<a href ={link_ref}>{link_txt}<a>"
            link_ref = ""
            link_txt = ""                                    

        #Unorderedlist
        if char == "-":
            list_itm=True
            list_opened=True
            list_return_count = 0
        if list_itm == True and char != "-" and char != "\n" and char != "\r":
            list_text += char
        if list_opened == True and char=="\n":
            list_return_count += 1
            list_itm=False
            if list_return_count > 1:
                list_opened=False
                converted += "<ul>"
                for txt in list_texts:
                    converted += "<li>"+txt+"</li>"
                converted += "</ul>" + proxy + "<br>"
                list_itm=False
                list_return_count = 0 
                list_texts = []
            if list_return_count == 1 and list_opened:
                list_texts.append(list_text)
            list_text=""
        if not list_itm and list_opened:
            proxy += char   

        #headings
        if char == "#":
            hash_count += 1
            hash_counting = True
            
        if char != "#" and hash_counting:
            hash_counted=True
            if hash_counted:
                if hash_count >= 1 and hash_count<= 6:
                    converted += f"<h{hash_count}>"
                    head_opened = True
                else:
                    converted += "#"
                hash_counting = False

        if (char == "\r" or char == "\n") and hash_counted:
            converted +=  f"</h{hash_count}>"
            head_opened = False
            hash_counted = False
            hash_count = 0
            headingtracked = True
                             
             
        if char != "#" and char != "\n" and char != "\r" and char != "*" and char != "[" and char != "]" and char != "(" and char != ")" and not link_opened and not list_opened:
            converted += char   

    if list_opened == True:
            list_texts.append(list_text)
            converted += "<ul>"
            for txt in list_texts:
                converted += "<li>"+txt+"</li>"
            converted += "</ul>"
            list_itm=False
            list_opened=False
            list_return_count = 0 
            list_texts = [] 


    return converted

def searchfunction(cont,request):
    customcheck = False
    editcheck = False
    if cont.is_valid():
            searched = cont.cleaned_data["searchcont"]
            listentries = False
    if get_entry(searched) == None:
        listentries = True
        newinst = []
        items_found = []        
        for item in list_entries():
            newinst.append(itmp(item,0))
        i=0
        for eachinstance in newinst:
            for char in searched:
                for charitm in eachinstance.itemstr:
                    if str.lower(char) == str.lower(charitm):
                        newinst[i].priority += 1
            i+=1
        newinst = sorted(newinst, key=operator.attrgetter('priority'), reverse = True) 
        for item in newinst:
            if item.priority >= 2:#pricision
                items_found.append(item.itemstr)
        return render(request, "encyclopedia/index.html", {"editcheck":editcheck,"customcheck":customcheck,"entries": items_found,"listcheck": listentries,"searchcont": Newsearch()})
    else:
        return redirect(f'/wiki/{searched}')

def customfunction(cont,request):
    customcheck = True
    editcheck = False
    listentries = False
    if cont.is_valid():
        datainp = cont.cleaned_data["customapp"]
    return render(request, "encyclopedia/index.html", {"editcheck":editcheck,"fulltxt": to_htm(datainp),"customcheck":customcheck,"listcheck": listentries,"customapp": cfunc(datainp),"searchcont": Newsearch()})

def editfunction(request):
    return None