from flask import Blueprint, redirect
from .database import buscar_url

main = Blueprint('main', __name__)

@main.route('/<alias>')
def redirecionar(alias):
    url = buscar_url(alias)
    if url:
        return redirect(url)
    else:
        return "Alias não encontrado", 404

@main.route('/')
def home():
    return "Servidor Lavines Encurtador Ativo!"
