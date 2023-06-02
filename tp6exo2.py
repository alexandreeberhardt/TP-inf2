import matplotlib.colors
import numpy as np
import matplotlib.pyplot as plt

Citroen = plt.imread('citroen.jpg')  # Ouverture de la photo

Citroen_array = np.array(Citroen)  # Création d'une array pour obtenir toutes les informations de la photo (pas forcément utile)
print('classe :', type(Citroen_array))  # OU plt.imread('citroen.jpg')
print('type :', Citroen_array.dtype)
print('taille :', Citroen_array.shape)
print('modifiable :', Citroen_array.flags.writeable)
plt.imshow(Citroen_array)
plt.title("Photo d'origine de la 2CV")
plt.show()


def rgb_to_hsv(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]  # On sélectionne les canaux R (rouge), V (vert), B (bleu)
    r1 = r / 255
    g1 = g / 255
    b1 = b / 255

    maxc = np.max([r1, g1, b1], axis=0)
    minc = np.min([r1, g1, b1], axis=0)
    deltac = maxc - minc

    choicelist = [0, ((g1 - b1) / deltac % 6), ((b1 - r1) / deltac + 2), ((r1 - g1) / deltac + 4)]
    condlist = [deltac == 0, maxc == r1, maxc == g1, maxc == b1]
    h = 1 / 6 * np.select(condlist, choicelist,0)  # utilisation du np.select comme indiqué dans l'énoncé avec les différentes conditions imposées dans le sujet

    choicelist1 = [0, deltac / maxc]
    condlist1 = [maxc == 0, maxc != 0]
    s = np.select(condlist1, choicelist1, 0)

    v = maxc
    hsv = np.random.rand(400, 600, 3)  # Création d'un ndarray avec les caractéristiques de la photo
    hsv[:, :, 0] = h  # conversion en hsv // ajout des caractéristiques hsv à la photo
    hsv[:, :, 1] = s  # conversion en hsv
    hsv[:, :, 2] = v  # conversion en hsv
    return hsv


def mask(hsv):  # création du masque
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    hsv_copy = np.copy(hsv)

    # Création des caractéristiques avec le masque pour obtenir la photo en hsv avec la carrosserie jaune et le fond mauve
    h_mask = hsv_copy[h > 0.52] = 1.0  # On prend la couleur de la voiture depuis la colobar pour la changer en jaune (rouge en rgb)
    h_mask2 = hsv_copy[h < 0.22] = 0.0
    s_mask = hsv_copy[s > 0.75] = 1.0
    s_mask2 = hsv_copy[s < 0.30] = 0.0
    v_mask = hsv_copy[v < 0.51] = 0.0
    plt.imshow(hsv_copy[:, :, 1])
    plt.title("Carrosserie de la 2CV isolée")
    plt.show()

    # Conversion des masques en tableau booléen pour pouvoir les manipuler ensuite pour retourner au rgb
    h_mask = np.array(h_mask, dtype=bool)
    h_mask2 = np.array(h_mask2, dtype=bool)
    s_mask = np.array(s_mask, dtype=bool)
    s_mask2 = np.array(s_mask2, dtype=bool)
    v_mask = np.array(v_mask, dtype=bool)

    # Inverser les masques pour restaurer le fond / on ne touche pas à la couche H car elle donne la couleur rouge à la voiture
    s_mask_inv = np.invert(s_mask)
    s_mask2_inv = np.invert(s_mask2)
    v_mask_inv = np.invert(v_mask)

    # Appliquer les masques aux canaux H, S et V de l'image HSV
    hsv_copy[..., 0][h_mask] = 1.0
    hsv_copy[..., 0][h_mask2] = 0.0
    hsv_copy[..., 1][s_mask] = 0.8
    hsv_copy[..., 1][s_mask2] = 0.6
    hsv_copy[..., 2][v_mask] = 1.0

    # Restaurer le fond en utilisant les masques inverses a part pour la couche H pour garder la couleur rouge
    '''hsv_copy[..., 0][h_mask_inv] = h[h_mask_inv]
    hsv_copy[..., 0][h_mask2_inv] = h[h_mask2_inv]'''
    hsv_copy[..., 1][s_mask_inv] = s[s_mask_inv]
    hsv_copy[..., 1][s_mask2_inv] = s[s_mask2_inv]
    hsv_copy[..., 2][v_mask_inv] = v[v_mask_inv]

    # Convertir l'image HSV en RVB
    rgb_image = matplotlib.colors.hsv_to_rgb(hsv_copy)

    # Afficher l'image
    plt.imshow(rgb_image)
    plt.colorbar()
    plt.title("Carrosserie de la 2CV isolée en RGB")
    plt.show()
    '''hsv_copy[h > 0.52] = 0.52
    hsv_copy[h < 0.22] = 0.22
    hsv_copy[s > 0.75] = 0.75
    hsv_copy[s < 0.30] = 0.3
    nvelle = matplotlib.colors.hsv_to_rgb(hsv_copy) #Apres avoir essayé multiples tentatives pour remettre les couleurs de fond d'origine ainsi que la voiture en rouge, nous n'avons pas réussi
    plt.imshow(nvelle)
    plt.colorbar()
    plt.show()'''


def main():
    # On convertit la photo en hsv puis on affiche les différnets canaux H,S,V
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
    plt.title("Canal S")
    plt.show()
    plt.imshow(citroen_hsv[:, :, 2])
    plt.colorbar()
    plt.title("Canal V")
    plt.show()

    mask(citroen_hsv)  # On applique le masque à la voiture


if __name__ == '__main__':
    main()

'''Malheuresmeent, nous n'avons pas réussi à retrouver l'image d'origine avec les fonctions demandées par l'énoncé
 Le fond reste un petit peu rouge malgré la nette démarcation de la voiture en rouge
 Nous avons aussi essayé sans utiliser les fonctions données par l'énonce, voici le code (qui fonctionne et renvoie l'image avec le bon fond et la carrosserie de la voiture en rouge) : 


from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# On charge l'image grâce au module PIL
image = Image.open('citroen.jpg')

# On affiche l'image d'origine
plt.imshow(image)
plt.title("2CV sans modification")
plt.axis('off')

# On convertit l'image en HSV
hsv_image = image.convert('HSV')

# On sépare les canaux H,S,V afin de travailler sur eux plus facilement
h_channel, s_channel, v_channel = hsv_image.split()

# Affochage des différents canaux comme demandé dans l'énoncé
plt.imshow(h_channel, cmap='hsv')
plt.title("Canal H")
plt.axis('off')

plt.imshow(s_channel, cmap='gray')
plt.title("Canal S")
plt.axis('off')

plt.imshow(v_channel, cmap='gray')
plt.title("Canal V")
plt.axis('off')


plt.show()

# Convertion des canaux en tableau numpy pour pouvoir travailler dessus 
h_array = np.array(h_channel)
s_array = np.array(s_channel)
v_array = np.array(v_channel)

# Déterminer les seuils en utilisant matplotlib.pyplot.colorbar
plt.imshow(h_channel, cmap='hsv')
plt.colorbar()
plt.title("Histogramme du Canal H")

plt.imshow(v_channel, cmap='gray')
plt.colorbar()
plt.title("Histogramme du Canal V")

plt.show()

# Seuils déterminés avec les histogrammes
h_min, s_min, v_min = 130, 100, 50
h_max, s_max, v_max = 150, 255, 255

# On crée le masque en utilisant les seuils pour extraire les couleurs voulues
mask = np.logical_and.reduce((h_array >= h_min, h_array <= h_max,
                              s_array >= s_min, s_array <= s_max,
                              v_array >= v_min, v_array <= v_max))

# On convertit le masque en tableau d'entiers
mask = mask.astype(np.uint8) * 255

# On applique le masque pour extraire uniquement les pixels correspondant à la carrosserie de la voiture
masked_image = Image.fromarray(np.array(image) * np.expand_dims(mask, axis=2))

# On modifie la couleur bleue en rouge dans l'image masquée
pixels = masked_image.load()
for i in range(masked_image.size[0]):
    for j in range(masked_image.size[1]):
        if mask[j, i] != 0:
            pixels[i, j] = (255, 0, 0)

# On affiche l'image résultante
masked_image.show()

# On convertit le masque en une instance de Image
mask_image = Image.fromarray(mask)

# On fusionne l'image filtrée avec l'image d'origine
filtered_image = Image.fromarray(np.array(image))
filtered_image.paste(masked_image, (0, 0), mask=mask_image)

# On affiche l'image résultante
filtered_image.show()

'''


