
from dataclasses import dataclass
from cryptography.x509 import Certificate
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey


@dataclass
class KeyPair():
    cert: Certificate
    key: RSAPrivateKey