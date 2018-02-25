import numpy as np
from skimage.io import imread  #, imsave
from skimage.transform import resize
from keras.models import load_model
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Line
from kivy.properties import StringProperty, NumericProperty

class Painter(Widget):

    text_box = StringProperty()
    line_width = NumericProperty()

    def __init__(self, **kwargs):
        super(Painter, self).__init__(**kwargs)
        self.text_box = ''
        self.line_width = 30
        self.model1 = load_model('mod1.h5')
        self.model2 = load_model('mod2.h5')

    def predict(self):
        self.export_to_png('img.png')
        img = imread('img.png')
        _ = int(img.shape[1]*0.8)      # crop & drop, resize, reshape
        processed = resize(img[:, :_ ,0], (28,28)).reshape(1,28,28,1)
        pred1 = np.argmax(self.model1.predict(processed))
        pred2 = np.argmax(self.model2.predict(processed))

        if pred1 == pred2:
            self.text_box = str(pred1)
        else:
            self.text_box = '%d or %d' % (pred1, pred2)

    def width_change(self, size_up):
        if size_up and self.line_width < 50:
            self.line_width += 1
            self.text_box = str(self.line_width)
        elif not size_up and self.line_width > 2:
            self.line_width -= 1
            self.text_box = str(self.line_width)
        else:
            self.text_box = 'OOB error'

    def clear_canv(self):
        self.canvas.clear()
        self.text_box = ''

    def on_touch_down(self, touch):
        with self.canvas:
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=self.line_width)

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]

class DigitRecogApp(App):

    def build(self):
        return FloatLayout()

DigitRecogApp().run()
