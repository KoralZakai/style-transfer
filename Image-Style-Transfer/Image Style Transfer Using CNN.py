"""Image Style Transfer Using Convolutional Neural Network
code Written in python, Ui made with PyQt5"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
import threading
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QFile, QTextStream
import ctypes

#don't delete using python files with image and css source
import design
import css
import os

# global variables created to control the UI and code parameters.
global content_path
global style_path
global outputImage
global pixmap
global exitflag
exitflag=0
global flag1
flag1=0
global flag2
flag2=0
global flag3
flag3=0
global count
count=0
global iter
iter = 0

class Transfer_Image_Gui(QWidget):
    def __init__(self, parent=None):
        super(Transfer_Image_Gui, self).__init__(parent)
        self.show
        # init the initial parameters of this GUI
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        self.title = 'Style Maker'
        self.width = w
        self.height = h
        self.initUI()

    def initUI(self):
        file = QFile(':css/StyleSheet.css')
        file.open(QFile.ReadOnly)
        stream = QTextStream(file)
        text = stream.readAll()
        self.setStyleSheet(text)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(":Pictures/logo.png"))
        self.setGeometry(0, 0, self.width, self.height - 60)

        # Creating main container-frame, parent it to QWindow
        self.main_frame = QtWidgets.QFrame(self)
        self.main_frame.setObjectName("MainFrame")
        self.main_frame.setFixedWidth(self.width)
        self.main_frame.setFixedHeight(self.height)
        self.main_layout = QtWidgets.QVBoxLayout(self.main_frame)

        # the Icons sub frame
        self.Iconsub_Frame = QtWidgets.QFrame(self.main_frame)
        self.Iconsub_Frame.setFixedHeight(75)
        self.main_layout.addWidget(self.Iconsub_Frame)
        self.Iconsub_Layout = QtWidgets.QHBoxLayout(self.Iconsub_Frame)
        self.Iconsub_Layout.setAlignment(Qt.AlignLeft)

        # help button
        helpBtn = QtWidgets.QPushButton("", self)
        helpBtn.setStyleSheet("QPushButton {background: url(:Pictures/help.png) no-repeat transparent;} ")
        helpBtn.setFixedWidth(68)
        helpBtn.setFixedHeight(68)
        helpBtn.clicked.connect(Main_Window.showHelp)
        self.Iconsub_Layout.addWidget(helpBtn)

        # home button
        homeBtn = QtWidgets.QPushButton("", self)
        homeBtn.setStyleSheet("QPushButton {background: url(:Pictures/home.png) no-repeat transparent;} ")
        homeBtn.setFixedWidth(68)
        homeBtn.setFixedHeight(68)
        homeBtn.clicked.connect(self.showHome)
        self.Iconsub_Layout.addWidget(homeBtn)

        # The style + conntent buttons sub frame
        self.Buttonsub_Frame = QtWidgets.QFrame(self.main_frame)
        self.main_layout.addWidget(self.Buttonsub_Frame)
        self.Buttonsub_Layout = QtWidgets.QHBoxLayout(self.Buttonsub_Frame)
        self.Buttonsub_Frame.setFixedWidth(self.width)
        self.Buttonsub_Layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        # upload content button
        contentBtn = QtWidgets.QPushButton("Upload content image", self)
        contentBtn.setObjectName("MainGuiButtons")
        contentBtn.clicked.connect(self.setContentImage)
        contentBtn.setStyleSheet("QPushButton {width: 250px;} ")
        self.Buttonsub_Layout.addWidget(contentBtn)

        # upload style
        StyleBtn = QtWidgets.QPushButton("Upload style Image", self)
        StyleBtn.setObjectName("MainGuiButtons")
        StyleBtn.clicked.connect(self.setStyleImage)
        StyleBtn.setStyleSheet("QPushButton {width: 250px;} ")
        self.Buttonsub_Layout.addWidget(StyleBtn)

        # The style + conntent photos sub frame
        self.Photosub_Frame = QtWidgets.QFrame(self.main_frame)
        self.main_layout.addWidget(self.Photosub_Frame)
        self.Photosub_Layout = QtWidgets.QHBoxLayout(self.Photosub_Frame)
        self.Photosub_Frame.setFixedWidth(self.width)
        self.Photosub_Layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        styleframe = QtWidgets.QLabel()
        styleframe.setGeometry(QtCore.QRect(350, 90, 251, 191))
        styleframe.setFrameShape(QtWidgets.QFrame.NoFrame)
        styleframe.setText("")
        styleframe.setPixmap(QtGui.QPixmap(":Pictures/logo.png"))
        styleframe.setScaledContents(True)
        styleframe.setObjectName("styleframe")
        self.Photosub_Layout.addWidget(styleframe)

        contentframe = QtWidgets.QLabel()
        contentframe.setGeometry(QtCore.QRect(350, 90, 251, 191))
        contentframe.setFrameShape(QtWidgets.QFrame.NoFrame)
        contentframe.setText("")
        contentframe.setPixmap(QtGui.QPixmap(":Pictures/logo.png"))
        contentframe.setScaledContents(True)
        contentframe.setObjectName("contentframe")
        self.Photosub_Layout.addWidget(contentframe)

        # Footer layout
        creditsLbl = QtWidgets.QLabel('Created By Koral Zakai & May Steinfeld, '
                                      'Supervisor: Zeev Vladimir Volkovich, '
                                      '03/06/2019')
        creditsLbl.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(creditsLbl)

        # show the window
        self.showMaximized()

    # Opens home window
    def showHome(self):
        """
        close current window and return to home page
        """
        self.parent().show()
        self.parent().main_frame.setVisible(True)
        self.close()
        """saveimage function control the saving of the output image."""

    """setContentImage function control on choosing the content image."""
    def setContentImage(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileNames(None, "Select Image", "",
                                                             "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if fileName:
            global content_path
            content_path = fileName[0]
            pixmap = QtGui.QPixmap(fileName[0])
            pixmap = pixmap.scaled(290, 290, QtCore.Qt.KeepAspectRatio)
            self.contentframe.setPixmap(pixmap)
            self.contentframe.setAlignment(QtCore.Qt.AlignCenter)
            global flag1
            flag1 = 1
            global flag2
            if (flag1 == 1 and flag2 == 1):
                self.outputframe.show()
               # self.warninglabel.hide()
                #self.generatebutton.show()
                #self.pluslabel.show()
                #self.equalabel.show()

    """setStyleImage function control on choosing the style image."""
    def setStyleImage(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileNames(None, "Select Image", "",
                                                             "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if fileName:
            global style_path
            style_path = fileName[0]
            pixmap = QtGui.QPixmap(fileName[0])
            pixmap = pixmap.scaled(290, 290, QtCore.Qt.KeepAspectRatio)
            self.styleframe.setPixmap(pixmap)
            self.styleframe.setAlignment(QtCore.Qt.AlignCenter)
            global flag2
            flag2 = 1
            global flag1
            if (flag2 == 1 and flag1 == 1):
                self.outputframe.show()
                #self.warninglabel.hide()
                #self.generatebutton.show()
               # self.pluslabel.show()
               # self.equalabel.show()

    def saveimage(self):
        global outputImage
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Select Image", "",
                                                            "Image Files (*.jpg *.png *.jpeg *.bmp)")
        if (fileName):
            outputImage.save(fileName)

class Gui_output_image_window(QWidget):
    def __init__(self, parent=None):
        super(Gui_output_image_window, self).__init__(parent)
        self.show
        # init the initial parameters of this GUI
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        self.title = 'Style Maker'
        self.width = w
        self.height = h
        self.initUI()

    def initUI(self):
        file = QFile(':css/StyleSheet.css')
        file.open(QFile.ReadOnly)
        stream = QTextStream(file)
        text = stream.readAll()
        self.setStyleSheet(text)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(":Pictures/logo.png"))
        self.setGeometry(0, 0, self.width, self.height - 60)

        # Creating main container-frame, parent it to QWindow
        self.main_frame = QtWidgets.QFrame(self)
        self.main_frame.setObjectName("MainFrame")
        self.main_frame.setFixedWidth(self.width)
        self.main_frame.setFixedHeight(self.height)
        self.main_layout = QtWidgets.QVBoxLayout(self.main_frame)

        # the Icons sub frame
        self.Iconsub_Frame = QtWidgets.QFrame(self.main_frame)
        self.Iconsub_Frame.setFixedHeight(75)
        self.main_layout.addWidget(self.Iconsub_Frame)
        self.Iconsub_Layout = QtWidgets.QHBoxLayout(self.Iconsub_Frame)
        self.Iconsub_Layout.setAlignment(Qt.AlignLeft)

        # help button
        helpBtn = QtWidgets.QPushButton("", self)
        helpBtn.setStyleSheet("QPushButton {background: url(:Pictures/help.png) no-repeat transparent;} ")
        helpBtn.setFixedWidth(68)
        helpBtn.setFixedHeight(68)
        helpBtn.clicked.connect(Main_Window.showHelp)
        self.Iconsub_Layout.addWidget(helpBtn)

        # home button
        homeBtn = QtWidgets.QPushButton("", self)
        homeBtn.setStyleSheet("QPushButton {background: url(:Pictures/home.png) no-repeat transparent;} ")
        homeBtn.setFixedWidth(68)
        homeBtn.setFixedHeight(68)
        homeBtn.clicked.connect(Transfer_Image_Gui.showHome)
        self.Iconsub_Layout.addWidget(homeBtn)

        # The Output + Button save sub frame
        self.Buttonsub_Frame = QtWidgets.QFrame(self.main_frame)
        self.main_layout.addWidget(self.Buttonsub_Frame)
        self.Buttonsub_Layout = QtWidgets.QVBoxLayout(self.Buttonsub_Frame)
        self.Buttonsub_Frame.setFixedWidth(self.width)
        self.Buttonsub_Layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        # Save button for the output image
        SaveOutputImageBtn = QtWidgets.QPushButton("Save your image", self)
        SaveOutputImageBtn.setObjectName("MainGuiButtons")
        SaveOutputImageBtn.clicked.connect(self.saveimage)
        self.Buttonsub_Layout.addWidget(SaveOutputImageBtn)

        # outputImage get the result from the MainFunc.
        # outputImage = self.MainFunc(content_path, style_path, iter, resolution)
        # pixmap = QtGui.QPixmap(outputImage.toqpixmap())
        # pixmap = pixmap.scaled(290, 290, QtCore.Qt.KeepAspectRatio)
        #self.outputframe.setPixmap(pixmap)
        #self.outputframe.setAlignment(QtCore.Qt.AlignCenter)
        # Setting up the logo
        outputImage = QtWidgets.QLabel('', self)
        pixmap = QPixmap(":Pictures/logo.png")
        pixmap = pixmap.scaled(290, 290, QtCore.Qt.KeepAspectRatio)
        outputImage.setPixmap(pixmap)
        self.Buttonsub_Layout.addWidget(outputImage)
        outputImage.setAlignment(Qt.AlignCenter)

        # Footer layout
        creditsLbl = QtWidgets.QLabel('Created By Koral Zakai & May Steinfeld, '
                                      'Supervisor: Zeev Vladimir Volkovich, '
                                      '03/06/2019')
        creditsLbl.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(creditsLbl)

        # show the window
        self.showMaximized()

    """saveimage function control the saving of the output image."""
    def saveimage(self):
        global outputImage
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Select Image", "",
                                                            "Image Files (*.jpg *.png *.jpeg *.bmp)")
        if (fileName):
            outputImage.save(fileName)

"""Main_Window is the main class of the UI,
all UI parameters and code functions defined here."""
class Main_Window(QWidget):
    def __init__(self, parent=None):
        super(Main_Window, self).__init__(parent)
        # init the initial parameters of this GUI
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        self.title = 'Style Maker'
        self.width = w
        self.height = h
        self.initUI()

    def initUI(self):
        file = QFile(':css/StyleSheet.css')
        file.open(QFile.ReadOnly)
        stream = QTextStream(file)
        text = stream.readAll()
        self.setStyleSheet(text)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(":Pictures/logo.png"))
        self.setGeometry(0, 0, self.width, self.height-60)

        #Creating main container-frame, parent it to QWindow
        self.main_frame = QtWidgets.QFrame(self)
        self.main_frame.setObjectName("MainFrame")
        self.main_frame.setFixedWidth(self.width)
        self.main_frame.setFixedHeight(self.height)
        self.main_layout = QtWidgets.QVBoxLayout(self.main_frame)

        # the Icons sub frame
        self.Iconsub_Frame = QtWidgets.QFrame(self.main_frame)
        self.Iconsub_Frame.setFixedHeight(75)
        self.main_layout.addWidget(self.Iconsub_Frame)
        self.Iconsub_Layout = QtWidgets.QHBoxLayout(self.Iconsub_Frame)
        self.Iconsub_Layout.setAlignment(Qt.AlignLeft)

        # help button
        helpBtn = QtWidgets.QPushButton("", self)
        helpBtn.setStyleSheet("QPushButton {background: url(:Pictures/help.png) no-repeat transparent;} ")
        helpBtn.setFixedWidth(68)
        helpBtn.setFixedHeight(68)
        helpBtn.clicked.connect(self.showHelp)
        self.Iconsub_Layout.addWidget(helpBtn)

        # the Icon sub frame
        self.Logosub_Frame = QtWidgets.QFrame(self.main_frame)
        self.Logosub_Frame.setFixedWidth(self.width)
        self.main_layout.addWidget(self.Logosub_Frame)
        self.Logosub_Layout = QtWidgets.QHBoxLayout(self.Logosub_Frame)
        self.Logosub_Layout.setAlignment(Qt.AlignCenter)

        # Setting up the logo
        logo = QtWidgets.QLabel('', self)
        pixmap = QPixmap(":Pictures/logo.png")
        pixmap = pixmap.scaled(260, 260)
        logo.setPixmap(pixmap)
        self.Logosub_Layout.addWidget(logo)
        logo.setAlignment(Qt.AlignCenter)

        # The Button sub frame
        self.Buttonsub_Frame = QtWidgets.QFrame(self.main_frame)
        self.main_layout.addWidget(self.Buttonsub_Frame)
        self.Buttonsub_Layout = QtWidgets.QHBoxLayout(self.Buttonsub_Frame)
        self.Buttonsub_Frame.setFixedWidth(self.width)
        self.Buttonsub_Layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        # start to create style button
        StartCreateNewBtn = QtWidgets.QPushButton("Style your image", self)
        StartCreateNewBtn.setObjectName("MainGuiButtons")
        StartCreateNewBtn.clicked.connect(self.openTransferImageGui)
        self.Buttonsub_Layout.addWidget(StartCreateNewBtn)

        # Footer layout
        creditsLbl = QtWidgets.QLabel('Created By Koral Zakai & May Steinfeld, '
                                      'Supervisor: Zeev Vladimir Volkovich, '
                                      '03/06/2019')
        creditsLbl.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(creditsLbl)

        # show the window
        self.showMaximized()

    def openTransferImageGui(self):
        transferImage = Transfer_Image_Gui(self)
        transferImage.show()
        self.main_frame.setVisible(False)

        #opens output image window + save button
    def openShowOutputGui(self):
        outputImageGui = Gui_output_image_window(self)
        outputImageGui.show()
        self.main_frame.setVisible(False)

    # Opens help window
    def showHelp(self):
        #pass
        import os
        filename = 'Help.pdf'
        try:
            os.startfile(filename)
        except:
            return
        # helpWindow = Help_Window(':Pictures/helpmain2.png')

    """onCountChanged function control on updating the progrssBar."""
    def onCountChanged(self, value):
        self.progressBar.setValue(value)

    """Generate function is start when the Generate button pushed. it start the main algorithm."""
    def Generate(self):
        global outputImage
        global exitflag
        exitflag=1
        global flag1
        global flag2
        if (flag1 == 0 or flag2 == 0):
            self.warninglabel.show()
            return
        self.actionHome.setEnabled(False)
        self.actionCreate_New.setEnabled(False)
        self.actionAbout.setEnabled(False)
        self.outputframe.setPixmap(QtGui.QPixmap(":Pictures/help.png"))
        self.savebutton.hide()
        self.progressBar.setValue(0)
        self.progressBar.show()
        # iter control the number of iteration the algorithm run, the user choose it.
        global iter
        iter=0
        if self.comboBox.currentText() == 'Low':
            iter=100
        elif self.comboBox.currentText() == 'Medium':
            iter=500
        else:
            iter=1000

        # resulotion control the output image resulotion, the user choose it.
        resolution = 0
        if self.resbox.currentText() == '256 Px':
            resolution = 256
        elif self.resbox.currentText() == '512 Px':
            resolution = 512
        elif self.resbox.currentText() == '1024 Px':
            resolution = 1024
        else:
            resolution = 2048

        global flag3
        flag3 = 1
        self.actionHome.setEnabled(True)
        self.actionCreate_New.setEnabled(True)
        self.actionAbout.setEnabled(True)

    """lunch_thread control the start of the second thread that running the MainFunc."""
    def lunch_thread(self):
        t = threading.Thread(target=self.Generate)
        t.start()

    """exit function control on exit the application."""
    def exit(self):
        if(exitflag == 1):
            self.exit()
        else:
            exit(1)

    """MainFunc is the main function that running the main algorithm"""
    def MainFunc(self, content_path, style_path, iter, resolution):
        import numpy as np
        from PIL import Image
        import tensorflow as tf
        import tensorflow.contrib.eager as tfe
        from tensorflow.python.keras.preprocessing import image as kp_image
        from tensorflow.python.keras import models

        # Eager execution is a flexible machine learning platform for research and experimentation.
        # Since we're using eager our model is callable just like any other function.
        tf.enable_eager_execution()
        print("Eager execution: {}".format(tf.executing_eagerly()))

        # define calc to the external thread.
        self.calc = External()
        self.calc.countChanged.connect(self.progressBar.setValue)

        # Content layer for the feature maps
        content_layers = ['block5_conv2']

        # Style layer for the feature maps.
        style_layers = ['block1_conv1',
                        'block2_conv1',
                        'block3_conv1',
                        'block4_conv1',
                        'block5_conv1'
                        ]

        num_content_layers = len(content_layers)
        num_style_layers = len(style_layers)

        # load_img function get the path of the image,
        # resize it and broadcast the image array such that it has a batch dimension.
        def load_img(path_to_img):
            max_dim = resolution
            img = Image.open(path_to_img)
            long = max(img.size)
            scale = max_dim / long
            img = img.resize((round(img.size[0] * scale), round(img.size[1] * scale)), Image.ANTIALIAS)
            img = kp_image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            return img

        # load_and_process_img is charge on load the image into the vgg16 network.
        def load_and_process_img(path_to_img):
            img = load_img(path_to_img)
            img = tf.keras.applications.vgg16.preprocess_input(img)
            return img

        def deprocess_img(processed_img):
            x = processed_img.copy()
            if len(x.shape) == 4:
                x = np.squeeze(x, 0)
            assert len(x.shape) == 3, ("Input to deprocess image must be an image of "
                                       "dimension [1, height, width, channel] or [height, width, channel]")
            if len(x.shape) != 3:
                raise ValueError("Invalid input to deprocessing image")

            x[:, :, 0] += 103.939
            x[:, :, 1] += 116.779
            x[:, :, 2] += 123.68
            x = x[:, :, ::-1]

            x = np.clip(x, 0, 255).astype('uint8')
            return x

        # get_model function load the VGG16 model and access the intermediate layers.
        # Returns: a Keras model that takes image inputs and outputs the style and content intermediate layers.
        def get_model():
            import ssl
            ssl._create_default_https_context = ssl._create_unverified_context
            # We load pretrained VGG Network, trained on imagenet data
            vgg = tf.keras.applications.vgg16.VGG16(include_top=False, weights='imagenet')
            vgg.trainable = False
            # Get output layers corresponding to style and content layers
            style_outputs = [vgg.get_layer(name).output for name in style_layers]
            content_outputs = [vgg.get_layer(name).output for name in content_layers]
            model_outputs = style_outputs + content_outputs
            # Build model
            return models.Model(vgg.input, model_outputs)

        # get_content_loss function calculate the content loss that is the
        # Mean Squared Error between the two feature representations matrices.
        def get_content_loss(base_content, target):
            return tf.reduce_mean(tf.square(base_content - target))

        # Calculate the gram matrix for the style representation.
        def gram_matrix(input_tensor):
            # Make the image channels
            channels = int(input_tensor.shape[-1])
            a = tf.reshape(input_tensor, [-1, channels])
            n = tf.shape(a)[0]
            gram = tf.matmul(a, a, transpose_a=True)
            return gram / tf.cast(n, tf.float32)

        # get the style loss by calculate the Mean Squared Error between the two gram matrices.
        # We scale the loss at a given layer by the size of the feature map and the number of filters
        def get_style_loss(base_style, gram_target):
            height, width, channels = base_style.get_shape().as_list()
            gram_style = gram_matrix(base_style)
            return tf.reduce_mean(tf.square(gram_style - gram_target))

        """This function will simply load and preprocess both the content and style
            images from their path. Then it will feed them through the network to obtain
            the outputs of the intermediate layers.
            Returns the style and the content features representation."""
        def get_feature_representations(model, content_path, style_path):
            # Load our images into the VGG16 Network
            content_image = load_and_process_img(content_path)
            style_image = load_and_process_img(style_path)

            # compute content and style features
            style_outputs = model(style_image)
            content_outputs = model(content_image)

            # Get the style and content feature representations from our model
            style_features = [style_layer[0] for style_layer in style_outputs[:num_style_layers]]
            content_features = [content_layer[0] for content_layer in content_outputs[num_style_layers:]]
            return style_features, content_features

        """This function compute the content, style and total loss.
            we use model that will give us access to the intermediate layers."""
        def compute_loss(model, loss_weights, init_image, gram_style_features, content_features):
            style_weight, content_weight = loss_weights

            # Feed our init image through our model. This will give us the content and
            # style representations at our desired layers.
            model_outputs = model(init_image)

            style_output_features = model_outputs[:num_style_layers]
            content_output_features = model_outputs[num_style_layers:]

            style_score = 0
            content_score = 0

            # calculate the style losses from all layers
            # equally weight each contribution of each loss layer
            weight_per_style_layer = 1.0 / float(num_style_layers)
            for target_style, comb_style in zip(gram_style_features, style_output_features):
                style_score += weight_per_style_layer * get_style_loss(comb_style[0], target_style)

            # calculate content losses from all layers
            weight_per_content_layer = 1.0 / float(num_content_layers)
            for target_content, comb_content in zip(content_features, content_output_features):
                content_score += weight_per_content_layer * get_content_loss(comb_content[0], target_content)

            style_score *= style_weight
            content_score *= content_weight

            # Get total loss
            loss = style_score + content_score
            return loss, style_score, content_score

        # Compute gradients according to input image
        def compute_grads(cfg):
            with tf.GradientTape() as tape:
                all_loss = compute_loss(**cfg)
            total_loss = all_loss[0]
            return tape.gradient(total_loss, cfg['init_image']), all_loss

        """The main method of the code, running the main loop for generating the image."""
        def run_style_transfer(content_path,
                               style_path,
                               num_iterations=1000,
                               content_weight=1e3,
                               style_weight=1e-2):
            # We don't train any layers of our model, so we set their trainable to false.
            model = get_model()
            for layer in model.layers:
                layer.trainable = False

            # Get the style and content feature representations (from our specified intermediate layers)
            style_features, content_features = get_feature_representations(model, content_path, style_path)
            gram_style_features = [gram_matrix(style_feature) for style_feature in style_features]

            # Set initial image
            init_image = load_and_process_img(content_path)
            init_image = tfe.Variable(init_image, dtype=tf.float32)
            # We  use Adam Optimizer
            opt = tf.train.AdamOptimizer(learning_rate=5, beta1=0.99, epsilon=1e-1)

            # Store our best result
            best_loss, best_img = float('inf'), None

            # Create config
            loss_weights = (style_weight, content_weight)
            cfg = {
                'model': model,
                'loss_weights': loss_weights,
                'init_image': init_image,
                'gram_style_features': gram_style_features,
                'content_features': content_features
            }

            norm_means = np.array([103.939, 116.779, 123.68])
            min_vals = -norm_means
            max_vals = 255 - norm_means

            # Main loop
            for i in range(num_iterations):
                global count
                count=i
                self.calc.start()
                print(i)
                grads, all_loss = compute_grads(cfg)
                loss, style_score, content_score = all_loss
                opt.apply_gradients([(grads, init_image)])
                clipped = tf.clip_by_value(init_image, min_vals, max_vals)
                init_image.assign(clipped)

                if loss < best_loss:
                    # Update best loss and best image from total loss.
                    best_loss = loss
                    best_img = deprocess_img(init_image.numpy())

            return best_img, best_loss

        best, best_loss = run_style_transfer(content_path, style_path, num_iterations=iter)
        im = Image.fromarray(best)
        return im

"""External class control the thread running the ProgressBar."""
class External(QThread):
    countChanged = pyqtSignal(int)

    def run(self):
        global count
        global iter
        ii =((count + 1) / iter) * 100
        self.countChanged.emit(ii)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main = Main_Window()
    sys.exit(app.exec_())