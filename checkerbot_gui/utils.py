from docx import Document

# 从 Word 文件中提取文本
def extract_text_from_word(file_path):
    try:
        doc = Document(file_path)
        content = "\n".join([para.text for para in doc.paragraphs])
        return content
    except Exception as e:
        raise Exception(f"读取 Word 文件失败: {str(e)}")
