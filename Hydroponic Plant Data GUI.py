import PySimpleGUI as sg
import openpyxl

def calculate_tds(data):
    """Calculates Total Dissolved Solids (TDS)."""
    tds = sum(data[2:])  # Sum all the components from index 2 onwards
    return tds

def calculate_ec(tds):
    """Calculates Electrical Conductivity (EC) using the TDS value."""
    ec = (tds * 2) / 1000  # Calculate EC using the formula EC = (TDS * 2) / 1000
    return ec

def calculate_salt_required(data, volume):
    """Calculates the amount of salts required based on the given data and volume."""
    # Conversion factors for converting ppm to mg
    ppm_to_mg = 1 / 1000

    # Salt names and their corresponding indices in the data
    salt_names = ['KNO3', 'CaNO3', 'NH4NO3', 'K2HPO4', 'MgSO4', 'NaCl']
    salt_indices = [6, 7, 8, 16, 18, 9]  # Indices of salts in the data list

    salt_required = {}
    for salt_name, salt_index in zip(salt_names, salt_indices):
        salt_ppm = data[salt_index]
        salt_mg = salt_ppm * volume * ppm_to_mg
        salt_required[salt_name] = salt_mg

    return salt_required

def create_gui():
    """Creates the GUI to display plant data."""
    workbook = openpyxl.load_workbook('D:/Output/copy of Phase 1.xlsx')
    sheet = workbook.active

    headers = [cell.value for cell in sheet[1]]
    plant_data = []

    for row in sheet.iter_rows(min_row=2, values_only=True):
        plant_data.append(row)

    plant_names = [data[0] for data in plant_data]

    cell_widths = [20, 10, 10, 10, 15, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]

    layout = [
        [sg.Text('Select Plant:'), sg.Combo(plant_names, key='plant_combo', enable_events=True)],
        [sg.Text('Plant Data:', font=('Arial', 14))],
        [
            sg.Table(
                values=[['' for _ in headers]],
                headings=headers,
                key='plant_data_table',
                justification='center',
                num_rows=10,
                enable_events=True,
                col_widths=cell_widths,
                auto_size_columns=False,
                vertical_scroll_only=True,
                hide_vertical_scroll=True
            )
        ],
        [sg.Text('TDS:', font=('Arial', 14))],
        [sg.Input(key='tds_output', readonly=True)],
        [sg.Text('EC:', font=('Arial', 14))],
        [sg.Input(key='ec_output', readonly=True)],
        [sg.Text('Volume (mL):'), sg.Input(key='volume_input')],
        [sg.Button('Calculate Salts')]
    ]

    window = sg.Window('Hydroponic Plant Data', layout)

    while True:
        event, values = window.read()


        if event == sg.WINDOW_CLOSED:
            break

        if event == 'plant_combo':
            plant_name = values['plant_combo']
            data = next((row for row in plant_data if row[0] == plant_name), [])
            table_data = [[str(cell) for cell in data]]
            window['plant_data_table'].update(values=table_data)
            tds = calculate_tds(data)
            window['tds_output'].update(tds)
            ec = calculate_ec(tds)
            window['ec_output'].update(ec)

        if event == 'Calculate Salts':
            volume = int(values['volume_input'])
            plant_name = values['plant_combo']
            data = next((row for row in plant_data if row[0] == plant_name), [])
            salt_required = calculate_salt_required(data, volume)
            sg.popup(f'Salt Required (in mg):\n{salt_required}')

        if event.startswith('plant_data_table'):
            row, col = map(int, event.split('-')[1:])
            sg.popup(f'Cell selected: Row={row}, Column={col}')

    window.close()

create_gui()
