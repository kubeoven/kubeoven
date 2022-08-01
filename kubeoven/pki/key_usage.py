
from cryptography import x509

KeyUsageServer = x509.ExtendedKeyUsage([x509.OID_SERVER_AUTH])
KeyUsageClient = x509.ExtendedKeyUsage([x509.OID_CLIENT_AUTH])
KeyUsageBoth = x509.ExtendedKeyUsage([x509.OID_SERVER_AUTH, x509.OID_CLIENT_AUTH])
