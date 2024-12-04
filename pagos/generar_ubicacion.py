def generar_ubicaciones_dinamico(terreno_ancho, terreno_largo, casa_ancho, casa_largo, calle_ancho, cul_de_sac_ancho):
    # Calculate the x-coordinates for the central street
    x_calle_central_inicio = (terreno_ancho // 2) - (calle_ancho // 2)
    x_calle_central_fin = (terreno_ancho // 2) + (calle_ancho // 2)

    ubicaciones_casas = []
    ubicaciones_cul_de_sac = []
    ubicaciones_calle_central = []

    # Define initial y-coordinate
    y_inicio = 0
    first_row = True  # Used to alternate between single row and double row

    while y_inicio + casa_largo <= terreno_largo:
        # Place one or two rows of houses
        rows = 1 if first_row else 2
        for row in range(rows):
            if y_inicio + casa_largo > terreno_largo:
                break
            # Place a row of houses on the left side of the central street
            x_inicio = x_calle_central_inicio - casa_ancho
            while x_inicio >= 0:
                casa = [
                    [x_inicio, y_inicio],  # Bottom-left corner
                    [x_inicio + casa_ancho, y_inicio],  # Bottom-right corner
                    [x_inicio + casa_ancho, y_inicio + casa_largo],  # Top-right corner
                    [x_inicio, y_inicio + casa_largo]  # Top-left corner
                ]
                ubicaciones_casas.append(casa)
                x_inicio -= casa_ancho

            # Place a row of houses on the right side of the central street
            x_inicio = x_calle_central_fin
            while x_inicio + casa_ancho <= terreno_ancho:
                casa = [
                    [x_inicio, y_inicio],  # Bottom-left corner
                    [x_inicio + casa_ancho, y_inicio],  # Bottom-right corner
                    [x_inicio + casa_ancho, y_inicio + casa_largo],  # Top-right corner
                    [x_inicio, y_inicio + casa_largo]  # Top-left corner
                ]
                ubicaciones_casas.append(casa)
                x_inicio += casa_ancho

            # Add central street section for the current block
            calle_central_izquierda = [
                [x_calle_central_inicio, y_inicio],
                [x_calle_central_inicio, y_inicio + casa_largo]
            ]
            calle_central_derecha = [
                [x_calle_central_fin, y_inicio],
                [x_calle_central_fin, y_inicio + casa_largo]
            ]
            ubicaciones_calle_central.append(calle_central_izquierda)
            ubicaciones_calle_central.append(calle_central_derecha)

            y_inicio += casa_largo  # Move to next row of houses

        # Add a cul-de-sac if there's enough space
        if y_inicio + cul_de_sac_ancho <= terreno_largo:
            cul_de_sac = [
                [0, y_inicio],  # Left side of cul-de-sac
                [terreno_ancho, y_inicio],  # Right side of cul-de-sac
                [terreno_ancho, y_inicio + cul_de_sac_ancho],  # Top-right
                [0, y_inicio + cul_de_sac_ancho]  # Top-left
            ]
            ubicaciones_cul_de_sac.append(cul_de_sac)
            y_inicio += cul_de_sac_ancho  # Skip space for the cul-de-sac

        # Toggle between single and double rows for the next iteration
        first_row = not first_row

    # Calculate the area of each house and the total area occupied by all houses
    area_casa = casa_ancho * casa_largo
    total_area_casas = area_casa * len(ubicaciones_casas)
    total_area_terreno = terreno_ancho * terreno_largo

    return ubicaciones_casas, ubicaciones_cul_de_sac, ubicaciones_calle_central, area_casa, total_area_casas, total_area_terreno


# Example Parameters
terreno_ancho = 410  # Width of the land in meters
terreno_largo = 670  # Length of the land in meters
casa_ancho = 30      # Width of each house in meters
casa_largo = 80      # Length of each house in meters
calle_ancho = 15     # Width of the central street in meters
cul_de_sac_ancho = 10  # Width reserved for cul-de-sacs

# Generate Locations
ubicaciones_casas, ubicaciones_cul_de_sac, ubicaciones_calle_central, area_casa, total_area_casas, total_area_terreno = generar_ubicaciones_dinamico(
    terreno_ancho, terreno_largo, casa_ancho, casa_largo, calle_ancho, cul_de_sac_ancho
)

# Output Results
print(f"Ubicaciones de casas (total {len(ubicaciones_casas)}):")
for idx, casa in enumerate(ubicaciones_casas, 1):
    print(f"Casa {idx}: {casa}")

print(f"\nUbicaciones de cul-de-sacs (total {len(ubicaciones_cul_de_sac)}):")
for idx, cul_de_sac in enumerate(ubicaciones_cul_de_sac, 1):
    print(f"Cul-de-sac {idx}: {cul_de_sac}")

print(f"\nUbicaciones de la calle central (total {len(ubicaciones_calle_central)}):")
for idx, calle in enumerate(ubicaciones_calle_central, 1):
    print(f"Calle central {idx}: {calle}")

print(f"\nÁrea de cada casa: {area_casa} m²")
print(f"Total área ocupada por las casas: {total_area_casas} m²")
print(f"Área total del terreno: {total_area_terreno} m²")
