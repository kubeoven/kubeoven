from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PrivateFormat,
    NoEncryption,
    load_pem_private_key,
)


def pem_decode_key(data: bytes) -> rsa.RSAPrivateKey:
    return load_pem_private_key(data, None)
    
def pem_encode_key(key: rsa.RSAPrivateKey):
    return key.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption(),
    )

def pem_decode_cert(data: bytes):
    return x509.load_pem_x509_certificate(data)

def pem_encode_cert(cert: x509.Certificate):
    return cert.public_bytes(Encoding.PEM)
