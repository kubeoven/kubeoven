import datetime
from ipaddress import ip_address
from typing import List
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from .key_pair import KeyPair


def create_cert(
    ca: KeyPair,
    cn: str,
    org: str,
    dns: List[str],
    addresses: List[str],
    key_usage: x509.ExtendedKeyUsage,
) -> KeyPair:
    cert_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    new_subject = x509.Name(
        [
            x509.NameAttribute(NameOID.COMMON_NAME, cn),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, org),
        ]
    )

    dns_names = [x509.DNSName(name) for name in dns]
    ip_addresses = [x509.IPAddress(ip_address(address)) for address in addresses]
    sans = [*dns_names, *ip_addresses]
    usage = x509.KeyUsage(
        digital_signature=True,
        key_encipherment=True,
        content_commitment=False,
        crl_sign=False,
        data_encipherment=False,
        decipher_only=False,
        encipher_only=False,
        key_agreement=False,
        key_cert_sign=False,
    )
    builder = (
        x509.CertificateBuilder()
        .subject_name(new_subject)
        .issuer_name(ca.cert.issuer)
        .public_key(cert_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.utcnow())
        .not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=1825))
        .add_extension(usage, critical=True)
        .add_extension(key_usage, critical=False)
    )
    if len(sans) > 0:
        sans_ext = x509.SubjectAlternativeName(sans)
        builder = builder.add_extension(sans_ext, critical=False)
    cert = builder.sign(ca.key, hashes.SHA256(), default_backend())
    return KeyPair(cert, cert_key)
