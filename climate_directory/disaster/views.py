from django.shortcuts import render
from openpyxl import load_workbook

def get_disaster_data(request):
    data = None
    error = None

    if request.method == "POST":
        country_name = request.POST.get('country', '').strip()
        start_year = request.POST.get('start_year', '').strip()
        end_year = request.POST.get('end_year', '').strip()
        filename = r"D:\Natural_disaster\natural_disaster\Disaster_datas.xlsx"
        country_column = 'Country'
        disno_column = 'DisNo.'

        try:
            # Load the workbook
            book = load_workbook(filename)
            sheet = book.active

            # Get headers from the first row
            headers = [cell.value for cell in sheet[1]]
            results = []

            # Search for rows matching the country and time filter
            for row in sheet.iter_rows(min_row=2, values_only=True):
                row_data = dict(zip(headers, row))

                # Extract the year from the "DisNo." column
                disno = row_data.get(disno_column, '')
                year = disno.split('-')[0] if disno else None

                if (
                    row_data.get(country_column) == country_name and
                    (not start_year or (year and year >= start_year)) and
                    (not end_year or (year and year <= end_year))
                ):
                    results.append(row_data)

            if results:
                # Sort results by year (descending)
                results.sort(key=lambda x: x.get(disno_column, ''), reverse=True)
                data = results
            else:
                error = f"No disaster data found for {country_name} in the specified time range."

        except FileNotFoundError:
            error = f"File not found: {filename}. Please ensure the file path is correct."
        except Exception as e:
            error = f"An unexpected error occurred: {str(e)}"

    return render(request, 'get_disaster_data.html', {'data': data, 'error': error})
