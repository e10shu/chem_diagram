from datetime import datetime

import flet as ft

from diagram import Group, Diagram



def main(page):
    graph_x = ft.TextField(label="x")
    graph_y = ft.TextField(label="y")

    name = ft.TextField(label='name', autofocus=True,width=150)
    homo = ft.TextField(label="homo",width=150)
    lumo = ft.TextField(label="lumo",width=150)
    color = ft.Dropdown(
        value = "Red",
        options=[
            ft.dropdown.Option("Red"),
            ft.dropdown.Option("Green"),
            ft.dropdown.Option("Blue")
        ],
    )

    img = ft.Image(
        src=f"plane_diagram.png",
        width=500,
        height=500,
        fit=ft.ImageFit.CONTAIN,
    )

    orbital_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("")),
            ft.DataColumn(ft.Text("Name",width=100)),
            ft.DataColumn(ft.Text("Homo",width=100)),
            ft.DataColumn(ft.Text("Lumo",width=100)),
            ft.DataColumn(ft.Text("Color",width=100)),
            ft.DataColumn(ft.Text("id"))
        ],
        rows=[
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text("New")),
                    ft.DataCell(name),
                    ft.DataCell(homo),
                    ft.DataCell(lumo),
                    ft.DataCell(color)
                ])
        ],
    )

    def delete(e,id):
        groups_table_row = []
        for row in orbital_table.rows:
            if row.cells[0].content.__class__.__name__ == "ElevatedButton":
                if row.cells[5].content.value != id:
                    groups_table_row.append(row)
            else:
                groups_table_row.append(row)

        orbital_table.rows = groups_table_row
        print(orbital_table.rows)
        page.update()

    def add(e):
        group_id = datetime.now().strftime("%f")

        orbital_table.rows.append(ft.DataRow(
                cells=[
                    ft.DataCell(ft.ElevatedButton("delete", on_click=lambda e: delete(e,group_id))),
                    ft.DataCell(ft.Text(name.value)),
                    ft.DataCell(ft.Text(homo.value)),
                    ft.DataCell(ft.Text(lumo.value)),
                    ft.DataCell(ft.Text(color.value)),
                    ft.DataCell(ft.Text(group_id))
                ]
            ),)

        name.value = ""
        homo.value = ""
        lumo.value = ""
        color.value = ""
        page.update()
        name.focus()

    add_button = ft.ElevatedButton("Add", on_click=add)
    orbital_table.rows[0].cells.append(ft.DataCell(add_button))

    def on_file_picked(e: ft.FilePickerResultEvent):
        target_file.value = e.path
        page.update()

        generate()

    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    def show_file_picker(e):
        file_picker.save_file(
            file_name="diagram.png",
            file_type=ft.FilePickerFileType.CUSTOM, allowed_extensions=['png']
        )

    target_file = ft.Text("file path")

    def generate():
        if target_file.value == "file path":
            print("file is not selected!")
        else:
            groups = []
            for row in orbital_table.rows:
                data_table = row.cells
                if str(row.cells[0].content.__class__.__name__) == "ElevatedButton":
                    new_name = data_table[1].content.value
                    new_homo = data_table[2].content.value
                    new_lumo = data_table[3].content.value
                    new_color = data_table[4].content.value
                    groups.append(Group(new_name,new_homo,new_lumo,new_color))


            d = Diagram(graph_x.value,graph_y.value,groups)
            d.plot(target_file.value)

            img.src = target_file.value
            page.update()

    generate_button = ft.ElevatedButton("Generate", on_click=show_file_picker)

    page.add(
        ft.Card(orbital_table),
        ft.Row([
            graph_x,
            graph_y,
            target_file,
            generate_button
        ], alignment=ft.MainAxisAlignment.START),
        img
    )

ft.app(target=main)