from flask import Flask, request, url_for, jsonify
from logging.handlers import RotatingFileHandler
import logging
import urllib, cStringIO
import os
import Image
from ImageChops import subtract, difference
import numpy
from scipy import ndimage
import math
import ImageFilter
import piggyphoto
import time

app = Flask(__name__)

@app.route("/get_image_url", methods=['POST'])
def get_image_url():
    url = request.form.get('url', '')
    img_id = request.form.get('id', str(int(time.time())))
    app.logger.info((url, url[-3:], img_id))
    img_name = '%s.jpg' % img_id
    img_loc = 'static/flickr/%s' % img_name

    if not os.path.exists(img_loc):
        app.logger.info("Retrieving image from url")
        f = cStringIO.StringIO(urllib.urlopen(url).read())
        img = Image.open(f)
        img.save(img_loc)

    return jsonify({'url' : img_loc})


@app.route("/take_background", methods=['POST'])
def take_background():
    uid = request.form.get('uid', str(int(time.time())))
    img_name = '%s.jpg' % (uid)
    img_loc = 'static/bg/%s' % img_name

    C = piggyphoto.camera()
    C.capture_image('/tmp/bg.jpg')

    os.rename('/tmp/bg.jpg', img_loc)

    return jsonify({'url' : img_loc})

@app.route("/take_both", methods=['POST'])
def take_both():
    uid = request.form.get('uid', str(int(time.time())))
    img_name = '%s.jpg' % (uid)
    img_loc = 'static/both/%s' % img_name

    C = piggyphoto.camera()
    C.capture_image('/tmp/both.jpg')
    os.rename('/tmp/both.jpg', img_loc)

    return jsonify({'url' : img_loc})


@app.route("/bs", methods=['POST'])
def bs():
    uid = request.form.get('uid', str(int(time.time())))
    img_id = request.form.get('id')
    img_loc = 'static/flickr/%s.jpg' % (img_id)
    img = Image.open(img_loc)
    bg = img

    cap = Image.open('static/bg/%s.jpg' % uid)
    cap2 = Image.open('static/both/%s.jpg' % uid)

    bgs = bg.size
    ins = cap2.size
    rh = ins[0] * 1.0 / (bgs[0] * 0.6)
    rw = ins[1] * 1.0 / (bgs[1] * 0.6)
    size = int(round(ins[0] / rh)), int(round(ins[1] / rw))


    diff = difference(cap, cap2)
    diff = diff.filter(ImageFilter.MedianFilter(5))

    rgb2L = (
        1, 1, 1, 1)
    diff = diff.convert("L", rgb2L)

    diff = numpy.array(diff)


    diff = diff > 100
    diff = diff.astype(numpy.int)
    diff = ndimage.binary_fill_holes(diff).astype(int)

    eroded_square = ndimage.binary_erosion(diff, structure=numpy.ones((20,20)))
    diff = ndimage.binary_propagation(eroded_square, mask=diff)

    # eroded_square = ndimage.binary_erosion(diff, structure=numpy.ones((20,20)))
    # diff = ndimage.binary_propagation(eroded_square, mask=diff)

    diff = diff * 255

    diff = Image.fromarray(diff)
    diff = diff.convert('1')

    box = diff.getbbox()
    diff = diff.crop(box)
    cap2 = cap2.crop(box)


    cap2.thumbnail(size, Image.ANTIALIAS)
    diff.thumbnail(size, Image.ANTIALIAS)

    psize = cap2.size

    bg.paste(cap2, ((bgs[0] / 2) - (psize[0] / 2),
            int(bgs[1]) - (psize[1])), diff)

    bs_img = '%s.jpg' % uid
    bg.save(os.path.join('static', 'composite', bs_img))
    return jsonify(url='static/composite/%s.jpg' % uid)

if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.debug = True
    app.run()