from langchain.document_loaders import PyPDFLoader

def load_pdf(file_name):
    loader = PyPDFLoader(file_name)
    pages = loader.load_and_split()
    print(f"load_pdf finished processing {file_name}")
    return pages