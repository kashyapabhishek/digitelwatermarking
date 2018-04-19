from django.shortcuts import render
from .forms import UploadFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from PIL import Image, ImageDraw
import os


def index(request):
    contex = {}
    if request.method == 'POST' and request.FILES['myinput']:

        myfile = request.FILES['myinput']
        print("file name :"+myfile.name)
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        upload_file_url = fs.url(filename)
        print("file url"+upload_file_url)
        watermark(myfile)
        contex = {'myfile': upload_file_url, }
        return render(request, "watermark/watermark.html", contex)
    return render(request,"watermark/index.html", contex)


def watermark(myfile):
    print("working dir"+os.getcwd())
    # os.chdir('/home/abhishek/PycharmProjects/watermarking/media/')
    print("working dir" + os.getcwd())
    filename = '/home/abhishek/PycharmProjects/watermarking/media/'+myfile.name
    main = Image.open(filename)
    watermark = Image.new("RGBA", main.size)
    waterdraw = ImageDraw.ImageDraw(watermark, "RGBA")
    waterdraw.text((10, 10), "The Image Project my name is abhishek kashyap ")
    watermask = watermark.convert("L").point(lambda x: min(x, 100))
    watermark.putalpha(watermask)
    main.paste(watermark, None, watermark)
    print(filename)
    main.save(filename, "PNG")
    # return myfile




