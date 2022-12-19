import os

from django.http import HttpResponse
from django.shortcuts import render
from .models import txtfile

# Create your views here.
def home(request):
    return render(request, "index.html")


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
                if len(csv) == 7:
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
        last_name    = csv[1]
        email        = csv[2]
        company      = csv[3]
        title        = csv[4]
        phone_number = csv[5]
        address      = csv[6]
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
