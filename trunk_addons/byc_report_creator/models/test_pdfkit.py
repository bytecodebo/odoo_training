import pdfkit


if __name__ == '__main__':
    # pdf =
    # pdfkit.from_string(result_html, file_store, options=options, css=css)
    pdfkit.from_url('http://localhost:9069/my/invoices/5669',
                    'invoice.pdf')