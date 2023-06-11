from langchain.document_loaders import PyPDFLoader

def load_pdf_pages(file_name):
    loader = PyPDFLoader(file_name)
    pages = loader.load_and_split()
    print(f"load_pdf finished processing {file_name}")
    return pages


def load_pdf_text(file_name):
    pages = load_pdf_pages(file_name)
    text = '\n\n'.join([page.page_content for page in pages])
    return text