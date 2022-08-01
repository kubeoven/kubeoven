import datetime
from typing import Tuple

from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def create_ca(cn: str) -> Tuple[x509.Certificate, rsa.RSAPrivateKey]:
    ca_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    subject = issuer = x509.Name(
        [
            x509.NameAttribute(NameOID.COMMON_NAME, cn),
        ]
    )
    usage = x509.KeyUsage(
        digital_signature=True,
        key_encipherment=True,
        key_cert_sign=True,
        content_commitment=False,
        crl_sign=False,
        data_encipherment=False,
        decipher_only=False,
        encipher_only=False,
        key_agreement=False,
    )
    ca_cert = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(ca_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=3650))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .add_extension(usage, critical=True)
        .sign(ca_key, hashes.SHA256(), default_backend())
    )
    return ca_cert, ca_key
