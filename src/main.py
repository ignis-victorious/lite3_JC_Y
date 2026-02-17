#
#  Import LIBRARIES
import sqlite3

import flet as ft

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


def ler_do_banco() -> list[int | str]:
    with sqlite3.connect(database=database) as conn:
        cur: sqlite3.Cursor = conn.cursor()
        cur.execute("SELECT * FROM contatos")
        resultado: list[int | str] = cur.fetchall()
        print(resultado)
        return resultado


def salvar_no_banco(nome: str, telefone: str) -> None:
    with sqlite3.connect(database=database) as conn:
        cur: sqlite3.Cursor = conn.cursor()
        cur.execute("INSERT INTO contatos (nome, telefone) VALUES (?,?)", (nome, telefone))


def deletar_no_banco(id_contato: int) -> None:
    with sqlite3.connect(database=database) as conn:
        cur: sqlite3.Cursor = conn.cursor()
        cur.execute("DELETE FROM contatos WHERE id=?", (id_contato,))


def main(page: ft.Page) -> None:
    page.title = "Minha Agenda SQLite"
    page.width = 400
    page.height = 600

    # iniciar_banco()
    salvar_no_banco(nome="Emma", telefone="+55 0672 88 1881")
    ler_do_banco()


#     counter = ft.Text("0", size=50, data=0)

#     def increment_click(e):
#         counter.data += 1
#         counter.value = str(counter.data)

#     page.floating_action_button = ft.FloatingActionButton(
#         icon=ft.Icons.ADD, on_click=increment_click
#     )
#     page.add(
#         ft.SafeArea(
#             expand=True,
#             content=ft.Container(
#                 content=counter,
#                 alignment=ft.Alignment.CENTER,
#             ),
#         )
#     )


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
