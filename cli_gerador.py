import psycopg2
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
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
print("\n=== LAVINES ENCURTADOR [Modo Termux com NeonDB] ===")
url = input("Digite a URL real: ").strip()
alias = input("Digite o alias desejado (ex: meulink): ").strip()

if alias_existe(alias):
    print(f"\n[!] O alias '{alias}' já está em uso.")
    sugestões = sugestoes_alias(alias)
    if sugestões:
        print("Sugestões disponíveis:")
        for s in sugestões:
            print(f" - {s}")
    else:
        print("Nenhuma sugestão disponível no momento.")
else:
    inserir_link(alias, url)
    print(f"\n[✓] Link encurtado com sucesso!")
    print(f"→ https://enc-m8i4.onrender.com/{alias}")
