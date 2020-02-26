from Classes.Board import *
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

board = Board(config)
