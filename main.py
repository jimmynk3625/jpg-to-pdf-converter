from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
import os
from pathlib import Path
import shutil
from typing import List
import tempfile

app = FastAPI()

# 建立暫存資料夾
TEMP_DIR = Path("temp_files")
TEMP_DIR.mkdir(exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """提供首頁 HTML"""
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.head("/")
def root():
    return {"status": "ok"}

@app.post("/convert")
async def convert_images_to_pdf(files: List[UploadFile] = File(...)):
    """
    接收多個圖片檔案並轉換為 PDF
    """
    try:
        # 檢查是否有上傳檔案
        if not files:
            return {"error": "沒有上傳任何檔案"}
        
        # 暫存上傳的圖片
        temp_images = []
        for file in files:
            # 檢查檔案類型
            if not file.content_type.startswith('image/'):
                continue
            
            # 儲存暫存檔案
            temp_path = TEMP_DIR / file.filename
            with open(temp_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            temp_images.append(temp_path)
        
        if not temp_images:
            return {"error": "沒有有效的圖片檔案"}
        
        # 轉換圖片為 PDF
        images = []
        for img_path in temp_images:
            try:
                img = Image.open(img_path)
                # 轉換為 RGB 模式
                if img.mode == 'RGBA':
                    img = img.convert('RGB')
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                images.append(img)
            except Exception as e:
                print(f"無法處理圖片 {img_path}: {e}")
        
        if not images:
            return {"error": "無法處理任何圖片"}
        
        # 產生 PDF
        output_path = TEMP_DIR / "output.pdf"
        if len(images) == 1:
            images[0].save(output_path, 'PDF', resolution=100.0)
        else:
            images[0].save(
                output_path, 
                'PDF', 
                resolution=100.0, 
                save_all=True, 
                append_images=images[1:]
            )
        
        # 清理暫存圖片
        for temp_img in temp_images:
            try:
                temp_img.unlink()
            except:
                pass
        
        # 回傳 PDF 檔案
        return FileResponse(
            output_path,
            media_type='application/pdf',
            filename='converted.pdf'
        )
    
    except Exception as e:
        return {"error": f"轉換失敗: {str(e)}"}

@app.on_event("shutdown")
async def cleanup():
    """關閉伺服器時清理暫存檔案"""
    try:
        shutil.rmtree(TEMP_DIR)
    except:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)