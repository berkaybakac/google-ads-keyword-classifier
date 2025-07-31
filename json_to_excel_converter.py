import json
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
import os

def create_styled_excel(json_data, sheet_name, wb):
    """Verilen JSON verisini belirtilen sayfaya stilize bir şekilde yazar."""
    
    # JSON verisini DataFrame'e dönüştür
    df = pd.DataFrame(json_data)
    
    # Excel'e yaz
    if sheet_name in wb.sheetnames:
        del wb[sheet_name]
    ws = wb.create_sheet(sheet_name)
    
    # Başlıkları yaz
    headers = list(df.columns)
    ws.append(headers)
    
    # Verileri yaz
    for _, row in df.iterrows():
        ws.append(list(row))
        
    # Stil tanımları
    header_font = Font(bold=True, color="FFFFFF", size=12)
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center")
    cell_alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    thin_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )
    
    # Explanation sütun indexini bul
    explanation_col_idx = None
    if 'explanation' in headers:
        explanation_col_idx = headers.index('explanation') + 1
    
    # Başlık stilini uygula
    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
        cell.border = thin_border
    
    # Veri hücrelerini stillendir
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
        for cell in row:
            cell.alignment = cell_alignment
            cell.border = thin_border
    
    # Sütun genişliklerini ayarla
    for col_idx, col_name in enumerate(headers, 1):
        col_letter = get_column_letter(col_idx)
        
        if col_idx == explanation_col_idx:
            ws.column_dimensions[col_letter].width = 80
        else:
            max_length = 0
            for row_cell in ws[col_letter]:
                if row_cell.value:
                    length = len(str(row_cell.value))
                    if length > max_length:
                        max_length = length
            
            adjusted_width = min(max(max_length + 2, 12), 30)
            ws.column_dimensions[col_letter].width = adjusted_width
    
    # Satır yüksekliklerini ayarla
    ws.row_dimensions[1].height = 25
    
    for row_idx in range(2, ws.max_row + 1):
        if explanation_col_idx:
            explanation_cell = ws.cell(row=row_idx, column=explanation_col_idx)
            if explanation_cell.value:
                text_length = len(str(explanation_cell.value))
                lines = max(1, text_length // 80)
                height = max(30, min(lines * 18, 120))
                ws.row_dimensions[row_idx].height = height
            else:
                ws.row_dimensions[row_idx].height = 25
        else:
            ws.row_dimensions[row_idx].height = 25
    
    # Otomatik filtre ekle
    if ws.max_row > 1:
        ws.auto_filter.ref = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"

def main():
    """İki JSON dosyasını işleyerek tek bir Excel'de iki ayrı sayfa oluşturur."""
    
    json_files = [
        ("04_ai_output_sample.json", "30_Keywords_Report"),
        ("04_ai_output_sample_2.json", "50_Keywords_Report")
    ]
    
    output_excel_path = "gelismis_output.xlsx"
    
    # Yeni bir Excel çalışma kitabı oluştur
    wb = load_workbook(output_excel_path)
    # Varsayılan sayfayı sil
    if "Sheet" in wb.sheetnames:
        del wb["Sheet"]
        
    for json_file, sheet_name in json_files:
        json_file_path = os.path.join("prompts", json_file)
        
        try:
            if not os.path.exists(json_file_path):
                print(f"Hata: JSON dosyası bulunamadı: {json_file_path}")
                continue
                
            with open(json_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            results = data.get("results", [])
            
            if not results:
                print(f"Uyarı: {json_file_path} dosyasında 'results' listesi boş.")
                continue
            
            create_styled_excel(results, sheet_name, wb)
            print(f"'{sheet_name}' sayfası başarıyla oluşturuldu ve stilize edildi.")
            
        except Exception as e:
            print(f"'{json_file}' işlenirken bir hata oluştu: {e}")
            
    # Son halini kaydet
    wb.save(output_excel_path)
    print(f"\nExcel dosyası oluşturuldu: {output_excel_path}")

if __name__ == "__main__":
    main()