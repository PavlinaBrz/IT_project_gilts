# Interní systém pro evidenci prasniček

Tento projekt slouží pro **evidenci hmotnosti** a dalších parametrů prasniček na farmě Libichov.  
Umožňuje:
- Registraci a přihlášení uživatelů (admini, zaměstnanci),
- Přidání zvířete (vážení, narození, měření špeku, atd.),
- Zobrazení tabulky všech evidovaných zvířat,
- Vykreslení růstové křivky (graf) z dostupných vážení,
- Editaci existujících záznamů.

## Požadavky
- **Python 3.10+**  
- Knihovny uvedené v [requirements.txt](requirements.txt)  
  (Flask, Flask-WTF, SQLAlchemy, Pandas, atd.)

## Instalace a spuštění
1. Naklonujte repozitář nebo stáhněte ZIP.
2. Vytvořte si a aktivujte virtuální prostředí (např. `python -m venv venv && source venv/bin/activate`).
3. Nainstalujte závislosti:  
   ```bash
   pip install -r requirements.txt
4. Inicializujte a upravte databázi:
    - buď flask db upgrade (při použití Flask-Migrate),
    - Nebo db.create_all() (pokud voláte učně v app.py)
5. Spusťte aplikaci:
    ```bash
   python app.py
nebo:
    ```bash
    flask run
6. Otevřete prohlížeč a jděte na http://127.0.0.1:5000/.

Struktura projektu
- app.py – hlavní soubor, kde je Flask aplikace, routy (index, login, register, atd.).
- database_animal.py – SQLAlchemy model Animals + funkce add_animal, update_animal.
- database_users.py – Model User + funkce pro práci s uživateli.
- forms.py – Formuláře (WTForms) pro registraci, login, přidání/úpravu zvířete.
- templates/ – HTML šablony (Jinja2): index.html, login.html, animals.html, atd.
- static/ – CSS, obrázky, popř. JS.

Používání
1. Registrace: Otevřete /register, zadejte uživatelské jméno a heslo (min. 6 znaků).
2. Přihlášení: Zadejte username, password => při úspěchu jste přesměrováni na /.
3. Přidání zvířete: Otevřete /add_animal, vyplňte formulář (kdy bylo zvíře váženo, hmotnost, …).
4. Seznam zvířat: /animals – stránkovaný výpis. Můžete kliknout na “Editovat” pro úpravu detailů.
5. Graf: /growth_curve – zobrazí průměrné křivky vážení I, II, III.

Testy
- spusťte:
    ```bash
   pytest
Testy používají in-memory databázi (sqlite:///:memory:) a definují základní scénáře (registrace, login, přidání zvířete).

Možné chyby
- "no such table: animals" - musíte nejdříve vytvořit tabulku (migrace nebo db.create_all()).
- "IntegrityError: UNIQUE constraint failed: animals.interni_ID" – duplicita interni_ID.
- "Invalid isoformat string" – v Excelu je datum s časem, ale v DB sloupec je Date. Ořízněte čas nebo změňte sloupec na DateTime.

Licence
Projekt je interní a nepodléhá open-source licenci.
Vytvořila © Pavlína Brzobohatá, 2025.

