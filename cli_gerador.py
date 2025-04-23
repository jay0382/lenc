import psycopg2
import os
from dotenv import load_dotenv

# Cores ANSI para terminal
VERDE = "\033[1;32m"
VERMELHO = "\033[1;31m"
AZUL = "\033[1;34m"
AMARELO = "\033[1;33m"
RESET = "\033[0m"
NEGRITO = "\033[1m"

# Banner
banner = f"""
{AZUL}{NEGRITO}
╔════════════════════════════════════════════════════╗
║            LAVINES ENCURTADOR [NeonDB]            ║
╠════════════════════════════════════════════════════╣
║        Crie links curtos e personalizados!         ║
╚════════════════════════════════════════════════════╝
{RESET}
"""

# Carrega .env
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

def conectar():
    return psycopg2.connect(DB_URL)

def alias_existe(alias):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM links WHERE alias=%s", (alias,))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe

def sugestoes_alias(alias_base):
    padrões = [
        alias_base + "1",
        alias_base + "123",
        alias_base + "_oficial",
        alias_base + "_br",
        alias_base + "_link"
    ]
    sugestões = []
    for sugestão in padrões:
        if not alias_existe(sugestão):
            sugestões.append(sugestão)
    return sugestões[:3]

def inserir_link(alias, url):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO links (alias, url_real) VALUES (%s, %s)", (alias, url))
    conn.commit()
    conn.close()

# Interface CLI
print(banner)
url = input(f"{AZUL}Digite a URL real: {RESET}").strip()
alias = input(f"{AZUL}Digite o alias desejado (ex: meulink): {RESET}").strip()

if alias_existe(alias):
    print(f"\n{VERMELHO}[!] O alias '{alias}' já está em uso.{RESET}")
    sugestões = sugestoes_alias(alias)
    if sugestões:
        print(f"{AMARELO}Sugestões disponíveis:{RESET}")
        for s in sugestões:
            print(f" - {VERDE}{s}{RESET}")
    else:
        print(f"{VERMELHO}Nenhuma sugestão disponível no momento.{RESET}")
else:
    inserir_link(alias, url)
    print(f"\n{VERDE}[✓] Link encurtado com sucesso!{RESET}")
    print(f"{AZUL}→ https://enc-m8i4.onrender.com/{alias}{RESET}")
