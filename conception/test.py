# import requests
# from bs4 import BeautifulSoup
# import os

# # Lien de la page
# url = "https://e-hentai.org/s/c513829faa/1784319-24"

# # Requête HTTP
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "html.parser")

# # Créer un dossier pour enregistrer les images
# os.makedirs("images", exist_ok=True)

# # Trouver toutes les balises <img>
# for i, img in enumerate(soup.find_all("img")):
#     src = img.get("src")
#     if src:
#         # Si le lien est relatif, le compléter
#         if src.startswith("//"):
#             src = "https:" + src
#         elif src.startswith("/"):
#             src = url + src

#         try:
#             # Télécharger l’image
#             img_data = requests.get(src).content
#             with open(f"images/image_{i}.jpg", "wb") as f:
#                 f.write(img_data)
#             print(f"Téléchargé: {src}")
#         except Exception as e:
#             print(f"Erreur pour {src}: {e}")
take = 'hery' + '1'
print(take)