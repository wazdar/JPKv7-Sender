import base64
import json
import os
import re
import requests
import string
import zipfile
from io import BytesIO
from Crypto import Random
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Hash import SHA256, MD5
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
from azure.storage.blob import BlobClient

MF_URL = 'https://test-e-dokumenty.mf.gov.pl/api/Storage'
KEY_SIZE = 32  # AES256
BS = 16


def get_status(ref_number):
    resp = requests.get('%s/Status/%s' % (MF_URL, ref_number))
    return resp.json()


def create_init_upload(file):
    jpk_nazwa = os.path.basename(file)
    jpk_xml = open(file, 'rb').read()
    jpk = {'xml_nazwa': jpk_nazwa,
           'kod': re.search('kodSystemowy="(\w+) ', jpk_xml.decode('utf-8')).group(1),
           'xml_len': len(jpk_xml)
           }
    # losowy 256 bitowy klucz szyfrujący
    key = Random.new().read(KEY_SIZE)

    # szyfrowanie kluczem szyfrującym MF algo RSA
    klucz_mf = RSA.importKey(open('msf/test_e_dokumenty.mf.gov.pl.pem', 'r').read())
    rsa_cipher = PKCS1_v1_5.new(klucz_mf)
    jpk['key'] = base64.b64encode(rsa_cipher.encrypt(key)).decode()

    # sha256 dla pliku jpk
    xml_hash = SHA256.new()
    xml_hash.update(jpk_xml)
    jpk['xml_hash'] = base64.b64encode(xml_hash.digest()).decode()

    # Utworzenie archiwum zip z plikiem jpk
    zipio = BytesIO()
    with zipfile.ZipFile(zipio, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr(jpk_nazwa, jpk_xml)
    jpk_zip = zipio.getvalue()

    # szyfrowanie pliku
    iv = Random.new().read(16)
    jpk['iv'] = base64.b64encode(iv).decode()

    obj = AES.new(key, AES.MODE_CBC, iv)
    jpk_aes = obj.encrypt(pad(jpk_zip, BS))

    # md5 zaszyfrowanego archiwum zip
    md5 = MD5.new()
    md5.update(jpk_aes)

    jpk['zip_nazwa'] = jpk_nazwa.replace('.xml', '.zip')
    jpk['zip_len'] = len(jpk_zip)
    jpk['zip_hash'] = base64.b64encode(md5.digest()).decode()

    # Zapisanie zaszyfrowanego pliku zip (to będzie wysyłane w kroku upload)
    with open(jpk['zip_nazwa'], 'wb') as f:
        f.write(jpk_aes)

    initupload_xml = open('./jpk_support/initupload.tpl.xml', 'rb')
    templ = string.Template(initupload_xml.read().decode('utf-8'))
    initupload_xml = templ.substitute(jpk)

    # Zapisanie pliku initupload.xml
    with open(jpk_nazwa[:-4] + '-initupload.xml', 'wb') as f:
        f.write(initupload_xml.encode())

    return os.path.abspath(jpk_nazwa[:-4] + '-initupload.xml')


def send_jpk(init_upload_xml):
    xml = open(init_upload_xml, 'rb').read()
    headers = {'Content-Type': 'application/xml'}
    resp = requests.post(MF_URL + '/InitUploadSigned', data=xml, headers=headers, verify=True)
    if resp.status_code != 200:
        print('InitUploadSigned', resp.status_code, repr(resp.text))
        return resp

    data = json.loads(resp.text)
    reference = data.get(u'ReferenceNumber')
    blob_list = []
    for element in data.get(u'RequestToUploadFileList'):
        blob_name = element.get(u'BlobName')
        file_name = element.get(u'FileName')
        sas_url = element.get(u'Url')
        blob_list.append(blob_name)
        blob_client = BlobClient.from_blob_url(sas_url)

        with open(file_name, "rb") as data:
            blob_client.upload_blob(data, blob_type="BlockBlob")

    data = {'ReferenceNumber': reference, 'AzureBlobNameList': blob_list}
    headers = {'Content-Type': 'application/json'}
    resp = requests.post(MF_URL + '/FinishUpload', data=json.dumps(data), headers=headers, verify=True)

    if resp.status_code != 200:
        print(f'FinishUpload {resp.status_code} {repr(resp.text)}')
        return resp

    resp.reference = reference

    return resp