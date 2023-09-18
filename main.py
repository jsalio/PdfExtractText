import os, glob, PyPDF2, uuid
import shutil

file_path = '.\samples'

class Document(object):
    id =0
    documentType = 0
    nuc = ""
    filePath = ""

    def __init__(self, id,docType, nuc, path) -> None:
        self.documentType = docType
        self.id = id
        self.nuc = nuc
        self.filePath = path

def create_output_dir():
    try:
        os.mkdir('out', 0o666)
    except:
        print("out folder exists skip")

def read_document (document_path:str) -> str:
    pdfReader = PyPDF2.PdfFileReader(document_path)
    count = pdfReader.numPages
    output = []
    for i in range(count):
        page = pdfReader.getPage(i)
        output.append(page.extractText())
        output.append(f'\n -------End of page ({i+1}) ------- \n')
    return ''.join(output)


def create_file(content:str, fileName:str)-> str:
    with open(fileName, 'w') as f:
        f.write(f'{content}')
    return "ok"

# replace  this function for connect to ProdoctivityDb and get full path to pdf documents and return into a list []
def find_document_path(): # [id,documentType,NUC,FilePath]
    list = []
    items = glob.glob(os.path.join(file_path,'*.pdf')) 
    for i in items :
        doc = Document(123,15,"123-789-75",i)
        list.append(doc)
    return list

def generate_csv(list:list):
    output = []
    for row in list:
        output.append(f'{row.id},{row.documentType},{row.nuc},{row.filePath}\n')
    return ''.join(output)
    
create_output_dir()
read_files = find_document_path() 
for files in read_files:
    name = f'{files.id}-{str(uuid.uuid4())}.txt'
    pdf_text = read_document(files.filePath)
    create_file(pdf_text, f'./out/{name}')
csv_data= generate_csv(read_files)
create_file(csv_data,'./out/out.csv')
shutil.make_archive('out', 'zip', './out')
