# Set client's name
# if [ "$#" -ne 1 ]; then
#     echo "Usage: ./gen-client.sh <username>"
#     exit 1
# fi

USERNAME=user

# Generate keypair for client
echo "Generating keypair"
openssl genrsa -out private_key.pem -3 3072

# Generate a certificate signing request
echo "Generating CSR"
openssl req -new -key private_key.pem -out ${USERNAME}.csr -subj "/CN=${USERNAME}"

# Generate a certificate for the client signed by the signer
echo "Signing CSR"
openssl x509 -req -in ${USERNAME}.csr -CA root_cert.crt -CAkey root.pem -CAcreateserial -out cert_chain.crt

rm ${USERNAME}.csr
rm *.srl
