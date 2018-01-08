# coding=utf-8
from flask_assets import Environment, Bundle


css_all = Bundle('css/main.css',
                 'css/bootstrap.css',
                 filters='cssmin', output='css/all.css')


js_all = Bundle(
    'js/jquery.js',
    'js/bootstrap.js',
    filters='jsmin', output='js/all.js')


def init_app(app):
    webassets = Environment(app)
    webassets.register('css_all', css_all)
    webassets.register('js_all', js_all)
    webassets.manifest = 'cache' if not app.debug else False
    webassets.cache = not app.debug
    webassets.debug = not app.debug
