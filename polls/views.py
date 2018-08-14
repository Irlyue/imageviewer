import os
import glob

from django.shortcuts import render
from django.http import HttpResponse
from . import image_utils as iu
from concurrent import futures
from tqdm import tqdm
from threading import Thread

# Create your views here.

names = []
name2id = {}


def index(request):
    context = {'names': names}
    return render(request, 'polls/index.html', context=context)


def image_id(request, idx):
    return render(request, 'polls/image.html',
                  context={
                      'image_id': idx,
                      'name': names[idx],
                      'n_images': len(names),
                      'prev_id': max(0, idx - 1),
                      'next_id': min(len(names) - 1, idx + 1),
                  })


def image_name(request, name):
    idx = name2id[name]
    return image_id(request, idx=idx)


def initialize():
    global names, name2id
    local_names = [name.split('.')[0] for name in os.listdir('static/images')]
    name2id = {name: i for i, name in enumerate(local_names)}
    generate_image_thumb(local_names)
    names = local_names
    print('Done initialization!')


def generate_image_thumb(image_names, in_dir='static/images', out_dir='static/thumbs'):
    in_path_fmt = os.path.join(in_dir, '%s.jpg')
    out_path_fmt = os.path.join(out_dir, '%s.jpg')
    with futures.ThreadPoolExecutor(4) as pool:
        thumbs = []
        print('Generating thumbs...')
        for image in tqdm(pool.map(lambda _name: iu.read_image(in_path_fmt % _name), image_names),
                          total=len(image_names)):
            shp = image.shape[:2]
            out_shp = shrink_larger_size_to(shp, 150)
            image_thumb = iu.resize_image(image, out_shp)
            thumbs.append(image_thumb)
        print('Saving thumbs...')
        for _ in tqdm(pool.map(lambda _image, _name: iu.save_image(_image, out_path_fmt % _name), thumbs, image_names),
                      total=len(image_names)):
            pass
    print('Done generating thumbs!')


def shrink_larger_size_to(shp, n):
    h_old, w_old = shp
    if h_old > w_old:
        h_new = n
        w_new = int(w_old * n / h_old)
    else:
        w_new = n
        h_new = int(h_old * n / w_old)
    return h_new, w_new


def init_with_a_separate_thread():
    t = Thread(target=initialize)
    t.start()


init_with_a_separate_thread()
