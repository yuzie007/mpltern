from PIL import Image

filename = r'../examples/miscellaneous/favicon.png'
img = Image.open(filename)
icon_sizes = [(16, 16), (32, 32), (48, 48)]
img.save('_static/favicon.ico', sizes=icon_sizes)
