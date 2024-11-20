import pandas as pd
import os
from datetime import datetime
import numpy_financial as npf
import sys
from dateutil.relativedelta import relativedelta

#=====================================================================================================#
#=====================================================================================================#
#=====================================================================================================#


def calculate_payments(apartment_type, total_units, price, units_sold_per_month, units_delivered_per_month, price_increase_threshold, price_increase_percentage, down_payment_percentage, finance_percentage, completion_percentage, finance_months, start_selling_month, end_of_construction_month):
    data = []
    current_price = price
    apartment_number = 1
    month_counter = start_selling_month
    units_sold = 0

    # Dictionary to store delivery month for each apartment
    delivery_months = {}
    
    # Calculate delivery months based on units_delivered_per_month
    for i in range(total_units):
        delivery_months[i + 1] = end_of_construction_month + 1 + (i // units_delivered_per_month)

    while apartment_number <= total_units:
        # Selling only units_sold_per_month apartments in each month
        for _ in range(units_sold_per_month):
            if apartment_number > total_units:
                break

            if units_sold % price_increase_threshold == 0 and units_sold != 0:
                current_price *= (1 + price_increase_percentage)

            # Check the delivery month for the current apartment
            delivery_month = delivery_months[apartment_number]

            # Determine if it's a presale or a normal sale
            if month_counter <= end_of_construction_month:
                # Presale phase: Record down payment
                down_payment = current_price * down_payment_percentage
                data.append({
                    'Apartment Type': apartment_type,
                    'Apartment': apartment_number,
                    'Month': month_counter,
                    'Payment Type': '1. Down Payment',
                    'Amount': down_payment
                })

                # Calculate delivery month and register completion payment
                completion_amount = current_price * completion_percentage
                data.append({
                    'Apartment Type': apartment_type,
                    'Apartment': apartment_number,
                    'Month': delivery_month,
                    'Payment Type': '3. Completion Amount',
                    'Amount': completion_amount
                })

                # Include finance payments in the months between down payment and delivery
                available_finance_months = min(finance_months, delivery_month - month_counter - 1)
                
                if available_finance_months > 0:
                    for m in range(1, int(available_finance_months) + 1):
                        if month_counter + m < delivery_month:
                            monthly_payment = (current_price * finance_percentage) / available_finance_months
                            data.append({
                                'Apartment Type': apartment_type,
                                'Apartment': apartment_number,
                                'Month': month_counter + m,
                                'Payment Type': '2. Monthly Payment',
                                'Amount': monthly_payment
                            })
            else:
                # Normal sale phase: full payment after construction ends
                full_payment = current_price * (down_payment_percentage + finance_percentage + completion_percentage)
                data.append({
                    'Apartment Type': apartment_type,
                    'Apartment': apartment_number,
                    'Month': month_counter,
                    'Payment Type': '4. Full Payment',
                    'Amount': full_payment
                })

            apartment_number += 1
            units_sold += 1

        month_counter += 1

    return data


#=====================================================================================================#
#=====================================================================================================#
#=====================================================================================================#

import pandas as pd
from .models import ProjectCost  # Adjust import based on your project structure

def calculate_apartment_payments(project_cost_id):
    # Retrieve the project cost instance from the database
    project_cost = ProjectCost.objects.get(id=project_cost_id)
    

    # Calculate total months between start and end dates
    total_months = (project_cost.fecha_fin_proyecto.year - project_cost.fecha_inicio_proyecto.year) * 12 + \
                   (project_cost.fecha_fin_proyecto.month - project_cost.fecha_inicio_proyecto.month)

           
    mes_fin_cons = (project_cost.fecha_fin_construccion.year - project_cost.fecha_inicio_proyecto.year) * 12 + (project_cost.fecha_fin_construccion.month - project_cost.fecha_inicio_proyecto.month)
    
    # Lot details from the ProjectCost instance
    
    precio_por_m2 = project_cost.precio_por_m2
    tamaño_promedio_lotes = project_cost.tamaño_promedio_lotes
    
    numero_lotes = project_cost.numero_lotes
    precio_venta_lotes = precio_por_m2 * tamaño_promedio_lotes
    absorcion_mensual_lotes = project_cost.absorcion_mensual_lotes
    escrituracion_por_mes_lotes = project_cost.escrituracion_por_mes_lotes
    
    enganche_lotes = project_cost.enganche_lotes / 100
    financiamiento_lotes = project_cost.financiamiento_lotes / 100
    liquidacion_lotes = project_cost.liquidacion_lotes / 100

    plazo_financiamiento_lotes = project_cost.plazo_financiamiento_lotes
    incremento_precio_por_ud_vendidas_lotes = project_cost.incremento_precio_por_ud_vendidas_lotes
    incremento_precio_lotes = project_cost.incremento_precio_lotes / 100


    
    # Check if number of lots is valid
    if numero_lotes is None or numero_lotes <= 0:
        data_E = None
    else:
        data_E = calculate_payments(
            'Lotes',
            numero_lotes,
            precio_venta_lotes,
            absorcion_mensual_lotes,
            escrituracion_por_mes_lotes,
            incremento_precio_por_ud_vendidas_lotes,
            incremento_precio_lotes,
            enganche_lotes,
            financiamiento_lotes,
            liquidacion_lotes,
            plazo_financiamiento_lotes,
            project_cost.mes_inicio_proyecto,  # Use the appropriate variables from the model
            mes_fin_cons  # Assuming this is needed for calculations
        )

    
        # Create a DataFrame from the combined data
    if data_E:
        df = pd.DataFrame(data_E)
        df = df.round(2)  # Round the DataFrame to two decimal places

        # Generate a pivot table
        pivot_table = df.pivot_table(index=['Apartment Type', 'Apartment', 'Payment Type'],
                                      columns='Month', values='Amount', fill_value=0)
        
        # Reindex the pivot table to include all months in the range
        pivot_table = pivot_table.reindex(columns=range(1, total_months + 1), fill_value=0)
        
        # Convert to HTML
        return pivot_table

    return None


#=====================================================================================================#
#=====================================================================================================#
#=====================================================================================================#


def calculate_monthly_sums(pivot_table):
    # Sum the amounts for each month (i.e., sum over the rows)
    monthly_sums = pivot_table.sum(axis=0)

    # Transpose the result so that months are columns and the sum is a single row
    monthly_sums_df = pd.DataFrame(monthly_sums).T

    # Rename the index for clarity
    monthly_sums_df.index = ['Total Amount']

    # Add a "Month 0" column at the beginning with a value of 0
    monthly_sums_df.insert(0, '0', 0)
    
    return monthly_sums_df

#=====================================================================================================#
#=====================================================================================================#
#=====================================================================================================#

def calculate_comisiones(apartment_type, total_units, price, units_sold_per_month, units_delivered_per_month, 
                        price_increase_threshold, price_increase_percentage, down_payment_percentage, 
                        finance_percentage, completion_percentage, finance_months, start_selling_month, 
                        end_of_construction_month,comision, comision_contraventa, comision_contraescritura):
    
    data = []
    commission_data = []
    current_price = price
    apartment_number = 1
    month_counter = start_selling_month
    units_sold = 0
    


    # Dictionary to store delivery month for each apartment
    delivery_months = {}
    
    # Calculate delivery months based on units_delivered_per_month
    for i in range(total_units):
        delivery_months[i + 1] = end_of_construction_month + 1 + (i // units_delivered_per_month)

    while apartment_number <= total_units:
        # Selling only units_sold_per_month apartments in each month
        for _ in range(units_sold_per_month):
            if apartment_number > total_units:
                break

            if units_sold % price_increase_threshold == 0 and units_sold != 0:
                current_price *= (1 + price_increase_percentage)

            # Check the delivery month for the current apartment
            delivery_month = delivery_months[apartment_number]

            # Calculate the sales commission
            sales_commission = current_price * comision
            down_payment_commission = sales_commission * comision_contraventa
            delivery_commission = sales_commission * comision_contraescritura

            # Determine if it's a presale or a normal sale
            if month_counter <= end_of_construction_month:
                # Presale phase: Record down payment
                down_payment = current_price * down_payment_percentage
                data.append({
                    'Apartment Type': apartment_type,
                    'Apartment': apartment_number,
                    'Month': month_counter,
                    'Payment Type': '1. Down Payment',
                    'Amount': down_payment
                })

                # Include 75% of sales commission in the down payment month
                commission_data.append({
                    'Apartment Type': apartment_type,
                    'Apartment': apartment_number,
                    'Month': month_counter,
                    'Payment Type': 'Sales Commission (Down Payment)',
                    'Amount': down_payment_commission
                })

                # Calculate delivery month and register completion payment
                completion_amount = current_price * completion_percentage
                data.append({
                    'Apartment Type': apartment_type,
                    'Apartment': apartment_number,
                    'Month': delivery_month,
                    'Payment Type': '3. Completion Amount',
                    'Amount': completion_amount
                })

                # Include 25% of sales commission in the delivery month
                commission_data.append({
                    'Apartment Type': apartment_type,
                    'Apartment': apartment_number,
                    'Month': delivery_month,
                    'Payment Type': 'Sales Commission (Delivery)',
                    'Amount': delivery_commission
                })

                # Include finance payments in the months between down payment and delivery
                available_finance_months = min(finance_months, delivery_month - month_counter - 1)
                
                if available_finance_months > 0:
                    for m in range(1, int(available_finance_months) + 1):
                        if month_counter + m < delivery_month:
                            monthly_payment = (current_price * finance_percentage) / available_finance_months
                            data.append({
                                'Apartment Type': apartment_type,
                                'Apartment': apartment_number,
                                'Month': month_counter + m,
                                'Payment Type': '2. Monthly Payment',
                                'Amount': monthly_payment
                            })
            else:
                # Normal sale phase: full payment after construction ends
                full_payment = current_price * (down_payment_percentage + finance_percentage + completion_percentage)
                data.append({
                    'Apartment Type': apartment_type,
                    'Apartment': apartment_number,
                    'Month': month_counter,
                    'Payment Type': 'Full Payment',
                    'Amount': full_payment
                })

                # Include full sales commission in the month of full payment
                commission_data.append({
                    'Apartment Type': apartment_type,
                    'Apartment': apartment_number,
                    'Month': month_counter,
                    'Payment Type': 'Sales Commission (Full Payment)',
                    'Amount': sales_commission
                })

            apartment_number += 1
            units_sold += 1

        month_counter += 1

    # Create DataFrames for sales and commission data
    sales_df = pd.DataFrame(data)
    commission_df = pd.DataFrame(commission_data)

    return commission_df
#=====================================================================================================#
#=====================================================================================================#
#=====================================================================================================#


def calculate_apartment_comisiones(project_cost_id):
    # Retrieve the project cost instance from the database
    project_cost = ProjectCost.objects.get(id=project_cost_id)
    

    # Calculate total months between start and end dates
    total_months = (project_cost.fecha_fin_proyecto.year - project_cost.fecha_inicio_proyecto.year) * 12 + \
                   (project_cost.fecha_fin_proyecto.month - project_cost.fecha_inicio_proyecto.month)

           
    mes_fin_cons = (project_cost.fecha_fin_construccion.year - project_cost.fecha_inicio_proyecto.year) * 12 + (project_cost.fecha_fin_construccion.month - project_cost.fecha_inicio_proyecto.month)
    
    # Lot details from the ProjectCost instance
    precio_por_m2 = project_cost.precio_por_m2
    tamaño_promedio_lotes = project_cost.tamaño_promedio_lotes
    
    numero_lotes = project_cost.numero_lotes
    precio_venta_lotes = precio_por_m2 * tamaño_promedio_lotes
    absorcion_mensual_lotes = project_cost.absorcion_mensual_lotes
    escrituracion_por_mes_lotes = project_cost.escrituracion_por_mes_lotes
    
    enganche_lotes = project_cost.enganche_lotes / 100
    financiamiento_lotes = project_cost.financiamiento_lotes / 100
    liquidacion_lotes = project_cost.liquidacion_lotes / 100

    plazo_financiamiento_lotes = project_cost.plazo_financiamiento_lotes
    incremento_precio_por_ud_vendidas_lotes = project_cost.incremento_precio_por_ud_vendidas_lotes
    incremento_precio_lotes = project_cost.incremento_precio_lotes / 100

    comision = project_cost.comercializacion / 100
    comision_contraventa = project_cost.comision_contraventa / 100
    comision_contraescritura = project_cost.comision_contraescritura / 100

    
    # Check if number of lots is valid
    if numero_lotes is None or numero_lotes <= 0:
        data_E = None
    else:
        data_E = calculate_comisiones(
            'Lotes',
            numero_lotes,
            precio_venta_lotes,
            absorcion_mensual_lotes,
            escrituracion_por_mes_lotes,
            incremento_precio_por_ud_vendidas_lotes,
            incremento_precio_lotes,
            enganche_lotes,
            financiamiento_lotes,
            liquidacion_lotes,
            plazo_financiamiento_lotes,
            project_cost.mes_inicio_proyecto,  # Use the appropriate variables from the model
            mes_fin_cons,
            comision,
            comision_contraventa,
            comision_contraescritura  # Assuming this is needed for calculations
        )


        df = pd.DataFrame(data_E)
        df = df.round(2)  # Round the DataFrame to two decimal places

        # Generate a pivot table
        pivot_table = df.pivot_table(index=['Apartment Type', 'Apartment', 'Payment Type'],
                                      columns='Month', values='Amount', fill_value=0)
        
        # Reindex the pivot table to include all months in the range
        pivot_table = pivot_table.reindex(columns=range(1, total_months + 1), fill_value=0)
        
        # Convert to HTML
        return pivot_table

    return None

#=====================================================================================================#
#=====================================================================================================#
#=====================================================================================================#

def calculate_hard_costs(project_cost_id):
    project_cost = ProjectCost.objects.get(id=project_cost_id)
    
    
    # Extracting values from the project_variables dictionary
    numero_lotes = project_cost.numero_lotes
    tamaño_promedio_lotes = project_cost.tamaño_promedio_lotes
    cesion_municipal = project_cost.cesion_municipal
    vialidades_pavimentos = project_cost.vialidades_pavimentos
    jardines_amenidades_externas = project_cost.jardines_amenidades_externas
    costo_area_vendible_lotes = project_cost.costo_area_vendible_lotes
    costo_vialidades_pavimentos = project_cost.costo_vialidades_pavimentos
    costo_amenidades_externas = project_cost.costo_amenidades_externas
    costo_exterior_municipal = project_cost.costo_exterior_municipal
    imprevistos_hard = project_cost.imprevistos_hard / 100
    iva_hard_cost = project_cost.iva_hard_cost / 100

    # Calculating total sellable area for departments
    area_vendible_lotes = (
        numero_lotes * tamaño_promedio_lotes
    )
    
    # Calculating the draft hard costs
    draft_hard_cost = (
        (area_vendible_lotes * costo_area_vendible_lotes) +
        (vialidades_pavimentos * costo_vialidades_pavimentos) +
        (jardines_amenidades_externas * costo_amenidades_externas) +
        (cesion_municipal * costo_exterior_municipal)
    )

    # Final hard costs calculation with contingencies and taxes
    draft_hard_cost2 = draft_hard_cost * (1 + imprevistos_hard)
    total_hard_cost = draft_hard_cost*(iva_hard_cost) +draft_hard_cost2

    return total_hard_cost

    

#=====================================================================================================#
#=====================================================================================================#
#=====================================================================================================#
from django.shortcuts import get_object_or_404

def calculate_soft_costs(project_cost_id):
    # Assuming project_cost is retrieved by project_cost_id
    project_cost = get_object_or_404(ProjectCost, id=project_cost_id)
    total_hard_cost = calculate_hard_costs(project_cost_id)
    
    # Get the pivot table from calculate_project_ingresos
    pivot_table = calculate_apartment_payments(project_cost_id)
    monthly_sums_df = calculate_monthly_sums(pivot_table)
    total_ingresos = monthly_sums_df.sum().sum()
    
    ## Calculo de comisiones
    pivot_table_comisiones = calculate_apartment_comisiones(project_cost_id)
    comisiones = calculate_monthly_sums(pivot_table_comisiones).loc['Total Amount'].tolist()

    pre_planeacion = project_cost.pre_planeacion / 100
    fee_desarrollo = project_cost.fee_desarrollo / 100
    mercadotecnia = project_cost.mercadotecnia / 100
    gerencia_de_obra = project_cost.gerencia_de_obra / 100
    ingenierias_estudios = project_cost.ingenierias_estudios / 100
    tramites_permisos = project_cost.tramites_permisos / 100
    legal_fiscal = project_cost.legal_fiscal / 100
    proyecto_ejecutivo = project_cost.proyecto_ejecutivo / 100
    imprevistos_soft = project_cost.imprevistos_soft / 100
    iva_soft_cost = project_cost.iva_soft_cost / 100

#---------------------------

    # Calculate total months between start and end dates
    total_months = (project_cost.fecha_fin_proyecto.year - project_cost.fecha_inicio_proyecto.year) * 12 + \
                   (project_cost.fecha_fin_proyecto.month - project_cost.fecha_inicio_proyecto.month)

    # Meses
    fecha_inicio_proyecto = project_cost.fecha_inicio_proyecto
    
    fecha_inicio_construccion = project_cost.fecha_inicio_construccion
    fecha_fin_construccion = project_cost.fecha_fin_construccion

    fecha_inicio_preplaneacion = project_cost.fecha_inicio_preplaneacion
    fecha_fin_preplaneacion = project_cost.fecha_fin_preplaneacion

    fecha_inicio_mkt = project_cost.fecha_inicio_mkt
    fecha_fin_mkt = project_cost.fecha_fin_mkt

    fecha_inicio_tramites = project_cost.fecha_inicio_tramites
    fecha_fin_tramites = project_cost.fecha_fin_tramites

    fecha_inicio_legal_fiscal = project_cost.fecha_inicio_legal_fiscal
    fecha_fin_legal_fiscal = project_cost.fecha_fin_legal_fiscal

    fecha_inicio_proy_ejecutivo = project_cost.fecha_inicio_proy_ejecutivo
    fecha_fin_proy_ejecutivo = project_cost.fecha_fin_proy_ejecutivo

#---------------------------

    # Calculating for 'Construcción' months using calculate_month_difference
    mes_inicio_construccion = calculate_month_difference(fecha_inicio_construccion, fecha_inicio_proyecto)
    mes_fin_construccion = calculate_month_difference(fecha_fin_construccion, fecha_inicio_proyecto)
    
    # Calculating for 'Pre-planeación' months using calculate_month_difference
    mes_inicio_preplaneacion = calculate_month_difference(fecha_inicio_preplaneacion, fecha_inicio_proyecto)
    mes_fin_preplaneacion = calculate_month_difference(fecha_fin_preplaneacion, fecha_inicio_proyecto)

    # Calculating for 'MKT' months using calculate_month_difference
    mes_inicio_mkt = calculate_month_difference(fecha_inicio_mkt, fecha_inicio_proyecto)
    mes_fin_mkt = calculate_month_difference(fecha_fin_mkt, fecha_inicio_proyecto)

    # Calculating for 'Tramites' months using calculate_month_difference
    mes_inicio_tramites = calculate_month_difference(fecha_inicio_tramites, fecha_inicio_proyecto)
    mes_fin_tramites = calculate_month_difference(fecha_fin_tramites, fecha_inicio_proyecto)

    # Calculating for 'Legal Fiscal' months using calculate_month_difference
    mes_inicio_legal_fiscal = calculate_month_difference(fecha_inicio_legal_fiscal, fecha_inicio_proyecto)
    mes_fin_legal_fiscal = calculate_month_difference(fecha_fin_legal_fiscal, fecha_inicio_proyecto)

    # Calculating for 'Proyecto Ejecutivo' months using calculate_month_difference
    mes_inicio_proy_ejecutivo = calculate_month_difference(fecha_inicio_proy_ejecutivo, fecha_inicio_proyecto)
    mes_fin_proy_ejecutivo = calculate_month_difference(fecha_fin_proy_ejecutivo, fecha_inicio_proyecto)

    #---------------------------
    
    duration_pre = mes_fin_preplaneacion - mes_inicio_preplaneacion + 1
    pre_planeacion_cost = (total_ingresos * pre_planeacion) / duration_pre

    # Calculating 'Mercadotecnia' for specific months
    duration_mkt = mes_fin_mkt - mes_inicio_mkt + 1
    mkt_cost = (total_ingresos * mercadotecnia) / duration_mkt

    # Calculating 'Gerencia de obra' for specific months
    duration_construccion = mes_fin_construccion - mes_inicio_construccion + 1
    gerencia_de_obra_cost = (total_hard_cost * gerencia_de_obra) / duration_construccion

    # Calculating 'Trámites' for specific months
    duration_tramites = mes_fin_tramites - mes_inicio_tramites + 1
    tramites_cost = (total_hard_cost * tramites_permisos) / duration_tramites
    ingenierias_cost = (total_hard_cost * ingenierias_estudios) / duration_tramites

    # Calculating 'Legal Fiscal' for specific months
    duration_legal_fiscal = mes_fin_legal_fiscal - mes_inicio_legal_fiscal + 1
    legal_fiscal_cost = (total_hard_cost * legal_fiscal) / duration_legal_fiscal

    # Calculating 'Proyecto Ejecutivo' for specific months
    duration_proy_ejecutivo = mes_fin_proy_ejecutivo - mes_inicio_proy_ejecutivo + 1
    proy_ejecutivo_cost = (total_hard_cost * proyecto_ejecutivo) / duration_proy_ejecutivo

    # Creating a DataFrame for monthly expenses
    monthly_data = []

    for month in range(1, total_months + 1):
        month_data = {
            'Pre_planeacion': pre_planeacion_cost if mes_inicio_preplaneacion <= month <= mes_fin_preplaneacion else 0,
            'Fee_desarrollo': (total_ingresos * fee_desarrollo) / total_months,
            'Mercadotecnia': mkt_cost if mes_inicio_mkt <= month <= mes_fin_mkt else 0,
            'Gerencia_de_obra': gerencia_de_obra_cost if mes_inicio_construccion <= month <= mes_fin_construccion else 0,
            'Tramites_y_permisos': tramites_cost if mes_inicio_tramites <= month <= mes_fin_tramites else 0,
            'Ingenierias_Estudios': ingenierias_cost if mes_inicio_tramites <= month <= mes_fin_tramites else 0,
            'Legal_y_fiscal': legal_fiscal_cost if mes_inicio_legal_fiscal <= month <= mes_fin_legal_fiscal else 0,
            'Proyecto_ejecutivo': proy_ejecutivo_cost if mes_inicio_proy_ejecutivo <= month <= mes_fin_proy_ejecutivo else 0,
        }
        monthly_data.append(month_data)

    # Creating the DataFrame with 'Mes' as the index
    df_monthly_soft_costs = pd.DataFrame(monthly_data, index=pd.Index(range(1, total_months + 1), name='Mes'))
     
    # Adjusting the 'Comisiones' array
    comisiones_adjusted = comisiones[1:]
    df_monthly_soft_costs['Comercialización'] = comisiones_adjusted

    # Subtotal
    total_row = df_monthly_soft_costs.sum(axis=1)
    total_row.name = 'Subtotal'
    df_monthly_soft_costs['Subtotal'] = total_row

    # Imprevistos
    df_monthly_soft_costs['Imprevisto'] = df_monthly_soft_costs['Subtotal'] * imprevistos_soft

    # IVA
    df_monthly_soft_costs['IVA'] = df_monthly_soft_costs['Subtotal'] * iva_soft_cost

    # Total
    df_monthly_soft_costs['Total'] = df_monthly_soft_costs['Subtotal'] + df_monthly_soft_costs['Imprevisto'] + df_monthly_soft_costs['IVA']

    # Format numbers with commas for thousands and millions
    #df_monthly_soft_costs = df_monthly_soft_costs.applymap(lambda x: f"${x:,.0f}" if isinstance(x, (int, float)) else x)

    # Transpose
    df_monthly_soft_costs = pd.DataFrame(df_monthly_soft_costs).T

    return df_monthly_soft_costs

#=====================================================================================================#
#=====================================================================================================#
#=====================================================================================================#

def calculate_project_cashflow(project_cost_id):
    
    project_cost = get_object_or_404(ProjectCost, id=project_cost_id)

    sales_pivot_table = calculate_apartment_payments(project_cost_id)
    sales = calculate_monthly_sums(sales_pivot_table).loc['Total Amount'].tolist()

    soft_table = calculate_soft_costs(project_cost_id)
    total_soft_cost = soft_table.loc['Total'].tolist()

    # Calculate total months between start and end dates
    total_months = (project_cost.fecha_fin_proyecto.year - project_cost.fecha_inicio_proyecto.year) * 12 + \
                   (project_cost.fecha_fin_proyecto.month - project_cost.fecha_inicio_proyecto.month)


    initial_balance = project_cost.caja_inicial

    
    # Calculating for 'Construcción' months using calculate_month_difference
    fecha_inicio_proyecto = project_cost.fecha_inicio_proyecto
    fecha_inicio_construccion = project_cost.fecha_inicio_construccion
    fecha_fin_construccion = project_cost.fecha_fin_construccion
    mes_inicio_construccion = calculate_month_difference(fecha_inicio_construccion, fecha_inicio_proyecto)
    mes_fin_construccion = calculate_month_difference(fecha_fin_construccion, fecha_inicio_proyecto)

    monthly_interest_rate = project_cost.tasa_interes / 12
    monthly_inflation = project_cost.inflacion / 12

    # Inputs for land cost calculation
    total_area = project_cost.superficie_terreno
    price_per_m2 = project_cost.costo_terreno

    # Calculate the cost of the land
    land_cost = total_area * price_per_m2

    # Hard cost per month (spread between construction start and end)
    hard_cost_months = mes_fin_construccion - mes_inicio_construccion + 1
    total_hard_cost = calculate_hard_costs(project_cost_id)
    hard_cost_per_month = total_hard_cost / hard_cost_months

    # Create lists to track sales, soft costs, hard costs, monthly expenses, balances, and loans
    soft_costs = []
    hard_costs = []
    interest_expenses = []
    expenses = []
    balances = [initial_balance]  # Add Month 0 with initial balance
    loans = [0]  # Add Month 0 loan amount
    total_loans = [0]  # Track total accumulated loans

    # Iterate through each month
    for month in range(1, total_months + 1):
        # Soft costs are incurred every month, adjusted for inflation
        monthly_soft_cost = total_soft_cost[month - 1]
        soft_costs.append(monthly_soft_cost)

        # Hard costs are incurred between month 10 and month 30, adjusted for inflation
        if mes_inicio_construccion  <= month <= mes_fin_construccion :
            monthly_hard_cost = hard_cost_per_month * (1 + monthly_inflation) ** month
        else:
            monthly_hard_cost = 0
        hard_costs.append(monthly_hard_cost)

        
        # Calculate interest expense based on the previous month's total loan accumulation
        monthly_interest_expense = total_loans[-1] * monthly_interest_rate
        interest_expenses.append(monthly_interest_expense)

        # Total expenses for the month including interest
        total_monthly_expense = monthly_soft_cost + monthly_hard_cost + monthly_interest_expense
        expenses.append(total_monthly_expense)

        # Calculate the balance including sales as income and subtracting expenses
        new_balance = balances[-1] + sales[month] - total_monthly_expense

        # Check if the balance goes negative
        if new_balance < initial_balance:
            loan_needed = initial_balance - new_balance
            loans.append(loan_needed)
            new_balance = initial_balance  # Set balance to at least initial balance
        else:
            loans.append(0)  # No loan needed

        # Check if the balance exceeds the initial balance for repayment
        if new_balance > initial_balance:
            repayment = min(new_balance - initial_balance, total_loans[-1])  # Repay only up to the loan amount
            loans[-1] -= repayment  # Repay the bank
            new_balance -= repayment  # Adjust the balance

        # Update the balance for the month
        balances.append(new_balance)

        # Calculate the total accumulated loan
        total_loans.append(total_loans[-1] + loans[-1])
    # Create a DataFrame where each month is a column
    df = pd.DataFrame({
        'Sales': sales,
        'Soft Cost': [0] + soft_costs,  # Include Month 0 soft costs
        'Hard Cost': [0] + hard_costs,  # Include Month 0 hard costs
        'Interest Expense': [0] + interest_expenses,  # Include Month 0 interest expenses
        'Total Expense': [0] + expenses,  # Include Month 0 expenses
        'Balance': balances,  # Include Month 0 balance
        'Loan': loans,  # Include Month 0 loan amount
        'Total Loan Accumulation': total_loans,  # Total accumulated loans
        'Land Cost': [land_cost] + [0] * total_months,  # Include land cost only in Month 0
    }, index=[f'Month {i}' for i in range(0, total_months + 1)])
    
    # Transpose the DataFrame to have months as columns
    df = df.transpose()

    return df

#=====================================================================================================#
#=====================================================================================================#
#=====================================================================================================#

def calculate_yearly_sums(flujo, months_per_year=12):

    index = ['Sales', 'Soft Cost', 'Hard Cost', 'Interest Expense', 'Total Expense','Land Cost']
    df = pd.DataFrame(flujo, index=index)
    
    # Get the number of months
    num_months = len(df.columns)
    
    # Create a dictionary to hold year mappings
    years = {0: ['Month 0']}  # Year 0 only has Month 0
    
    # Group remaining months into years
    for i in range(1, num_months):
        year = (i - 1) // 12 + 1  # Start grouping from Year 1
        if year not in years:
            years[year] = []
        years[year].append(f'Month {i}')
    
    # Initialize a dictionary to hold the yearly summary
    yearly_summary = {}
    
    # Iterate over the rows and aggregate by year
    for row in df.index:
        yearly_summary[row] = {}
        for year, months in years.items():
            yearly_summary[row][year] = df.loc[row, months].sum()
    
    # Convert the summary to a DataFrame
    summary_df = pd.DataFrame(yearly_summary).T
    
    # Calculate total across all years
    summary_df['Total'] = summary_df.sum(axis=1)

    # Format the DataFrame to money format
    summary_df = summary_df.apply(lambda x: x.map(lambda y: f"${y:,.0f}" if isinstance(y, (int, float)) else y))
    
    return summary_df

#=====================================================================================================#
#=====================================================================================================#
#=====================================================================================================#

def calculate_annual_irr(flujo):
    # Create a rank-1 array for Cashflow (Sales - Total Expense - Land Cost)
    cashflow = (flujo.loc['Sales'] - flujo.loc['Total Expense'] - flujo.loc['Land Cost']).values
    
    # Calculate the monthly IRR
    monthly_irr = npf.irr(cashflow)
    
    # Convert the monthly IRR to annual IRR
    annual_irr = (1 + monthly_irr) ** 12 - 1
    
    # Convert annual IRR to a percentage value
    annual_irr_percentage = round(annual_irr * 100, 2)
    
    # Create a DataFrame with the percentage value
    irr_df = pd.DataFrame({'Metric': ['Annual IRR'], 'Value (%)': [annual_irr_percentage]})
    
    return irr_df
#=====================================================================================================#
#=====================================================================================================#
#=====================================================================================================#

def save_analysis_to_excel(pivot_table, soft_cost, df, yearly_summary_df, irr):
    """
    Saves the given DataFrames to an Excel file with three sheets: 'Ingresos', 'Flujo', and 'Proforma'.
    If the file already exists, it appends the new sheets to the existing file.
    
    Args:
        pivot_table (pd.DataFrame): DataFrame containing pivot table data.
        df (pd.DataFrame): DataFrame containing the cash flow data.
        yearly_summary_df (pd.DataFrame): DataFrame containing the yearly summary data.
    """
    # Get the current date and time
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'Analisis_inmobiliario_{current_time}.xlsx'

    # Check if the file exists
        # Check if the file exists
    if os.path.exists(output_file):
        # Load the existing Excel file and append new worksheets
        with pd.ExcelWriter(output_file, engine='openpyxl', mode='a') as writer:
            pivot_table.to_excel(writer, sheet_name='Ingresos')  # First sheet
            soft_cost.to_excel(writer, sheet_name='SoftCost')  # First sheet
            df.style.to_excel(writer, sheet_name='Flujo')              # Second sheet
            yearly_summary_df.to_excel(writer, sheet_name='Proforma')  # Third sheet
            irr.to_excel(writer, sheet_name='Indicadores', index=False)  #Fourth sheet
            
    else:
        # Create a new Excel file and add the sheets
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            pivot_table.to_excel(writer, sheet_name='Ingresos')  # First sheet
            soft_cost.to_excel(writer, sheet_name='SoftCost')  # First sheet
            df.style.to_excel(writer, sheet_name='Flujo')              # Second sheet
            yearly_summary_df.to_excel(writer, sheet_name='Proforma')  # Third sheet
            irr.to_excel(writer, sheet_name='Indicadores', index=False)  #Fourth sheet

#=====================================================================================================#
#=====================================================================================================#
#=====================================================================================================#


# Function to calculate month difference
def calculate_month_difference(start_date, reference_date):
    delta = relativedelta(start_date, reference_date)
    return delta.years * 12 + delta.months