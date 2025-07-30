import json
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
import os

def create_styled_excel(json_file_path, output_path="output.xlsx"):
    try:
        if not os.path.exists(json_file_path):
            raise FileNotFoundError(f"JSON dosyası bulunamadı: {json_file_path}")
            
        with open(json_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        results = data.get("results", [])
        
        if not results:
            print("Uyarı: JSON dosyasında 'results' listesi boş.")
            return
        
        df = pd.DataFrame(results)
        df.to_excel(output_path, index=False, engine='openpyxl')
        
        wb = load_workbook(output_path)
        ws = wb.active
        
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
        explanation_col = None
        for col_idx, cell in enumerate(ws[1], 1):
            if cell.value and 'explanation' in str(cell.value).lower():
                explanation_col = col_idx
                break
        
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
        for col_idx in range(1, ws.max_column + 1):
            col_letter = get_column_letter(col_idx)
            
            if col_idx == explanation_col:
                ws.column_dimensions[col_letter].width = 80
            else:
                max_length = 0
                for row in ws.iter_rows(min_col=col_idx, max_col=col_idx):
                    for cell in row:
                        if cell.value:
                            length = len(str(cell.value))
                            if length > max_length:
                                max_length = length
                
                adjusted_width = min(max(max_length + 2, 12), 25)
                ws.column_dimensions[col_letter].width = adjusted_width
        
        # Satır yüksekliklerini ayarla
        ws.row_dimensions[1].height = 25
        
        for row_idx in range(2, ws.max_row + 1):
            if explanation_col:
                explanation_cell = ws.cell(row=row_idx, column=explanation_col)
                if explanation_cell.value:
                    text_length = len(str(explanation_cell.value))
                    lines = max(1, text_length // 80)
                    height = max(30, min(lines * 18, 120))
                    ws.row_dimensions[row_idx].height = height
                else:
                    ws.row_dimensions[row_idx].height = 25
            else:
                ws.row_dimensions[row_idx].height = 25
        
        ws.title = "Veri Raporu"
        
        if ws.max_row > 1:
            ws.auto_filter.ref = f"A1:{get_column_letter(ws.max_column)}{ws.max_row}"
        
        wb.save(output_path)
        print(f"Excel dosyası oluşturuldu: {output_path}")
        print(f"Toplam {len(results)} satır ve {len(df.columns)} sütun işlendi")
        
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    create_styled_excel("prompts/04_ai_output_sample.json", "gelismis_output.xlsx")