import csv

def fetch_case_data(case_type, case_number, filing_year):
    try:
        with open('data.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if (
                    row['case_type'].strip().lower() == case_type.strip().lower() and
                    row['case_number'].strip() == case_number.strip() and
                    row['filing_year'].strip() == filing_year.strip()
                ):
                    return {
                        'parties': row['parties'],
                        'filing_date': row['filing_date'],
                        'next_hearing': row['next_hearing'],
                        'order_link': row['order_link']
                    }
    except FileNotFoundError:
        return {
            'parties': '❌ Error: data.csv not found',
            'filing_date': '-',
            'next_hearing': '-',
            'order_link': '#'
        }

    # Case not found
    return {
        'parties': '⚠️ Case not found in the database',
        'filing_date': '-',
        'next_hearing': '-',
        'order_link': '#'
    }
def get_case_by_id(case_id):
    try:
        with open('data.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cid = f"{row['case_type'].strip()}_{row['case_number'].strip()}_{row['filing_year'].strip()}"
                if cid == case_id:
                    return {
                        'case_type': row['case_type'],
                        'case_number': row['case_number'],
                        'filing_year': row['filing_year'],
                        'parties': row['parties'],
                        'filing_date': row['filing_date'],
                        'next_hearing': row['next_hearing']
                    }
    except:
        return None
