from cnocr.utils import read_img
from cnocr import CnOcr

ocr = CnOcr()
img_fp = 'ocr/test002.png'
img = read_img(img_fp)
res = ocr.ocr(img)
print("Predicted Chars:", res)
