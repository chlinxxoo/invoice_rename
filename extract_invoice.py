import argparse
import os
import re
import sys
import pdfplumber
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    """
    从PDF文件中提取文本
    :param pdf_path: PDF文件路径
    :return: 提取的文本内容
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += (page.extract_text() or "")
            return text.strip()
    except Exception as e:
        print(f"处理文件 {pdf_path} 时发生错误: {str(e)}")
        return None

def process_pdf_directory(directory_path, dumpTxt, dumpTotalCount):
    """
    处理指定目录下的所有PDF文件
    :param directory_path: PDF文件所在目录
    """
    directory = Path(directory_path)
    
    # 确保输出目录存在
    output_dir = directory / "txt"
    output_dir.mkdir(exist_ok=True)

    totalCount = 0
    
    # 处理所有PDF文件
    pdf_files = list(directory.glob("*.pdf"))
    if not pdf_files:
        print(f"在目录 {directory_path} 中没有找到PDF文件")
        if getattr(sys, 'frozen', False):
            input("按回车键退出...")
        return

    for pdf_file in pdf_files:
        print(f"正在处理: {pdf_file.name}")
        
        # 提取文本
        text_content = extract_text_from_pdf(pdf_file)
        
        if text_content:
            invoice_number = None
            invoice_date = None
            invoice_company = None
            invoice_amount = None
            detail_name = None
            isDetail = False
            for line in text_content.split('\n'):
                if isDetail == False:
                    m = re.match(r'.*税\s*额', line)
                    if m:
                        isDetail = True
                        continue
                else:
                    m = re.search(r'\*[^\s]*\*([^\s]+)', line)
                    if m:
                        detail_name = m.group(1).replace(" ", "")
                    isDetail = False
                    continue

                if invoice_number == None:
                    m = re.search(r'.*发票号码[:：]\s*(.*)', line)
                    if m:
                        invoice_number = m.group(1).replace(" ", "")
                    continue

                if invoice_date == None:
                    m = re.search(r'.*开票日期[:：]\s*(.*)', line)
                    if m:
                        invoice_date = m.group(1).replace(" ", "")
                        continue

                
                if invoice_company == None:
                    m = re.search(r'.*?名\s*称[:：]\s*(.*?公司)', line)
                    if m:
                        invoice_company = m.group(1).replace(" ", "")
                    continue

                if invoice_amount == None:
                    m = re.search(r'.*[(（]小写[)）]\s*[¥￥]\s*(.*)', line)
                    if m:
                        invoice_amount = m.group(1).replace(" ", "")
                        totalCount += float(invoice_amount)
                    continue

            
            # 根据发票信息构建新文件名
            if invoice_number and invoice_date and invoice_amount and invoice_company:
                # 提取年月日
                # print(invoice_date)
                match = re.search(r'.*(\d{4})年\s*(\d{2})月\s*(\d{2})日.*', invoice_date)
                if match:
                    year, month, day = match.groups()
                else:
                    year, month, day = invoice_date[:4], invoice_date[5:7], invoice_date[8:10]
                
                # 构建新文件名 格式: 公司名-年月日-类型-金额.pdf
                new_name = f"{invoice_number}-{invoice_company}-{year}{month}{day}-{detail_name if detail_name else '【类别获取失败】'}-{invoice_amount}.pdf"
                
                # 获取目标路径
                target_path = pdf_file.parent / new_name
                
                try:
                    # 重命名文件
                    pdf_file.rename(target_path)
                    # print(f"文件已重命名为: {new_name}")
                except Exception as e:
                    print(f"重命名失败: {str(e)}")
            else:
                print(f"无法重命名文件 {pdf_file.name}: 缺少必要信息", invoice_number, invoice_date, invoice_amount, invoice_company)
                dumpTxt = True

            if dumpTxt:
                # 将提取的文本内容保存到txt文件
                extracted_text_dir = pdf_file.parent / "txt"
                extracted_text_dir.mkdir(exist_ok=True)
                
                # 使用相同的文件名(不含扩展名)创建txt文件
                txt_file = extracted_text_dir / f"{pdf_file.stem}.txt"
                try:
                    with open(txt_file, "w", encoding="utf-8") as f:
                        f.write(text_content)
                    print(f"文本内容已保存到: {txt_file}")
                except Exception as e:
                    print(f"保存文本内容失败: {str(e)}")
        else:
            print(f"无法从 {pdf_file.name} 提取文本")

    if dumpTotalCount and totalCount > 0:
        # 将汇总金额写入文件
        print(f"汇总金额: {totalCount}")
        try:
            amount_file = directory / f"{totalCount:.2f}.txt"
            with open(amount_file, "w", encoding="utf-8") as f:
                f.write(f"汇总金额: {totalCount}")
            print(f"汇总金额已保存到: {amount_file}")
        except Exception as e:
            print(f"保存汇总金额失败: {str(e)}")

    # 如果是打包后的可执行文件，等待用户按键后退出
    if getattr(sys, 'frozen', False):
        input("按回车键退出...")

if __name__ == "__main__":
    # 获取程序运行路径
    if getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件
        app_path = os.path.dirname(sys.executable)
    else:
        # 如果是Python脚本
        app_path = os.path.dirname(os.path.abspath(__file__))

    parser = argparse.ArgumentParser(description='发票处理工具')
    parser.add_argument('--pdfFolder', action="store", dest="pdfFolder", help='发票文件夹路径')
    parser.add_argument('--dumpTxt', action="store_true", dest="dumpTxt", help='文本全输出')
    parser.add_argument('--dumpTotalCount', action="store_true", dest="dumpTotalCount", help='汇总金额')

    # 解析命令行参数
    if len(sys.argv) > 1:
        results = parser.parse_args()
        pdf_folder = results.pdfFolder
        dump_txt = results.dumpTxt
        dump_total = results.dumpTotalCount
    else:
        # 如果没有参数，使用默认值
        pdf_folder = app_path
        dump_txt = False
        dump_total = True

    print(f"发票文件夹路径: {pdf_folder}")
    print("开始处理PDF文件...")
    process_pdf_directory(pdf_folder, dump_txt, dump_total)
    print("处理完成！") 