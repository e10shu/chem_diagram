import base64
from datetime import datetime
from typing import List

import flet as ft

from diagram import Group, Diagram

class OrbitalsTable(ft.DataTable):
    def __init__(self,img : ft.Image):
        super().__init__(columns=[])
        self.img_element = img
        self.x_text = ""
        self.y_text = ""

        self.orbitals :List[Group] = []
        self.columns = [
            ft.DataColumn(ft.Container(ft.Text(""),width=30, alignment=ft.alignment.center)),
            ft.DataColumn(ft.Container(ft.Text("Name"),width=100, alignment=ft.alignment.center)),
            ft.DataColumn(ft.Container(ft.Text("Homo"),width=80, alignment=ft.alignment.center)),
            ft.DataColumn(ft.Container(ft.Text("Lumo"),width=80, alignment=ft.alignment.center)),
            ft.DataColumn(ft.Container(ft.Text("Color"),width=100, alignment=ft.alignment.center)),
            ft.DataColumn(ft.Container(ft.Text("id"),width=50, alignment=ft.alignment.center))
        ]

        self.column_spacing = 20.0

        self.name = ft.TextField(label='', autofocus=True)
        self.homo = ft.TextField(label='')
        self.lumo = ft.TextField(label='')
        self.color = ft.Dropdown(
            value="Red",
            options=[
                ft.dropdown.Option("Red"),
                ft.dropdown.Option("Green"),
                ft.dropdown.Option("Blue")
            ],
            width=100
        )
        self.add_button = ft.ElevatedButton("Add")

        self.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(self.add_button),
                    ft.DataCell(ft.Container(self.name,width=100,alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(self.homo,width=80,alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(self.lumo,width=80,alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(self.color,width=100,alignment=ft.alignment.center)),
                    ft.DataCell(ft.Container(ft.Text(""), width=50, alignment=ft.alignment.center)),
                ])
        ]

        self.controls = [
            self.name,
            self.homo,
            self.lumo,
            self.color,
            self.name
        ]

    def delete_orbital(self, id: str,x: str, y: str):
        self.orbitals = [i for i in self.orbitals if i.id != id]

        new_rows = []
        for row in self.rows:

            add_or_delete_button = row.cells[0].content

            # 最初の行 (フォーム部分)
            if add_or_delete_button.text == "Add":
                new_rows.append(row)
            # 最初の行 (フォーム部分) 以外
            else:
                if row.cells[5].content.value != id:
                    new_rows.append(row)

        self.rows = new_rows

        self.update_diagram(x,y)
        self.update()

    def __orbital_to_element(self,orbital:Group):
        return ft.DataRow(
                cells=[
                    ft.DataCell(ft.ElevatedButton("delete", on_click=lambda _: self.delete_orbital(orbital.id))),
                    ft.DataCell(ft.Text(orbital.name)),
                    ft.DataCell(ft.Text(orbital.homo)),
                    ft.DataCell(ft.Text(orbital.lumo)),
                    ft.DataCell(ft.Text(orbital.color)),
                    ft.DataCell(ft.Text(orbital.id))
                ]
            )

    def add_orbital(self):
        orbital = Group(self.name.value,self.homo.value,self.lumo.value,color=self.color.value)
        self.orbitals.append(orbital)

        self.rows.append(self.__orbital_to_element(orbital))

        self.name.value = ""
        self.homo.value = ""
        self.lumo.value = ""
        self.color.value = ""
        self.name.focus()

        self.update_diagram()
        self.update()

    def update_diagram(self):
        diagram = Diagram(self.x_text,self.y_text,self.orbitals)
        self.img_element.src_base64 = diagram.base64()
        self.img_element.update()

    def save_diagram(self,file_path):
        save_img = base64.b64decode(self.img_element.src_base64.encode())
        with open(file_path, 'bw') as f3:
            f3.write(save_img)

    def add_button_setup(self):
        self.add_button.on_click = self.add_orbital



def main(page):
    graph_x = ft.TextField(label="x")
    graph_y = ft.TextField(label="y")

    img = ft.Image(
        src=f"plane_diagram.png",
        width=400,
        height=400,
        fit=ft.ImageFit.CONTAIN,
    )
    orbitals_table = OrbitalsTable(img)
    orbitals_table.add_button_setup()

    def apply_xy_text(_):
        orbitals_table.x_text = graph_x.value
        orbitals_table.y_text = graph_y.value

    apply_button = ft.ElevatedButton("apply",on_click=apply_xy_text)

    def on_file_picked(e: ft.FilePickerResultEvent):
        orbitals_table.save_diagram(e.path)
        page.update()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    def show_file_picker(e):
        file_picker.save_file(
            file_name="diagram.png",
            file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=['png']
        )

    save_button = ft.ElevatedButton("Save", on_click=show_file_picker)

    page.add(
        ft.Row([
            graph_x,
            graph_y,
            apply_button
        ], alignment=ft.MainAxisAlignment.START),
        ft.Row([
            ft.Card(orbitals_table,height=400),
            ft.Container(ft.Column(
                [
                    img,
                    save_button,
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            ),height=500)
        ],alignment=ft.MainAxisAlignment.START),
    )

    page.controls.append(img)


ft.app(target=main)