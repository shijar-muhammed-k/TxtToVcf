import os
import os
from PIL import Image
from pytesseract import pytesseract
import re
from django.http import HttpResponse
from django.shortcuts import render
from .models import txtfile, imagefile

# Create your views here.
def index(request):
    return render(request, "index.html")


def imageToTextHome(request):
    return render(request, 'imageToText.html')


def convert(request):
    res = 0
    con = txtfile()
    count = 0
    if request.method == "POST":
        con.file = request.FILES['textfile']
        con.save()
        path = str(con.file)
        with open(path, 'r') as txt:
            values = txt.readlines()
        if len(values) <= 0:
            msg = 1
        else:
            for data in values:
                csv = data.split(",")
                if len(csv) == 2:
                    res = main(csv, path)
                    msg = 3
                else:
                    count += 1

                if count == len(values):
                    msg = 2

        os.remove(path)
        return render(request, 'index.html', {'res' : res, 'msg' : msg})
    else:
        return render(request, 'index.html')


def download(request, path):
    file = "Files/" + path
    with open(file, 'r') as f:
        data = f.read()

    os.remove(file)

    response = HttpResponse(data, content_type="application/vcard.vcf")
    response['Content-Disposition'] = "attachment; filename=vcard.vcf"
    return response




def main(csv, path):

        first_name   = csv[0]
        last_name    = ''
        email        = ''
        company      = ''
        title        = ''
        phone_number = csv[1]
        address      = ''
        vcf_file = path[:(len(path)-4)] +'.csv'
        vcard = make_vcard(first_name, last_name, company, title, phone_number, address, email)
        write_vcard(vcf_file, vcard)

        return vcf_file[6:]

def make_vcard(
        first_name,
        last_name,
        company,
        title,
        phone,
        address,
        email):
    address_formatted = ';'.join([p.strip() for p in address.split(',')])
    return [
        'BEGIN:VCARD',
        'VERSION:2.1',
        f'N:{last_name};{first_name}',
        f'FN:{first_name} {last_name}',
        f'ORG:{company}',
        f'TITLE:{title}',
        f'EMAIL;PREF;INTERNET:{email}',
        f'TEL;WORK;VOICE:{phone}',
        f'ADR;WORK;PREF:;;{address_formatted}',
        f'REV:1',
        'END:VCARD'
    ]

def write_vcard(f, vcard):
    with open(f, 'a') as f:
        f.writelines([l + '\n' for l in vcard])


def imageconvert(request):
    if request.method == "POST":
        nums = []
        con = imagefile()
        path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        pytesseract.tesseract_cmd = path_to_tesseract
        name = request.POST['name']
        number = int(request.POST['number'])
        con.file = request.FILES['imagefile']
        con.save()
        text = pytesseract.image_to_string(str(con.file))
        ma = re.findall('\d\d\d\d\d\s\d\d\d\d\d', text)
        for i in ma:
            nums.append(i.replace(' ', ""))
        if(name == ''):
            name = 'Number'
        if(number == ''):
            number = 1

        res = r'Files\text.txt'
        with open (res, 'a') as wr:
            for i in nums:
                wr.writelines(f'{name}{number},{i}\n')
                number += 1
        
        count = len(nums)
        if count == 0:
            msg = 1
        else:
            msg = 3
        
        os.remove(str(con.file))
        return render(request, 'imageToText.html', {'res' : res[6:], 'msg' : msg, 'Count' : count})
    else:    
        return render(request, 'imageToText.html')


def txtdownload(request, path):
    file = "Files/" + path
    with open(file, 'r') as f:
        data = f.read()

    os.remove(file)

    response = HttpResponse(data, content_type="application/text.txt")
    response['Content-Disposition'] = "attachment; filename=text.txt"
    return response
