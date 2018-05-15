from django.shortcuts import render
from .forms import UploadFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from PIL import Image, ImageDraw
from .mycode.visible import Visible
from .mycode.visible_image import VisibleImage
from .mycode.stegoproject import Invisible
from .mycode.dwt import DWT, extract_dwt
from .forms import UploadFileForm, Retrive


def index(request):

    contex = {'form': UploadFileForm, }

    if request.method == 'POST' and request.FILES['image']:

        MyUploadFileForm = UploadFileForm(request.POST)
        print(MyUploadFileForm)
        watermark_message = MyUploadFileForm.cleaned_data['message']
        myfile = request.FILES['image']
        mainImage = myfile
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
            try:
                watermark_file = request.FILES['watermark_image']
                if watermark_file is not None:
                    print("watermark file")
                    fs1 = FileSystemStorage()
                    filename1 = fs1.save(watermark_file.name, watermark_file)
                    upload_file_url1 = fs1.url(filename1)
                    print("upload_file_url1" + upload_file_url1)
                    vi = VisibleImage()
                    vi.imageMark(watermark_file, mainImage)
            except Exception:
                print("Error")
            else:
                watermark_file = None
        if watermark_message_option == 'invisible':
            print("under invisible ")
            try:
                watermark = request.FILES['watermark_image']
                fs1 = FileSystemStorage()
                filename1 = fs1.save(watermark.name, watermark)
                upload_file_url1 = fs1.url(filename1)
                print("upload_file_url1" + upload_file_url1)
                if watermark is not None:
                    print("DWT")
                    url = DWT(myfile, watermark)
                    print("jfsalj"+url)
                    contex = {'myfile': upload_file_url, }
                    return render(request, "watermark/watermark.html", contex)
            except Exception:
                Invisible().encrypt(watermark_message, myfile)
                print("gjjjjjjjjjjjjh")
                contex = {'myfile':upload_file_url}
                return render(request, "watermark/watermark.html", contex)
                print("end")

        return render(request, "watermark/watermark.html", contex)
    return render(request, "watermark/index.html", contex)


def imageRetrive(request):
    context = {'form': Retrive}
    if request.method == 'POST' and request.FILES['image']:
        MyUploadFileForm = Retrive(request.POST)
        print(MyUploadFileForm)
        myfile = request.FILES['image']
        try:
            watermark = request.FILES['coverImage']
            if watermark is not None:
                extract_dwt(myfile, watermark)
                context = {'myfile': 'C:/Users/saumy/PycharmProjects/Dwt watermark/src/media/extracted.jpg'}
                return render(request, "watermark/watermark.html", context)
        except Exception:
            message = Invisible().decrypt(myfile)
            context = {'file': message}
            return render(request, "watermark/resutl.html", context)

    return render(request, "watermark/retrive.html", context)



