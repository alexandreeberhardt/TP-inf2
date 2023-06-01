import matplotlib.colors
import numpy as np
import matplotlib.pyplot as plt
Citroen = plt.imread('citroen.jpg')

Citroen_array = np.array(Citroen)
print('classe :',type(Citroen_array)) #OU plt.imread('citroen.jpg')
print( 'type :', Citroen_array.dtype)
print( 'taille :', Citroen_array.shape)
print( 'modifiable :', Citroen_array.flags.writeable)
plt.imshow(Citroen_array)
plt.title("Photo d'origine de la 2CV")
plt.show()

def rgb_to_hsv(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    r1 = r/255
    g1 = g/255
    b1 = b/255

    maxc = np.max([r1, g1, b1],axis=0)
    minc = np.min([r1, g1, b1],axis=0)
    deltac = maxc - minc

    choicelist = [0, ((g1-b1)/deltac % 6), ((b1-r1)/deltac+2), ((r1-g1)/deltac+4)]
    condlist = [deltac == 0, maxc == r1, maxc == g1, maxc == b1]
    h = 1/6*np.select(condlist, choicelist, 0)

    choicelist1 = [0, deltac/maxc]
    condlist1 = [maxc == 0, maxc != 0]
    s = np.select(condlist1, choicelist1, 0)

    v = maxc
    hsv = np.random.rand(400,600,3)
    hsv[:, :, 0] = h
    hsv[:, :, 1] = s
    hsv[:, :, 2] = v
    return hsv


def mask(hsv):
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    hsv_copy = np.copy(hsv)
    '''hsv_copy = np.copy(hsv)
    hsv_copy[hsv[:, :, 1] > 0.70] = 1.0
    hsv_copy[hsv[:, :, 1] < 0.6] = 0.0
    hsv_copy[hsv[:, :, 2] < 0.53] = 0.0
    plt.imshow(hsv_copy[:,:,1])
    plt.title("carrosserie de la 2CV isolée")
    plt.show()
    
    nvelle = matplotlib.colors.hsv_to_rgb(hsv_copy)
    plt.imshow(nvelle)
    plt.colorbar()
    plt.show()'''
    hsv_copy[h > 0.52] = 1.0
    hsv_copy[h < 0.22] = 0.0
    hsv_copy[s > 0.75] = 1.0
    hsv_copy[s < 0.30] = 0.0
    hsv_copy[v < 0.51] = 0.0
    plt.imshow(hsv_copy[:, :, 1])
    plt.title("Carrosserie de la 2CV isolée")
    plt.show()

    
    nvelle = matplotlib.colors.hsv_to_rgb(hsv_copy)
    plt.imshow(nvelle)
    plt.colorbar()
    plt.show()

def main():
    citroen_hsv = rgb_to_hsv(Citroen_array)
    plt.imshow(citroen_hsv)
    plt.title("HSV")
    plt.show()
    plt.imshow(citroen_hsv[:, :, 0])
    plt.colorbar()
    plt.title("Canal H")
    plt.show()
    plt.imshow(citroen_hsv[:, :, 1])
    plt.colorbar()
    plt.title("Canal S") #Seul qui fait ressortir la carrosserie, c'est donc lui que l'on doit modifier
    plt.show()
    plt.imshow(citroen_hsv[:, :, 2])
    plt.colorbar()
    plt.title("Canal V")
    plt.show()

    mask(citroen_hsv)

if __name__ == '__main__':
    main()




