import cv2

def parlaklik_olc(goruntu):
    gri = cv2.cvtColor(goruntu, cv2.COLOR_BGR2GRAY)
    return gri.mean()

def dinamik_esik(parlaklik):
    if parlaklik > 180:
        return 0.2
    elif parlaklik > 150:
        return 0.3
    elif parlaklik > 90:
        return 0.4
    else:
        return 0.5

def histogram_esitleme_uygula(kare):
    yuv = cv2.cvtColor(kare, cv2.COLOR_BGR2YUV)
    yuv[:, :, 0] = cv2.equalizeHist(yuv[:, :, 0])
    return cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)