import xlsxwriter
from datetime import datetime

def generate_xlsx(address:str, number:str, items:dict):
    workbook = xlsxwriter.Workbook("base.xlsx")
    worksheet = workbook.add_worksheet()

    # set column width and default row height
    worksheet.set_default_row(23)
    worksheet.set_column(0,0,4)
    worksheet.set_column(1,1,40)
    worksheet.set_column(2,4,15)
    
    # header
    worksheet.insert_image(1,0,"fenzerpro.png")
    worksheet.write(1,1, "          บริษัท สตาร์ป๊อป จำกัด",)
    worksheet.write(2,1, "          45/2 หมู่ 3 ถนนคุ้มเกล้า แขวงลำปลาทิว เขตลาดกระบัง กทม. 10520",)
    worksheet.write(3,1, "          โทร.089 666 4525  086 319 0309 แฟกซ์ 02-360-6391",)

    # merge A5 - E5, bold, underline, center align
    a5e5 = workbook.add_format({
        'bold':1,
        'underline':1,
        'top':1,
        'align': 'center',
    })
    worksheet.merge_range(4,0,4,4,"ใบเสนอราคา", a5e5)

    # date
    day, month, year = datetime.now().day, datetime.now().month, datetime.now().year
    thai_month = {1:"มกราคม", 2:"กุมภาพันธ์", 3:"มีนาคม", 4:"เมษายน", 5:"พฤษภาคม", 6:"มิถุนายน", 7:"กรกฎาคม", 8:"สิงหาคม", 9:"กันยายน", 10: "ตุลาคม", 11:"พฤศจิกายน", 12:"ธันวาคม"}
    # in case the month is somehow not in the dict:
    try:
        current_date = format(f"วันที่ {day} {thai_month[month]} {year + 543}")
    except:
        print("Month is somehow not in range 1-12")
        current_date = ""
    finally:
        worksheet.write(6,3,current_date)

    # number
    worksheet.write(7,3, format(f"เลขที่ {number}"))

    # address
    current_line = 6
    split_address = address.split("\n")
    for line in split_address:
        worksheet.write(current_line, 1, line)
        current_line += 1
    current_line += 1

    # item list header
    worksheet.set_row(current_line,45)
    border_c_align = workbook.add_format({
        'border':1,
        'align':'center',
    })
    list_header = ("ลำดับ", "รายการสินค้า", "ราคาต่อชิ้น\n(บาท)", "จำนวน(ชิ้น)", "จำนวนเงิน(บาท)")
    for column in range(len(list_header)):
        worksheet.write(current_line,column, list_header[column], border_c_align)
    current_line += 1

    # 1 line between header and items
    side_border = workbook.add_format({
        'left':1,
        'right':1
    })
    for column in range(5):
        worksheet.write(current_line,column,"",side_border)
    current_line += 1

    # item list items
    item_order = 1
    total_cost = 0
    for item in items:\
        # a row consists of (the item's order on the list, item name, item price, item amount, total cost)
        row = (item_order, item, "PLACEHOLDER PRICE", items[item], "PLACEHOLDER TOTAL")
        for column in range(len(row)):
            worksheet.write(current_line, column, row[column], side_border)
        item_order, current_line = item_order + 1, current_line + 1

    # bottom of the item list
    bottom_border = workbook.add_format({
        'left':1,
        'right':1,
        'bottom': 1
    })
    for column in range(5):
        worksheet.write(current_line,column,"",bottom_border)
    current_line += 1

    # bottom of the quotation
    bottom_rows = (("***ขนส่งด้วย 10ล้อ เท่านั้น***", "รวมเงิน", total_cost),
                   ("***ไม่รับคืนหรือเปลี่ยนสินค้า***", "จำนวนภาษีมูลค่าเพิ่ม 7%", round(total_cost*(0.07), 2)),
                   ("***ชำระเงินก่อนส่งสินค้า 3-5วัน***", "จำนวนเงินรวมภาษีมูลค่าเพิ่ม", round(total_cost*(1.07), 2)))
    for row in bottom_rows:
        worksheet.write(current_line, 1, row[0])
        worksheet.merge_range(current_line, 2, current_line, 3, row[1], border_c_align)
        worksheet.write(current_line, 4, row[2], border_c_align)
        current_line += 1
    worksheet.write(current_line, 1, "***ราคาอาจเปลี่ยนแปลง ตามต้นทุนสินค้าที่ไม่ทราบล่วงหน้า***")
    current_line += 1
    border_c_align_bold = workbook.add_format({
        'border':1,
        'align':'center',
        'bold':1
    })
    worksheet.merge_range(current_line,2,current_line,4,format(f"=BAHTTEXT(E{current_line-1})"),border_c_align_bold)
    current_line += 1
    worksheet.write(current_line,1,"ยืนยันการสั่งซื้อ")
    current_line += 1
    c_align = workbook.add_format({'align':'center'})
    worksheet.merge_range(current_line,2,current_line,4,"ลงชื่อ ..................................... ผู้เสนอราคา", c_align)
    current_line += 1
    worksheet.write(current_line,1, "............................")
    worksheet.merge_range(current_line,2,current_line,4,"(นิลุบล เรืองทอง)", c_align)
    current_line +=1
    worksheet.write(current_line,1, "(                       )")
     

    print(current_line)
    workbook.close()

customer_address = "หน่วยงาน เฉลิมพระเกียรติ\nบริษัท ดินเทคซ์ เอ.จี.จำกัด\n48/1741 ถ.เอกชัย ต.คอกกระบือ อ.เมืองสมุทรสาคร\nจ.สมุทรสาคร 74000"
items ={"เสารั้วI15*15*2.28ม. สำหรับรั้วสูงไม่เกิน 2.0ม.": 17, "ฟุตติ้ง 0.35*0.7*0.30 ม.":15, "แผ่นรั้วรุ่นPRO เรียบ":104, "ทับหลัง C":13, "เสาเข็มI15-4ม.":30, "ค่าแรงติดตั้ง":1500}
generate_xlsx(customer_address, "660922-06", items)