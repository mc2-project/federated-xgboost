# Helper script to generate keys + certificate for the trusted authority (signer)
# The authority signs the enclave binary, and also acts as the CA for signing client identities

# Generate keypair for signer
openssl genrsa -out root.pem -3 3072
openssl rsa -in root.pem -pubout -out root.pub

# Generate self-signed root certificate
openssl req -x509 -new -nodes -key root.pem -sha256 -days 3650 -out root_cert.crt -subj "/CN=root"
