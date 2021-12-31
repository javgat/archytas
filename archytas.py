#!/usr/bin/env python3
import sys
from PySide2 import QtCore, QtWidgets, QtGui
from os.path import exists, join, abspath
from os import remove
import tweepy
from auth.auth import AuthData
from tweet.tweet import getTweetsKeyword, tweetRandom, OutputerInterface
import types

class AuthDataInput(QtWidgets.QWidget):
    def __init__(self, wrapper: 'AuthDataWidget', authdata_path: str):
        super().__init__()

        self.authdata_path = authdata_path
        self.wrapper = wrapper

        self.layout_consumer_key = QtWidgets.QHBoxLayout()
        self.label_consumer_key = QtWidgets.QLabel("Consumer Key", alignment=QtCore.Qt.AlignCenter)
        self.edit_consumer_key = QtWidgets.QLineEdit()
        self.layout_consumer_key.addWidget(self.label_consumer_key)
        self.layout_consumer_key.addWidget(self.edit_consumer_key)
        
        self.layout_consumer_secret = QtWidgets.QHBoxLayout()
        self.label_consumer_secret = QtWidgets.QLabel("Consumer Secret", alignment=QtCore.Qt.AlignCenter)
        self.edit_consumer_secret = QtWidgets.QLineEdit()
        self.layout_consumer_secret.addWidget(self.label_consumer_secret)
        self.layout_consumer_secret.addWidget(self.edit_consumer_secret)

        self.layout_access_token = QtWidgets.QHBoxLayout()
        self.label_access_token = QtWidgets.QLabel("Access Token", alignment=QtCore.Qt.AlignCenter)
        self.edit_access_token = QtWidgets.QLineEdit()
        self.layout_access_token.addWidget(self.label_access_token)
        self.layout_access_token.addWidget(self.edit_access_token)

        self.layout_access_token_secret = QtWidgets.QHBoxLayout()
        self.label_access_token_secret = QtWidgets.QLabel("Access Token Secret", alignment=QtCore.Qt.AlignCenter)
        self.edit_access_token_secret = QtWidgets.QLineEdit()
        self.layout_access_token_secret.addWidget(self.label_access_token_secret)
        self.layout_access_token_secret.addWidget(self.edit_access_token_secret)

        self.button_save = QtWidgets.QPushButton("Save")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addLayout(self.layout_consumer_key)
        self.layout.addLayout(self.layout_consumer_secret)
        self.layout.addLayout(self.layout_access_token)
        self.layout.addLayout(self.layout_access_token_secret)
        self.layout.addWidget(self.button_save)

        self.button_save.clicked.connect(self.save)

    @QtCore.Slot()
    def save(self):
        # Save in self.authdata_path
        consumer_key = self.edit_consumer_key.text()
        consumer_secret = self.edit_consumer_secret.text()
        access_token = self.edit_access_token.text()
        access_token_secret = self.edit_access_token_secret.text()
        ad = AuthData(consumer_key, consumer_secret, access_token, access_token_secret)
        ad.SaveToJson(self.authdata_path)
        # Notify parent wrapper
        self.wrapper.update_storage_status()

class AuthDataStored(QtWidgets.QWidget):
    def __init__(self, wrapper: 'AuthDataWidget', authdata_path: str):
        super().__init__()

        self.wrapper = wrapper
        self.authdata_path = authdata_path

        # Read auth data
        self.ad = AuthData.CreateFromJson(authdata_path)

        self.layout_consumer_key = QtWidgets.QHBoxLayout()
        self.label_consumer_key = QtWidgets.QLabel("Consumer Key", alignment=QtCore.Qt.AlignLeft)
        self.label_literal_consumer_key = QtWidgets.QLabel(self.ad.consumer_key, alignment=QtCore.Qt.AlignRight)
        self.layout_consumer_key.addWidget(self.label_consumer_key)
        self.layout_consumer_key.addWidget(self.label_literal_consumer_key)

        self.layout_consumer_secret = QtWidgets.QHBoxLayout()
        self.label_consumer_secret = QtWidgets.QLabel("Consumer Secret", alignment=QtCore.Qt.AlignLeft)
        self.label_literal_consumer_secret = QtWidgets.QLabel(self.ad.consumer_secret, alignment=QtCore.Qt.AlignRight)
        self.layout_consumer_secret.addWidget(self.label_consumer_secret)
        self.layout_consumer_secret.addWidget(self.label_literal_consumer_secret)

        self.layout_access_token = QtWidgets.QHBoxLayout()
        self.label_access_token = QtWidgets.QLabel("Access Token", alignment=QtCore.Qt.AlignLeft)
        self.label_literal_access_token = QtWidgets.QLabel(self.ad.access_token, alignment=QtCore.Qt.AlignRight)
        self.layout_access_token.addWidget(self.label_access_token)
        self.layout_access_token.addWidget(self.label_literal_access_token)

        self.layout_access_token_secret = QtWidgets.QHBoxLayout()
        self.label_access_token_secret = QtWidgets.QLabel("Access Token Secret", alignment=QtCore.Qt.AlignLeft)
        self.label_literal_access_token_secret = QtWidgets.QLabel(self.ad.access_token_secret, alignment=QtCore.Qt.AlignRight)
        self.layout_access_token_secret.addWidget(self.label_access_token_secret)
        self.layout_access_token_secret.addWidget(self.label_literal_access_token_secret)

        self.text = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)

        self.layout_buttons = QtWidgets.QHBoxLayout()
        self.button_connect = QtWidgets.QPushButton("Connect")
        self.button_edit = QtWidgets.QPushButton("Edit")
        self.button_delete = QtWidgets.QPushButton("Delete")
        self.layout_buttons.addWidget(self.button_connect)
        self.layout_buttons.addWidget(self.button_edit)
        self.layout_buttons.addWidget(self.button_delete)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addLayout(self.layout_consumer_key)
        self.layout.addLayout(self.layout_consumer_secret)
        self.layout.addLayout(self.layout_access_token)
        self.layout.addLayout(self.layout_access_token_secret)
        self.layout.addLayout(self.layout_buttons)
        self.button_connect.clicked.connect(self.authenticate)
        self.button_delete.clicked.connect(self.delete_auth)

    @QtCore.Slot()
    def authenticate(self):
        # Authenticate to Twitter
        auth = tweepy.OAuthHandler(self.ad.consumer_key, self.ad.consumer_secret)
        auth.set_access_token(self.ad.access_token, self.ad.access_token_secret)
        api = tweepy.API(auth)
        auth_success = False
        try:
            api.verify_credentials()
            result_text = "Authentication OK"
            auth_success = True
        except:
            result_text = "Error during authentication"
        self.text.setText(result_text)
        if (auth_success):
            self.wrapper.update_api(api)
    
    @QtCore.Slot()
    def delete_auth(self):
        # Remove auth file
        if exists(self.authdata_path):
            remove(self.authdata_path)
        # Notify parent wrapper
        self.wrapper.update_storage_status()

class AuthDataWidget(QtWidgets.QWidget):
    def __init__(self, authdata_path, archytas: 'ArchytasWidget'):
        super().__init__()
        self.authdata_path = authdata_path
        self.archytas = archytas

        self.calculate_authdata()

        self.title = QtWidgets.QLabel("Authentication", alignment=QtCore.Qt.AlignCenter)
        self.title.setFont(QtGui.QFont("Default", 16))
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.authdata_inner)

    def calculate_authdata(self):
        self.isAuthDataStored = exists(self.authdata_path)
        ad = AuthData.CreateFromJson(self.authdata_path)
        if (self.isAuthDataStored and ad is not None):
            self.authdata_inner = AuthDataStored(self, self.authdata_path)
        else:
            self.authdata_inner = AuthDataInput(self, self.authdata_path)
    
    def update_storage_status(self):
        aw = self.layout.takeAt(1)
        aw.widget().deleteLater()
        self.calculate_authdata()
        self.layout.addWidget(self.authdata_inner)
    
    def update_api(self, api: tweepy.API):
        self.api = api
        if (self.api is not None):
            self.archytas.update_api(api)

class RetweetWidget(QtWidgets.QWidget):
    def __init__(self, archytas: 'ArchytasWidget'):
        super().__init__()
        self.archytas = archytas

        self.title = QtWidgets.QLabel("Auto retweeter", alignment=QtCore.Qt.AlignCenter)
        self.title.setFont(QtGui.QFont("Default", 16))
        self.label_err_message = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
        self.layout_number_retweets = QtWidgets.QHBoxLayout()
        self.label_number_retweets = QtWidgets.QLabel("Number of retweets", alignment=QtCore.Qt.AlignLeft)
        self.edit_number_retweets = QtWidgets.QLineEdit()
        self.layout_number_retweets.addWidget(self.label_number_retweets)
        self.layout_number_retweets.addWidget(self.edit_number_retweets)

        self.layout_keyword = QtWidgets.QHBoxLayout()
        self.label_keyword = QtWidgets.QLabel("Keyword", alignment=QtCore.Qt.AlignLeft)
        self.edit_keyword = QtWidgets.QLineEdit()
        self.layout_keyword.addWidget(self.label_keyword)
        self.layout_keyword.addWidget(self.edit_keyword)

        self.button_retweet = QtWidgets.QPushButton("Retweet")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.label_err_message)
        self.layout.addLayout(self.layout_number_retweets)
        self.layout.addLayout(self.layout_keyword)
        self.layout.addWidget(self.button_retweet)

        self.button_retweet.clicked.connect(self.retweet)

        self.set_connected(False)        

    def QtRetweetList(self, api: tweepy.API, tweets: list, index: int, secs: int, finishedAction: types.FunctionType):
        tweet = tweets[index]
        try:
            print('\nRetweet Bot found tweet by @' + tweet.user.screen_name + '. ' + 'Attempting to retweet.')

            tweet.retweet()
            print('Retweet published successfully.')
            index = index + 1
            if (index < len(tweets)):
                QtCore.QTimer.singleShot(secs * 1000, lambda: self.QtRetweetList(api, tweets, index, secs, finishedAction))
            else:
                finishedAction()
        # Some basic error handling. Will print out why retweet failed, into your terminal.
        except tweepy.TweepyException as error:
            print('\nError TweepyException. Retweet not successful. Reason: ')
            print(error)

        except tweepy.HTTPException as error:
            print('\nError HTTPException. Retweet not successful. Reason: ')
            print(error)

    def QtRetweetKeyword(self, api, keyword, rewteetRange, secs, finishedAction: types.FunctionType):
        tweets = getTweetsKeyword(api, keyword, rewteetRange)
        self.QtRetweetList(api, tweets, 0, secs, finishedAction)

    @QtCore.Slot()
    def retweet(self):
        self.label_err_message.setText("")
        if (not self.archytas.connected):
            self.label_err_message.setText("Error: The app is not connected to Twitter")
            return
        api = self.archytas.api
        # Retweet some tweets with the hashtag
        try:
            retweetRange = int(self.edit_number_retweets.text())
        except:
            self.label_err_message.setText("Error: Number of retweets is not a number")
            return
        keyword = self.edit_keyword.text()
        self.button_retweet.setEnabled(False)
        self.label_err_message.setText("Retweeting...")
        finishedAction = self.finishedRetweetingActions
        seconds_between_retweets = 2
        self.QtRetweetKeyword(api, keyword, retweetRange, seconds_between_retweets, finishedAction)
    
    def finishedRetweetingActions(self):
        self.button_retweet.setEnabled(True)
        self.label_err_message.setText("Successfully retweeted")

    def set_connected(self, connected: bool):
        self.button_retweet.setEnabled(connected)

class OutputerTweetWidget(OutputerInterface):
    def __init__(self, TweetWidget):
        super().__init__()
        self.tweetw = TweetWidget

    def print(self, message: str) -> None:
        self.tweetw.update_message(message)

class TweetWidget(QtWidgets.QWidget):
    def __init__(self, archytas: 'ArchytasWidget'):
        super().__init__()
        self.archytas = archytas
        self.csv_path = "<No file loaded>"
        self.loaded_csv = False
        self.connected = False

        self.title = QtWidgets.QLabel("Random tweet", alignment=QtCore.Qt.AlignCenter)
        self.title.setFont(QtGui.QFont("Default", 16))
        self.label_err_message = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)

        self.layout_input_csv = QtWidgets.QHBoxLayout()
        self.label_input_csv = QtWidgets.QLabel("Random tweet source:", alignment=QtCore.Qt.AlignLeft)
        self.label_location_csv = QtWidgets.QLabel(self.csv_path, alignment=QtCore.Qt.AlignLeft)
        self.button_load_csv = QtWidgets.QPushButton("Browse...")
        self.layout_input_csv.addWidget(self.label_input_csv)
        self.layout_input_csv.addWidget(self.label_location_csv)
        self.layout_input_csv.addWidget(self.button_load_csv)

        self.button_tweet = QtWidgets.QPushButton("Tweet")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.label_err_message)
        self.layout.addLayout(self.layout_input_csv)
        self.layout.addWidget(self.button_tweet)

        self.button_tweet.clicked.connect(self.tweet)
        self.button_load_csv.clicked.connect(self.browse_csv)

        self.try_enabling_tweet_button()

    @QtCore.Slot()
    def tweet(self):
        self.label_err_message.setText("")
        if (not self.archytas.connected):
            self.label_err_message.setText("Error: The app is not connected to Twitter")
            return
        if (not self.loaded_csv):
            self.label_err_message.setText("Error: Invalid tweet source file path")
            return
        api = self.archytas.api
        # Tweet randomly selected tweets
        number_of_tweets = 1
        outputer = OutputerTweetWidget(self)
        tweetRandom(api, self.csv_path, number_of_tweets, outputer)

    @QtCore.Slot()
    def browse_csv(self):
        file_input_csv = QtWidgets.QFileDialog()
        path_tuple: tuple = file_input_csv.getOpenFileName()
        path = path_tuple[0]
        self.update_csv_path(path)

    def update_csv_path(self, path):
        self.loaded_csv = True
        self.csv_path = path
        self.label_location_csv.setText(self.csv_path)
        self.try_enabling_tweet_button()

    def try_enabling_tweet_button(self):
        if (self.connected and self.loaded_csv):    
            self.button_tweet.setEnabled(True)
        else:
            self.button_tweet.setEnabled(False)

    def set_connected(self, connected: bool):
        self.connected = connected
        self.try_enabling_tweet_button()
    
    def update_message(self, message: str) -> None:
        self.label_err_message.setText(message)

class ArchytasWidget(QtWidgets.QWidget):
    def __init__(self, authdata_path):
        super().__init__()
        self.connected = False
        self.authdataw = AuthDataWidget(authdata_path, self)
        self.retweetw = RetweetWidget(self)
        self.tweetw = TweetWidget(self)

        self.line1 = QtWidgets.QFrame()
        self.line1.setFrameShape(QtWidgets.QFrame.HLine)
        self.line1.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.line2 = QtWidgets.QFrame()
        self.line2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line2.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.authdataw)
        self.layout.addWidget(self.line1)
        self.layout.addWidget(self.retweetw)
        self.layout.addWidget(self.line2)
        self.layout.addWidget(self.tweetw)
    
    def update_api(self, api: tweepy.API):
        self.api = api
        if (self.api is not None):
            self.connected = True
        else:
            self.connected = False
        self.retweetw.set_connected(self.connected)
        self.tweetw.set_connected(self.connected)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return join(sys._MEIPASS, relative_path)
    return join(abspath('.'), relative_path)

def main():
    app = QtWidgets.QApplication([])

    widget = ArchytasWidget("auth_data.json")
    widget.resize(800, 600)
    widget.show()

    widget.setWindowTitle("Archytas")

    widget.setWindowIcon( QtGui.QIcon(resource_path("./assets/icon.png")) )

    sys.exit(app.exec_())

if __name__=="__main__":
    main()