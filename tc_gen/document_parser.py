from bs4 import BeautifulSoup
import pandas as pd
import json
import os

def extract_text_from_html(html_content, source_file="unknown"):
    """Extracts all meaningful text from an HTML document, splitting into chunks."""
    soup = BeautifulSoup(html_content, 'lxml')
    chunks = []

    # 제목 추출
    title = soup.find('title')
    if title and title.string:
        chunks.append({'content': title.string.strip(), 'type': 'title', 'source_file': source_file})

    # 모든 텍스트 노드에서 텍스트 추출 (스크립트, 스타일 제외)
    for element in soup.find_all(text=True):
        if element.parent.name not in ['script', 'style', '[document]', 'head', 'title'] and element.string.strip():
            text = element.string.strip()
            # 너무 짧은 텍스트는 무시 (예: 테이블의 ID만 있는 경우)
            if len(text) > 20:
                chunks.append({'content': text, 'type': 'text', 'source_file': source_file})
    
    # 테이블 데이터 추출 (각 셀을 별도의 청크로)
    for table in soup.find_all('table'):
        try:
            df = pd.read_html(str(table), header=None)[0] # 헤더 없이 모든 행을 데이터로
            for _, row in df.iterrows():
                for cell_value in row.dropna().values:
                    cell_text = str(cell_value).strip()
                    if len(cell_text) > 20: # 의미 있는 길이의 셀만
                        chunks.append({'content': cell_text, 'type': 'table_cell', 'source_file': source_file})
        except Exception as e:
            # print(f"Warning: Could not parse a table in {source_file}. Reason: {e}")
            pass # 테이블 파싱 실패는 무시

    return chunks


if __name__ == '__main__':
    # 일반 HTML 텍스트 추출 테스트
    html_file_path = 'Confluence-space-export-065656.html/V2X2/1819934765.html' # PV25 개발 기획 및 아키텍처
    try:
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        general_chunks = extract_text_from_html(html_content, source_file=os.path.basename(html_file_path))

        if general_chunks:
            print(f"Successfully extracted {len(general_chunks)} general text chunks from {os.path.basename(html_file_path)}.")
            print("--- Sample General Chunk ---")
            print(json.dumps(general_chunks[0], indent=2, ensure_ascii=False))
            print(json.dumps(general_chunks[1], indent=2, ensure_ascii=False))
        else:
            print(f"No general text chunks extracted from {os.path.basename(html_file_path)}.")

    except FileNotFoundError:
        print(f"Error: The file {html_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred during general text extraction: {e}")
