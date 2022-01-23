import os
import calculations
import pdf_data
import excel_file
import user_inputs


for f in os.listdir(user_inputs.input_file_path):
    if f.endswith('.pdf'):
        # saves the customer name as a variable
        customer_name = pdf_data.get_customer_name(f)

        # saves the invoice number as a variable
        invoice_number = pdf_data.get_invoice_number(f)

        # uses the PDF in the input file to get the USD value listed on the invoice
        usd_value = pdf_data.get_usd_value(f)

        # calls function to calculate numbers to write on AP invoice
        full_usd_amount_rounded = calculations.calculate_usd_total(usd_value)
        commission_amount = calculations.calculate_commission_total(full_usd_amount_rounded, usd_value)

        # this adds commas to the number for user readability.  This number should be what is written on invoice for AP
        full_amt_to_code = f"{full_usd_amount_rounded:,}"
        commission_to_code = f"{commission_amount:,}"

        # check if customer name is included on the list of customers exempt from the 2% sales rule
        if customer_name.lower() in user_inputs.commission_exceptions:
            # the coding that needs to be written on the invoice for 206700
            coding_text_1 = f"206700: {usd_value}"
            # writes the coding to a new PDF in the output files location
            pdf_data.write_to_pdf(f, coding_text_1)
        else:
            # the coding that needs to be written on the invoice for 206700
            coding_text_1 = f"206700: {full_amt_to_code}"
            # the coding that needs to be written on the invoice for commissions
            coding_text_2 = f"600600-8888: {commission_to_code}"
            # writes the coding to a new PDF in the output files location
            pdf_data.write_to_pdf(f, coding_text_1, coding_text_2)

        # creates a csv file with the list of invoices and other information
        excel_file.create_csv(invoice_number, customer_name, usd_value, user_inputs.output_file_path)


print('Task Completed')
