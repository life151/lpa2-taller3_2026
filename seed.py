from sqlmodel import Session, select

from musica_api.database import engine
from musica_api.models import Cancion, Usuario

usuarios = [
    ("Lina Chamorro", "lina@test.com"),
    ("Ana Gomez", "ana@test.com"),
    ("Carlos Ruiz", "carlos@test.com"),
    ("Sofia Diaz", "sofia@test.com"),
    ("Diego Lopez", "diego@test.com"),
]

# 10 canciones de tus artistas
canciones = [
    # Silvio Rodríguez
    ("Ojalá", "Silvio Rodríguez", "Al Final de Este Viaje", 300, 1978, "Trova"),
    ("Unicornio", "Silvio Rodríguez", "Unicornio", 260, 1982, "Trova"),
    # Mercedes Sosa
    ("Gracias a la Vida", "Mercedes Sosa", "Cantata Sudamericana", 240, 1971, "Folclore"),
    ("Alfonsina y el Mar", "Mercedes Sosa", "Mujeres Argentinas", 300, 1969, "Folclore"),
    ("Todo Cambia", "Mercedes Sosa", "Mercedes Sosa", 280, 1982, "Folclore"),
    # Facundo Cabral
    ("No Soy de Aquí Ni Soy de Allá", "Facundo Cabral", "Facundo Cabral", 240, 1970, "Trova"),
    ("Este Es Un Nuevo Día", "Facundo Cabral", "Facundo Cabral", 210, 1984, "Trova"),
    # Camilo Sesto
    ("Vivir Así Es Morir de Amor", "Camilo Sesto", "Sentimientos", 250, 1978, "Balada"),
    ("Perdóname", "Camilo Sesto", "Amaneciendo", 230, 1980, "Balada"),
    # Vilma Palma e Vampiros
    ("La Pachanga", "Vilma Palma e Vampiros", "La Pachanga", 260, 1991, "Rock"),
]

with Session(engine) as s:
    # Si ya existen, no duplicar
    if s.exec(select(Usuario)).first():
        print("Ya hay datos, borrando para cargar los nuevos...")
        s.exec(select(Cancion)).all()
        for c in s.exec(select(Cancion)).all():
            s.delete(c)
        for u in s.exec(select(Usuario)).all():
            s.delete(u)
        s.commit()

    for n, c in usuarios:
        s.add(Usuario(nombre=n, correo=c))
    for t, a, al, d, an, g in canciones:
        s.add(Cancion(titulo=t, artista=a, album=al, duracion=d, año=an, genero=g))
    s.commit()
print("Listo: 5 usuarios + 10 canciones de Silvio, Mercedes, Facundo, Camilo y Vilma Palma 🎶")
