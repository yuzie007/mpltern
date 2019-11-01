from PIL import Image

filename = r'../examples/miscellaneous/favicon.png'
img = Image.open(filename)
img.save('_static/favicon.ico')
