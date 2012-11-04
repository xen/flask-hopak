from flask import Flask, url_for, redirect, render_template, request
from flask.ext import gear
from formgear import models
from formgear import fields

class Page(models.Model):
    title = fields.StringField(title="Page Title", length=80, required=True)
    body = fields.TextField()
