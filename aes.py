import sys
import cv2,os
import numpy as np
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# Set mode
mode = AES.MODE_CBC

# Set sizes
keySize = 32
ivSize = AES.block_size if mode == AES.MODE_CBC else 0

def saveKey(key):
    with open("key.txt",'wb') as keyFile:
        keyFile.write(key)
def loadKey():
    with open("key.txt",'rb') as keyFile:
        key = keyFile.read()
    
    return key


# Start Encryption 
def encrypt(file_to_encrypt):

# Load original image
    imageOrig = cv2.imread(file_to_encrypt)
    # os.remove(file_to_encrypt)
    # coeffs_org = list(np.load("imagedata.npy",allow_pickle=True))
    # imageOrig[:] = coeffs_org
    rowOrig, columnOrig, depthOrig = imageOrig.shape

    # Check for minimum width
    minWidth = (AES.block_size + AES.block_size) // depthOrig + 1
    if columnOrig < minWidth:
        print('The minimum width of the image must be {} pixels, so that IV and padding can be stored in a single additional row!'.format(minWidth))
        sys.exit()

 
    # Convert original image data to bytes
    imageOrigBytes = imageOrig.tobytes()

    # Encrypt
    key = get_random_bytes(keySize)
    iv = get_random_bytes(ivSize)
    cipher = AES.new(key, AES.MODE_CBC, iv) if mode == AES.MODE_CBC else AES.new(key, AES.MODE_ECB)
    imageOrigBytesPadded = pad(imageOrigBytes, AES.block_size)
    ciphertext = cipher.encrypt(imageOrigBytesPadded)


    paddedSize = len(imageOrigBytesPadded) - len(imageOrigBytes)
    void = columnOrig * depthOrig - ivSize - paddedSize
    ivCiphertextVoid = iv + ciphertext + bytes(void)
    imageEncrypted = np.frombuffer(ivCiphertextVoid, dtype = imageOrig.dtype).reshape(rowOrig + 1, columnOrig, depthOrig)

  

    cv2.imwrite("enc_"+file_to_encrypt, imageEncrypted)
    saveKey(key)
    # saving information about the encrypted image that cannot be saved
    # in the encryped image
    np.save('encryptedData.npy',imageEncrypted)
    imageEncryptedPath = "enc_"+file_to_encrypt
    return imageEncryptedPath


# Start Decryption 
def decrypt(encryptedImagePath):
    key = loadKey()
    
    # loading information about the encrypted image that cannot be saved
    # in the encryped image
    encryptedImage = np.load('encryptedData.npy')
    
    os.remove('encryptedData.npy')
    rowEncrypted, columnOrig, depthOrig = encryptedImage.shape 
    rowOrig = rowEncrypted - 1
    encryptedBytes = encryptedImage.tobytes()
    iv = encryptedBytes[:ivSize]
    imageOrigBytesSize = rowOrig * columnOrig * depthOrig
    paddedSize = (imageOrigBytesSize // AES.block_size + 1) * AES.block_size - imageOrigBytesSize
    encrypted = encryptedBytes[ivSize : ivSize + imageOrigBytesSize + paddedSize]

    # Decrypt
    cipher = AES.new(key, AES.MODE_CBC, iv) if mode == AES.MODE_CBC else AES.new(key, AES.MODE_ECB)
    decryptedImageBytesPadded = cipher.decrypt(encrypted)
    decryptedImageBytes = unpad(decryptedImageBytesPadded, AES.block_size)

    # Convert bytes to decrypted image data
    decryptedImage = np.frombuffer(decryptedImageBytes, encryptedImage.dtype).reshape(rowOrig, columnOrig, depthOrig)
    
    cv2.imwrite("dec_"+encryptedImagePath, decryptedImage)
    imageDecryptedPath = "dec_"+encryptedImagePath
    return imageDecryptedPath
