from django.shortcuts import render

# Create your views here.
def Prof_page_main(request) -> render:
    return render(request,"Professeur.html")