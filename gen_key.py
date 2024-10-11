from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

# 生成 256 位私钥
private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())

# 保存私钥到文件
with open("./private_key.pem", "wb") as private_key_file:
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    private_key_file.write(private_key_bytes)

# 生成公钥
public_key = private_key.public_key()

# 保存公钥到文件
with open("./public_key.pem", "wb") as public_key_file:
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    public_key_file.write(public_key_bytes)

print("Keys saved to files.")
