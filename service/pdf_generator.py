import os
from fpdf import FPDF


class BookingInvoice(FPDF):
    def __init__(self):
        super().__init__()
        current_dir = os.path.dirname(__file__)
        fonts_dir = os.path.join(current_dir, 'static', 'service', 'fonts')

        regular_font = os.path.join(fonts_dir, 'Montserrat-Regular.ttf')
        bold_font = os.path.join(fonts_dir, 'Montserrat-Bold.ttf')

        try:
            self.add_font('Montserrat', '', regular_font, uni=True)
            self.add_font('Montserrat', 'B', bold_font, uni=True)
        except FileNotFoundError as e:
            raise e

    def header(self):
        self.set_fill_color(250, 249, 244)
        self.rect(0, 0, 210, 297, 'F')

    def create_invoice(self, data):
        self.add_page()

        self.set_y(15)
        self.set_font("Montserrat", "B", 45)
        self.set_text_color(0, 0, 0)
        self.cell(95, 20, "Invoice", ln=False)


        self.set_font("Montserrat", "", 12)
        self.set_text_color(100, 100, 100)
        self.cell(95, 20, f"Order ID: {data['booking_id']}", align='R', ln=True)

        self.ln(20)

        self.set_font("Montserrat", "B", 10)
        self.set_text_color(150, 150, 150)
        self.cell(0, 6, "BILLED TO", ln=True)

        self.set_font("Montserrat", "", 16)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, data['username'], ln=True)

        self.ln(15)

        self.set_draw_color(0, 0, 0)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(10)

        self.set_font("Montserrat", "B", 14)
        self.cell(0, 8, data['room_name'], ln=True)

        self.set_font("Montserrat", "", 10)
        self.set_text_color(80, 80, 80)
        self.cell(0, 6, data['room_address'], ln=True)

        self.ln(8)

        self.set_font("Montserrat", "", 11)
        self.set_text_color(0, 0, 0)

        self.cell(35, 8, "Capacity:", ln=False)
        self.cell(0, 8, str(data['room_capacity']), ln=True)

        self.cell(35, 8, "Date Range:", ln=False)
        self.cell(0, 8, data['date_period'], ln=True)

        self.ln(10)

        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(10)

        self.set_y(self.get_y() + 5)

        self.set_font("Montserrat", "", 12)
        self.cell(140, 10, "Total Due", align='R')

        self.set_font("Montserrat", "B", 20)
        self.cell(50, 10, str(data['total_price']), align='R', ln=True)