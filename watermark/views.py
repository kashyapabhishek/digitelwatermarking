from django.shortcuts import render
from .forms import UploadFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from PIL import Image, ImageDraw
from .mycode.visible import Visible
from .mycode.visible_image import VisibleImage
from .mycode.stegoproject import Invisible
from .forms import UploadFileForm, Retrive


def index(request):

    contex = {'form': UploadFileForm, }

    if request.method == 'POST' and request.FILES['image']:

        MyUploadFileForm = UploadFileForm(request.POST)
        print(MyUploadFileForm)
        watermark_message = MyUploadFileForm.cleaned_data['message']
        myfile = request.FILES['image']
        mainImage = myfile
        watermark_file = request.FILES['watermark_image']
        watermark_message_option = MyUploadFileForm.cleaned_data['option']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        upload_file_url = fs.url(filename)
        print("file url" + upload_file_url)

        if watermark_message_option == 'visible':
            print('under visible')
            if watermark_message is not None:
                myfile = Visible(myfile, watermark_message)
                myfile.watermark()
                print('not none')
                contex = {'myfile': upload_file_url, }
            if watermark_file is not None:
                print("watermark file")
                fs1 = FileSystemStorage()
                filename1 = fs1.save(watermark_file.name, watermark_file)
                upload_file_url1 = fs1.url(filename1)
                print("upload_file_url1"+upload_file_url1)
                vi = VisibleImage()
                vi.imageMark(watermark_file, mainImage)
        if watermark_message_option == 'invisible':
            i = Invisible()
            i.encrypt(watermark_message,myfile)



        else:
            pass
        return render(request, "watermark/watermark.html", contex)
    return render(request,"watermark/index.html", contex)
    #

def imageRetrive(request):
    context = {'form':Retrive}
    if request.method == 'POST' and request.FILES['image']:
        MyUploadFileForm = Retrive(request.POST)
        print(MyUploadFileForm)
        myfile = request.FILES['image']
        if myfile is not None:
            message = Invisible().decrypt(myfile)
            context = {'file':message}
            return render(request, "watermark/resutl.html", context)
        return render(request, "watermark/retrive.html", context)
    return render(request, "watermark/retrive.html", context)



