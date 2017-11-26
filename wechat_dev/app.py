""" app.py

应用入口文件
"""

from flask import Flask, make_response, render_template, request
from news.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
