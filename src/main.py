#
#  Import LIBRARIES
import sqlite3

import flet as ft
from flet import FontWeight

#  Import FILES
#  ______________________
#


database: str = "./src/database/dados.db"


def iniciar_banco() -> None:
    # The connection context manager automatically commits if successful
    # and rolls back if an error occurs.
    with sqlite3.connect(database=database) as conn:
        cur: sqlite3.Cursor = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS contatos (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                nome TEXT, 
                telefone TEXT
            )
        """)
    # Connection is automatically closed when exiting the 'with' block (in most implementations) or at least safely managed.


def ler_do_banco() -> list[tuple[int, str, str]]:
    with sqlite3.connect(database=database) as conn:
        cur: sqlite3.Cursor = conn.cursor()
        cur.execute("SELECT * FROM contatos")
        resultado: list[tuple[int, str, str]] = cur.fetchall()
        print(resultado)
        return resultado


def salvar_no_banco(nome: str, telefone: str) -> None:
    with sqlite3.connect(database=database) as conn:
        cur: sqlite3.Cursor = conn.cursor()
        cur.execute("INSERT INTO contatos (nome, telefone) VALUES (?,?)", (nome, telefone))


def deletar_do_banco(id_contato: int) -> None:
    with sqlite3.connect(database=database) as conn:
        cur: sqlite3.Cursor = conn.cursor()
        cur.execute("DELETE FROM contatos WHERE id=?", (id_contato,))


# salvar_no_banco(nome="Emma", telefone="+55 0672 88 1881")
# salvar_no_banco(nome="Erre", telefone="+39 339 12 18 135")
# salvar_no_banco(nome="Effe", telefone="+123456789")


def main(page: ft.Page) -> None:
    page.title = "Minha Agenda SQLite"
    page.width = 400
    page.height = 600

    iniciar_banco()

    nome_input = ft.TextField(label="Nome", hint_text="Digite o nome")
    telefone_input = ft.TextField(label="Telefone", hint_text="Digiteo número")

    lista_contatos = ft.Column()

    def carregar_dados() -> None:
        lista_contatos.controls.clear()
        dados: list[tuple[int, str, str]] = ler_do_banco()

        for contato in dados:
            id_db: int = contato[0]
            nome_db: str = contato[1]
            tel_db: str = contato[2]

            linha: tuple[ft.Row] = (
                ft.Row(
                    controls=[
                        ft.Text(value=f"{nome_db} In{tel_db}", size=16, expand=True),
                        ft.IconButton(
                            icon=ft.Icons.DELETE, icon_color="red", data=id_db, on_click=deletar_contato
                        ),  # O data=id_db guarda o ID do banco no botão
                    ]
                ),
            )
            lista_contatos.controls.append(linha)

        page.update()

    def adicionar_contato(e: ft.ControlEvent) -> None:
        # Use the page object from the event to ensure it's always in scope
        page: ft.Page | ft.BasePage = e.page
        if nome_input.value:
            salvar_no_banco(nome=nome_input.value, telefone=telefone_input.value)
            nome_input.value = ""
            telefone_input.value = ""
            carregar_dados()
        else:
            # Create the snackbar
            snack_bar = ft.SnackBar(content=ft.Text(value="Nome é Obrigatório"))
            # Use the overlay collection and toggle the 'open' property
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
            # snack_bar = ft.SnackBar(content=ft.Text(value="Nome é Obrigatório"))
            # page.open(snack_bar)
            # page.update()

    btn_salvar = ft.Button(content="Salvar Contato", on_click=adicionar_contato)

    def deletar_contato(e) -> None:
        id_para_deletar = e.control.data
        deletar_do_banco(id_para_deletar)
        carregar_dados()

    page.add(
        ft.Text(value="Agenda Simples", size=24, weight=FontWeight.BOLD),
        nome_input,
        telefone_input,
        btn_salvar,
        ft.Divider(),
        ft.Text(value="Menus Contatos", size=20),  # weight=FontWeight.BOLD),
        lista_contatos,
    )
    carregar_dados()

    # salvar_no_banco(nome="Emma", telefone="+55 0672 88 1881")
    # ler_do_banco()


ft.run(main=main)  # type: ignore


#
#  Import LIBRARIES
#  Import FILES
#  ______________________
#


# def iniciar_banco():
#     conn = sqlite3.connect("dados.db")
#     cur = conn.cursor()
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS contatos ( id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, telefone TEXT
#     """)
#     conn.commit()
#     conn.close()
