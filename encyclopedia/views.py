from django.shortcuts import render
from . import util
import markdown2

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

    for char in txtgiv:

        #linebreak
        if (char == "\r" or char == "\n") and not head_opened and not list_opened:
            converted += "<br>"

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
        if list_opened == True and char=="\n" or char=="\r":
            list_return_count += 1
            list_itm=False
            if list_return_count <= 1:
                list_texts.append(list_text)
            list_text=""
            if list_return_count > 1:
                converted += "<ul>"
                for txt in list_texts:
                    converted += "<li>"+txt+"</li>"
                converted += "</ul>"
                list_itm=False
                list_opened=False
                list_return_count = 0 
                list_texts = []                                      

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
            converted += "</h1>"
            head_opened = False
            hash_counted = False
            hash_count = 0
                             
             
        if char != "#" and char != "\n" and char != "\r" and char != "*" and char != "[" and char != "]" and char != "(" and char != ")" and not link_opened and not list_opened:
            converted += char   

    return converted

#htmconvertedmd = markdown2.markdown(util.get_entry("CSS"))
htmconvertedmd = to_htm(util.get_entry("Git"))

def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries(),"fulltxt": htmconvertedmd})

