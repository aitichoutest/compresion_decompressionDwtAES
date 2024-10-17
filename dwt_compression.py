import numpy as np
import pywt,cv2,os


## Wavelet Compression
def compress(imagePath):
    Image = cv2.imread(imagePath)
    n = 4
    w = 'haar'
    imageName = "img_original.jpg"  
    cv2.imwrite(imageName,Image)
    coeffs = pywt.wavedecn(Image,wavelet=w,level=n)

    coeff_arr, coeff_slices = pywt.coeffs_to_array(coeffs)

    Csort = np.sort(np.abs(coeff_arr.reshape(-1)))

    thresholds = [0.1, 0.05, 0.02, 0.005]
    for keep in thresholds:
        thresh = Csort[int(np.floor((1-keep)*len(Csort)))]
        ind = np.abs(coeff_arr) > thresh
        Cfilt = coeff_arr * ind 
        # Threshold small indices
        coeffs_filt = pywt.array_to_coeffs(Cfilt,coeff_slices,output_format='wavedecn')
    reducedImage = pywt.waverecn(coeffs_filt,wavelet=w)
    
    imageName = "low_res.jpg"  
    cv2.imwrite(imageName,reducedImage)
    
    # saving the coefficents for later restoration
    np.save("imagedata.npy", coeffs)
    return imageName
## Wavelet Decompression
def decompress(imagePath):
    n = 4
    w = 'haar'
    Image = cv2.imread(imagePath)
    coeffs = pywt.wavedecn(Image,wavelet=w,level=n)
    # loading the coefficents of the orginal photo
    coeffs_org = list(np.load("imagedata.npy",allow_pickle=True))
    coeffs[:] = coeffs_org
    coeff_arr, coeff_slices = pywt.coeffs_to_array(coeffs)

    coeffs_filt = pywt.array_to_coeffs(coeff_arr,coeff_slices,output_format='wavedecn')

    imageName = "restored.jpg"
    restoredImage = pywt.waverecn(coeffs_filt,wavelet=w)
    cv2.imwrite(imageName,restoredImage)
    # os.remove("imagedata.npy")
    # os.remove(imagePath)
    return imageName
    