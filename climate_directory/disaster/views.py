from django.shortcuts import render
from django.http import HttpResponse
from openpyxl import load_workbook

def get_disaster_data(request):
    data = None
    error = None

    if request.method == "POST":
        country_name = request.POST.get('country', '').strip()  # Changed to country
        filename = r"D:\Natural_disaster\natural_disaster\Disaster_datas.xlsx"  # Specify the correct path and filename
        country_column = 'Country'  # Column header for country

        try:
            # Try loading the workbook
            book = load_workbook(filename)
            sheet = book.active

            # Get headers from the first row
            headers = [cell.value for cell in sheet[1]]  # Assuming headers are in the first row
            results = []

            # Search for rows matching the country
            for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip headers
                row_data = dict(zip(headers, row))
                if row_data.get(country_column) == country_name:
                    results.append(row_data)

            if results:
                data = results
            else:
                error = f"No disaster data found for country: {country_name}"

        except FileNotFoundError:
            error = f"File not found: {filename}. Please ensure the file path is correct."
        except ValueError:
            error = f"The file format is not supported. Please upload a valid Excel file (.xlsx, .xlsm, .xltx)."
        except Exception as e:
            error = f"An unexpected error occurred: {str(e)}"

    return render(request, 'get_disaster_data.html', {'data': data, 'error': error})
