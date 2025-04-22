import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'urls.db')

def alias_existe(alias):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM links WHERE alias=?", (alias,))
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
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO links (alias, url_real) VALUES (?, ?)", (alias, url))
    conn.commit()
    conn.close()

# Interface CLI
print("\n=== LAVINES ENCURTADOR [Modo Termux] ===")
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
    print(f"→ http://localhost:5000/{alias}")
