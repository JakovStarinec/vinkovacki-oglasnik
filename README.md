# Vinkovački oglasnik

Web aplikacija za male oglase izrađena u Djangu.

## Značajke

- Registracija i prijava korisnika
- Objava, uređivanje i brisanje oglasa (naslov, opis, cijena, lokacija)
- Upload slika uz oglas
- Skrivanje oglasa
- Lajkovi i popis omiljenih oglasa
- Administracija preko Django admin sučelja

## Tehnologije

Python · Django 5.2 · SQLite · Bootstrap 5 · Pillow

## Pokretanje

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Aplikacija je zatim dostupna na `http://127.0.0.1:8000/`.

## Struktura

```
vinkovacki-oglasnik/
├── accounts/              # registracija i prijava
├── ads/                   # oglasi, slike, lajkovi, favoriti
├── vinkovacki_oglasnik/   # postavke projekta
└── manage.py
```
