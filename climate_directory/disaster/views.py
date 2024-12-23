from django.shortcuts import render
from openpyxl import load_workbook

def get_disaster_data(request):
    data = None
    error = None

    if request.method == "POST":
        country_name = request.POST.get('country', '').strip()
        filename = r"D:\Natural_disaster\natural_disaster\Disaster_datas.xlsx"
        disno_column = 'DisNo.'  # Column header for DisNo.

        try:
            # Load the workbook
            book = load_workbook(filename)
            sheet = book.active

            # Get headers from the first row
            headers = [cell.value for cell in sheet[1]]  # Assuming headers are in the first row
            results = []

            # Search for rows matching the country
            for row in sheet.iter_rows(min_row=2, values_only=True):  # Skip headers
                row_data = dict(zip(headers, row))
                if row_data.get('Country') == country_name:  # Match the country column
                    results.append(row_data)

            # Sort results by the numerical prefix of DisNo.
            if results and disno_column in headers:
                try:
                    results.sort(
                        key=lambda x: int(x.get(disno_column, '').split('-')[0]) if x.get(disno_column) else 0,
                        reverse=True
                    )
                except Exception as e:
                    error = f"Error during sorting by DisNo.: {str(e)}"

            if results:
                data = results
            else:
                error = f"No disaster data found for country: {country_name}"

        except FileNotFoundError:
            error = f"File not found: {filename}. Please ensure the file path is correct."
        except Exception as e:
            error = f"An unexpected error occurred: {str(e)}"

    return render(request, 'get_disaster_data.html', {'data': data, 'error': error})
