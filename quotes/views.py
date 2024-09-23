from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

quotes = ["Think Different",
          "Stay hungry, stay foolish.",
          "The people who are crazy enough to think they can change the world are the ones who do.",
          "Doing what you love is the key to happiness.",
          "Remembering you are going to die is the best way to avoid thinking you have something to lose."]

images = ["https://cdn.profoto.com/cdn/053149e/contentassets/d39349344d004f9b8963df1551f24bf4/profoto-albert-watson-steve-jobs-pinned-image-original.jpg?width=1280&quality=75&format=jpg",
        "https://editorialcorprens.com.ar/wp-content/uploads/2024/03/steve-jobs-og-iphone.jpg",
        "https://static.k-tuin.com/media/blog/2011/08/steve-jobs-41.jpg",
        "https://content.time.com/time/magazine/archive/covers/2011/1101111017_400.jpg",
        "https://i.blogs.es/d1d709/steve-jobs-next-2/1366_2000.jpeg"]


def quote (request):

    template_name = "quotes/quote.html"
    context = {
        "quote": random.choice(quotes),
        "image": random.choice(images),
    }
    return render(request, template_name, context)

def show_all(request):
    #A function to respond to the /quotes/show_all url
    template_name = "quotes/show_all.html"
    context = {
        "quotes": quotes,
        "images": images,
    }
    return render(request, template_name, context)

def about(request):
    template_name = "quotes/about.html"
    return render(request, template_name)
