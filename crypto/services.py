import xlsxwriter
from django.http import HttpResponse
import io


def get_address(country, city, province, zip_code, line_1, line_2):
    address = ''
    if line_1:
        address = address + line_1
    if line_2:
        address = address + ', ' + line_2
    if zip_code:
        address = address + ', ' + zip_code
    if province:
        address = address + ', ' + province

    if city:
        address = address + ', ' + city
    if country:
        address = address + ', ' + country

    return address


def create_excel_receipt(receipt):
    output = io.BytesIO()
    file_name = f'{receipt.first_name} {receipt.last_name} {receipt.created.date()}.xlsx'
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    home_address = get_address(receipt.home_country,
                               receipt.home_city,
                               receipt.home_province,
                               receipt.home_zip,
                               receipt.home_address1,
                               receipt.home_address2)
    business_address = get_address(receipt.business_country,
                                   receipt.business_city,
                                   receipt.business_province,
                                   receipt.business_zip,
                                   receipt.business_address1,
                                   receipt.business_address2)

    bold = {'bold': True}
    date_format = {'num_format': 'mm/dd/yy'}
    bg_blue = {'fg_color': '#6495ed'}
    wt = {'text_wrap': True}
    header_cells_style = {
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 20}
    common_cells_style = {
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 14}

    worksheet.set_column('A:A', 25)
    worksheet.set_column('B:B', 50)
    line_index = 0
    '''Company Details'''
    # company name
    if receipt.company:
        line_index += 1
        worksheet.merge_range(f'A{line_index}:B{line_index}', receipt.company,
                              workbook.add_format(dict(header_cells_style, **bold)))
    # company address
    if business_address:
        worksheet.set_row(line_index, 45)
        line_index += 1
        worksheet.merge_range(f'A{line_index}:B{line_index}', business_address,
                              workbook.add_format(dict(header_cells_style, **wt)))
    # company ID
    if receipt.company_id:
        line_index += 1

        worksheet.write(f'A{line_index}', 'Company ID:',
                        workbook.add_format(dict(common_cells_style, **bg_blue)))

        worksheet.write(f'B{line_index}', receipt.company_id,
                        workbook.add_format(common_cells_style))
    # company receipt reference
    if receipt.receipt_reference:
        line_index += 1

        worksheet.write(f'A{line_index}', 'Receipt Reference:',
                        workbook.add_format(dict(common_cells_style, **bg_blue)))
        worksheet.write(f'B{line_index}', receipt.receipt_reference,
                        workbook.add_format(common_cells_style))

    '''Payee details'''
    # Payee's full name
    if receipt.first_name and receipt.last_name:
        line_index += 1

        worksheet.write(f'A{line_index}', 'Payee:',
                        workbook.add_format(dict(common_cells_style, **bg_blue)))
        worksheet.write(f'B{line_index}', f'{receipt.first_name} {receipt.last_name}',
                        workbook.add_format(common_cells_style))
    # Payee's national id
    if receipt.national_id:
        line_index += 1

        worksheet.write(f'A{line_index}', 'National ID:',
                        workbook.add_format(dict(common_cells_style, **bg_blue)))
        worksheet.write(f'B{line_index}', receipt.national_id,
                        workbook.add_format(common_cells_style))
    # Payee's taxpayer id
    if receipt.taxpayer_id:
        line_index += 1

        worksheet.write(f'A{line_index}', 'Tax Payer ID:',
                        workbook.add_format(dict(common_cells_style, **bg_blue)))
        worksheet.write(f'B{line_index}', receipt.taxpayer_id,
                        workbook.add_format(common_cells_style))
    # home address
    if home_address:
        worksheet.set_row(line_index, 40)
        line_index += 1
        worksheet.write(f'A{line_index}', 'Home address:',
                        workbook.add_format(dict(common_cells_style, **bg_blue)))
        worksheet.write(f'B{line_index}', home_address,
                        workbook.add_format(dict(common_cells_style, **wt)))
    # Payee's BTC address
    if receipt.btc_address:
        line_index += 1

        worksheet.write(f'A{line_index}', 'BTC address:',
                        workbook.add_format(dict(common_cells_style, **bg_blue)))
        worksheet.write(f'B{line_index}', receipt.btc_address,
                        workbook.add_format(common_cells_style))

    '''Transaction Details'''
    # 5th row, amount in USD
    if receipt.payment_amount and receipt.payment_currency:
        line_index += 1

        worksheet.write(f'A{line_index}', f'Amount in {receipt.payment_currency}:',
                        workbook.add_format(dict(common_cells_style, **bg_blue)))
        worksheet.write(f'B{line_index}', receipt.payment_amount,
                        workbook.add_format(common_cells_style))
    # 6th row, amount in BTC
    if receipt.btc_amount:
        line_index += 1

        worksheet.write(f'A{line_index}', 'Amount in BTC:',
                        workbook.add_format(dict(common_cells_style, **bg_blue)))
        worksheet.write(f'B{line_index}', receipt.btc_amount,
                        workbook.add_format(common_cells_style))

    # transaction date
    if receipt.created:
        line_index += 1

        worksheet.write(f'A{line_index}', 'Date of emission:',
                        workbook.add_format(dict(common_cells_style, **bg_blue)))
        worksheet.write(f'B{line_index}', receipt.created.strftime("%m/%d/%Y"),
                        workbook.add_format(dict(date_format, **common_cells_style)))

    workbook.close()
    output.seek(0)

    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % file_name

    return response
