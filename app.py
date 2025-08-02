from flask import Flask, render_template, request, send_file
from court_scraper import fetch_case_data, get_case_by_id
from database import init_db, log_query
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Initialize SQLite DB
init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    case = None
    show_result = False

    if request.method == 'POST':
        case_type = request.form['case_type'].strip()
        case_number = request.form['case_number'].strip()
        filing_year = request.form['filing_year'].strip()

        case = fetch_case_data(case_type, case_number, filing_year)

        
        if case:
            case['case_type'] = case_type
            case['case_number'] = case_number
            case['filing_year'] = filing_year

        log_query(case_type, case_number, filing_year, str(case))
        show_result = True

    return render_template('index.html', case=case, show_result=show_result)


@app.route('/download/<case_id>')
def download_pdf(case_id):
    case = get_case_by_id(case_id)
    if not case:
        return "Case not found", 404

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 12)

    p.drawString(50, 750, f"Parties: {case['parties']}")
    p.drawString(50, 730, f"Filing Date: {case['filing_date']}")
    p.drawString(50, 710, f"Next Hearing: {case['next_hearing']}")
    p.drawString(50, 690, f"Case Type: {case['case_type']}, Case Number: {case['case_number']}, Year: {case['filing_year']}")

    p.showPage()
    p.save()
    buffer.seek(0)

    filename = f"{case_id}_order.pdf"
    return send_file(buffer, as_attachment=True, download_name=filename, mimetype='application/pdf')


if __name__ == '__main__':
    app.run(debug=True)
