import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app
from musica_api.database import get_session
from musica_api.models import Cancion, Usuario


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    c = TestClient(app)
    yield c
    app.dependency_overrides.clear()


@pytest.fixture(name="usuario_test")
def usuario_test_fixture(session: Session):
    u = Usuario(nombre="Lina Chamorro", correo="lina@test.com")
    session.add(u)
    session.commit()
    session.refresh(u)
    return u


@pytest.fixture(name="cancion_test")
def cancion_test_fixture(session: Session):
    c = Cancion(
        titulo="Canción Test",
        artista="Artista Test",
        album="Álbum Test",
        duracion=210,
        año=2020,
        genero="Pop",
    )
    session.add(c)
    session.commit()
    session.refresh(c)
    return c


@pytest.fixture(name="musica_test")
def musica_test_fixture(cancion_test):
    return cancion_test


class TestUsuarios:
    def test_listar_usuarios(self, client: TestClient):
        assert client.get("/api/usuarios/").status_code == 200

    def test_crear_usuario(self, client: TestClient):
        assert client.post("/api/usuarios/", json={"nombre": "Ana", "correo": "ana@test.com"}).status_code == 201

    def test_crear_usuario_correo_duplicado(self, client: TestClient, usuario_test: Usuario):
        assert client.post("/api/usuarios/", json={"nombre": "Otro", "correo": "lina@test.com"}).status_code == 400

    def test_obtener_usuario(self, client: TestClient, usuario_test: Usuario):
        assert client.get(f"/api/usuarios/{usuario_test.id}").status_code == 200

    def test_obtener_usuario_no_existe(self, client: TestClient):
        assert client.get("/api/usuarios/9999").status_code == 404

    def test_actualizar_usuario(self, client: TestClient, usuario_test: Usuario):
        assert client.put(f"/api/usuarios/{usuario_test.id}", json={"nombre": "Lina Actualizada"}).status_code == 200

    def test_eliminar_usuario(self, client: TestClient, usuario_test: Usuario):
        assert client.delete(f"/api/usuarios/{usuario_test.id}").status_code == 200


class TestCancions:
    def test_listar_cancions(self, client: TestClient):
        assert client.get("/api/canciones/").status_code == 200

    def test_crear_cancion(self, client: TestClient):
        assert (
            client.post(
                "/api/canciones/",
                json={
                    "titulo": "X",
                    "artista": "Y",
                    "duracion": 180,
                    "año": 2021,
                    "genero": "Rock",
                },
            ).status_code
            == 201
        )

    def test_obtener_cancion(self, client: TestClient, cancion_test: Cancion):
        assert client.get(f"/api/canciones/{cancion_test.id}").status_code == 200

    def test_actualizar_cancion(self, client: TestClient, cancion_test: Cancion):
        assert client.put(f"/api/canciones/{cancion_test.id}", json={"titulo": "Nueva"}).status_code == 200

    def test_eliminar_cancion(self, client: TestClient, cancion_test: Cancion):
        assert client.delete(f"/api/canciones/{cancion_test.id}").status_code == 200

    def test_buscar_cancions(self, client: TestClient, cancion_test: Cancion):
        assert client.get("/api/canciones/buscar?titulo=Canción").status_code == 200

    def test_buscar_cancions_multiples_filtros(self, client: TestClient):
        assert client.get("/api/canciones/buscar?artista=Artista&genero=Pop").status_code == 200


class TestFavoritos:
    def test_listar_favoritos(self, client: TestClient):
        assert client.get("/api/favoritos/").status_code == 200

    def test_crear_favorito(self, client: TestClient, usuario_test: Usuario, cancion_test: Cancion):
        assert (
            client.post(
                "/api/favoritos/",
                json={"id_usuario": usuario_test.id, "id_cancion": cancion_test.id},
            ).status_code
            == 201
        )

    def test_crear_favorito_duplicado(self, client: TestClient, usuario_test: Usuario, cancion_test: Cancion):
        client.post(
            "/api/favoritos/",
            json={"id_usuario": usuario_test.id, "id_cancion": cancion_test.id},
        )
        assert (
            client.post(
                "/api/favoritos/",
                json={"id_usuario": usuario_test.id, "id_cancion": cancion_test.id},
            ).status_code
            == 400
        )

    def test_eliminar_favorito(
        self,
        client: TestClient,
        session: Session,
        usuario_test: Usuario,
        cancion_test: Cancion,
    ):
        r = client.post(
            "/api/favoritos/",
            json={"id_usuario": usuario_test.id, "id_cancion": cancion_test.id},
        )
        assert client.delete(f"/api/favoritos/{r.json()['id']}").status_code == 200

    def test_marcar_favorito_usuario(self, client: TestClient, usuario_test: Usuario, cancion_test: Cancion):
        assert client.post(f"/api/usuarios/{usuario_test.id}/favoritos/{cancion_test.id}").status_code == 201

    def test_listar_favoritos_usuario(
        self,
        client: TestClient,
        session: Session,
        usuario_test: Usuario,
        cancion_test: Cancion,
    ):
        client.post(
            "/api/favoritos/",
            json={"id_usuario": usuario_test.id, "id_cancion": cancion_test.id},
        )
        assert client.get(f"/api/usuarios/{usuario_test.id}/favoritos").status_code == 200


class TestIntegracion:
    def test_flujo_completo(self, client: TestClient):
        u = client.post("/api/usuarios/", json={"nombre": "Test", "correo": "flujo@test.com"}).json()
        c = client.post(
            "/api/canciones/",
            json={
                "titulo": "Flow",
                "artista": "A",
                "duracion": 200,
                "año": 2020,
                "genero": "Pop",
            },
        ).json()
        assert client.post("/api/favoritos/", json={"id_usuario": u["id"], "id_cancion": c["id"]}).status_code == 201
        assert len(client.get(f"/api/usuarios/{u['id']}/favoritos").json()) == 1


class TestValidacion:
    def test_email_invalido(self, client: TestClient):
        assert client.post("/api/usuarios/", json={"nombre": "Ana", "correo": "no-es-correo"}).status_code == 422

    def test_año_cancion_invalido(self, client: TestClient):
        assert (
            client.post(
                "/api/canciones/",
                json={
                    "titulo": "X",
                    "artista": "Y",
                    "duracion": 180,
                    "año": 1800,
                    "genero": "Rock",
                },
            ).status_code
            == 422
        )

    def test_campos_requeridos(self, client: TestClient):
        assert client.post("/api/usuarios/", json={}).status_code == 422
