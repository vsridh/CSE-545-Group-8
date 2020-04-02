from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
from django.http import HttpResponse

import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import cryptography.exceptions
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives.asymmetric import rsa

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


#generate key function
#generate private key and public key
def generate_key():
    # Generate the public/private key pair.
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend(),
    )

    # Save the private key to a file.
    with open('private.key', 'wb') as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    # Save the public key to a file.
    with open('public.pem', 'wb') as f:
        f.write(
            private_key.public_key().public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )
    return



#sign file function
#use private key to sign statement file
#generate sign file, it use to verificate
#The sign file and statement file is corresponding
#private_key---string of private_key file
#file_name ---- string of file should sign
def sign_file(private_key, file):
    # Load the private key.
    #private_key=private.key
    with open(private_key, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend(),
        )
    # Load the contents of the file to be signed.

    with open(file, 'rb') as f:
         payload = f.read()
    #file = file.encode("ISO-8859-1")
    #payload = bytearray(file)

    # Sign the payload file.
    #genertae sign file, it should send to verification
    signature = base64.b64encode(
        private_key.sign(
            payload,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
    )
    with open('signature5.txt', 'wb') as f:
        f.write(signature)
    return signature

#verificate_file function
#need statement file and sign file,  two file is corresponding
#public_key---string of private_key file
#file_name ---- string of file should verificate
#sign_file ----- string of sign file which generate by sign file function, use to verificate
def verify_file(public_key,file_name,sign_file):
    # Load the public key.
    #public_key=public.pem
    with open(public_key, 'rb') as f:
        public_key = load_pem_public_key(f.read(), default_backend())

    # Load the statement contents and the signature.
    #file_name='statement.txt'
    with open(file_name, 'rb') as f:
        payload_contents = f.read()
        print(payload_contents)
    #sign_file='signature.sig'
    with open(sign_file, 'rb') as f:
        signature = base64.b64decode(f.read())

    # Perform the verification.
    try:
        public_key.verify(
            signature,
            payload_contents,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        # this file is pass verification
        # to do more
        ##############
    except cryptography.exceptions.InvalidSignature as e:
        #this file is fail
        #ERROR
        print('ERROR: Payload and/or signature files failed verification!')
    return
