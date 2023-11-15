import tempfile
from abc import ABC, abstractmethod
from pypdf import PdfReader
import xml.etree.ElementTree as ET
import textract
from charset_normalizer import from_bytes
from io import BytesIO
import quopri


class Handler(ABC):
    def get_best_string(self, doc_bytes):
        return str(from_bytes(doc_bytes).best())
    
    def textract_process(self, doc_bytes, extension):
    	# delete should be false to work on Windows systems
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.write(doc_bytes)

        # Flush to ensure buffered data is written to file
        temp.flush()
        text = textract.process(temp.name, extension=extension).decode("utf-8")
        temp.close()
        return text

    @abstractmethod
    def process(self, doc_bytes):
        pass
    
    
class HandlerMbox(Handler):
    def process(self, doc_bytes):
        return quopri.decodestring(doc_bytes).decode("utf-8")


class HandlerEml(Handler):
    def process(self, doc_bytes):
        return quopri.decodestring(doc_bytes).decode("utf-8")


class HandlerTxt(Handler):
    def process(self, doc_bytes):
        return super().get_best_string(doc_bytes)


class HandlerPdf(Handler):
    def process(self, doc_bytes):
        reader = PdfReader(BytesIO(doc_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text()
            
        return text
        

class HandlerDoc(Handler):
    def process(self, doc_bytes):
        return super().textract_process(doc_bytes, ".doc")
        

class HandlerDocx(Handler):
    def process(self, doc_bytes):
        return super().textract_process(doc_bytes, ".docx")


class HandlerXls(Handler):
    def process(self, doc_bytes):
        return super().textract_process(doc_bytes, ".xls")


class HandlerXlsx(Handler):
    def process(self, doc_bytes):
        return super().textract_process(doc_bytes, ".xlsx")


class HandlerCsv(Handler):
    def process(self, doc_bytes):
        return super().textract_process(doc_bytes, ".csv")


class HandlerXml(Handler):
    def process(self, doc_bytes):
        root = ET.fromstring(self.__get_best_string(doc_bytes))
        return ET.tostring(root, encoding="utf-8", method="text").decode("utf-8")


class HandlerJson(Handler):
    def process(self, doc_bytes):
        return super().textract_process(doc_bytes, ".json")


class HandlerYml(Handler):
    def process(self, doc_bytes):
        return super().get_best_string(doc_bytes)


class HandlerHtml(Handler):
    def process(self, doc_bytes):
    	return super().textract_process(doc_bytes, ".html")


class DocumentHandler:
    handler_map = {".mbox": HandlerMbox(),
                   ".eml": HandlerEml(),
                   ".txt": HandlerTxt(),
                   ".pdf": HandlerPdf(),
                   ".doc": HandlerDoc(),
                   ".docx": HandlerDocx(),
                   ".xls": HandlerXls(),
                   ".xlsx": HandlerXlsx(),
                   ".csv": HandlerCsv(),
                   ".xml": HandlerXml(),
                   ".json": HandlerJson(),
                   ".yml": HandlerYml(),
                   ".html": HandlerHtml()}
    
    
    @staticmethod
    def process(suffix, doc_bytes):
        if not DocumentHandler.is_supported(suffix):
            print("File extension " + suffix + " is currently unsupported. Sorry!")
            return ""
        
        handler = DocumentHandler.handler_map[suffix]
        return handler.process(doc_bytes).replace("\n", "").replace("\r", "")
    
    @staticmethod
    def is_supported(suffix):
        return suffix in DocumentHandler.handler_map.keys()