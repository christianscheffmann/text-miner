import tempfile
from abc import ABC, abstractmethod:
from pypdf import PdfReader
import xml.etree.ElementTree as ET
import textract
from charset_normalizer import from_bytes
from io import BytesIO
import quopri


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
        if not self.is_supported(suffix):
            print("File extension " + suffix + " is currently unsupported. Sorry!")
            return ""
        
        handler = handler_map[suffix]
        return handler.process(doc_bytes).replace("\n", "").replace("\r", "")
    
    @staticmethod
    def is_supported(suffix):
        return suffix in handler_map.keys()

class Handler(ABC):
    def __get_best_string(self, doc_bytes):
        return str(from_bytes(doc_bytes).best())
        
    @abstractmethod
    def process(self, doc_bytes):
        pass
    
    
class HandlerMbox(Handler):
    def process(self, doc_bytes):
        return self.__get_best_string(doc_bytes) # TODO: Use quopri for decoding instead


class HandlerEml(Handler):
    def process(self, doc_bytes):
        return self.__get_best_string(doc_bytes)


class HandlerTxt(Handler):
    def process(self, doc_bytes):
        return self.__get_best_string(doc_bytes)


class HandlerPdf(Handler):
    def process(self, doc_bytes):
        reader = PdfReader(BytesIO(doc_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text()
            
        return text
        

class HandlerDoc(Handler):
    def process(self, doc_bytes):
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            temp.write(doc_bytes)
            temp.flush()
            
            return textract.process(temp.name, extension=".doc").decode("utf-8")
        

class HandlerDocx(Handler):
    def process(self, doc_bytes):
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            temp.write(doc_bytes)
            temp.flush()
            
            return textract.process(temp.name, extension=".docx").decode("utf-8")

class HandlerXls(Handler):
    def process(self, doc_bytes):
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            temp.write(doc_bytes)
            temp.flush()
            
            return textract.process(temp.name, extension=".xls").decode("utf-8")


class HandlerXlsx(Handler):
    def process(self, doc_bytes):
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            temp.write(doc_bytes)
            temp.flush()
            
            return textract.process(temp.name, extension=".xlsx").decode("utf-8")


class HandlerCsv(Handler):
    def process(self, doc_bytes):
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            temp.write(doc_bytes)
            temp.flush()
            
            return textract.process(temp.name, extension=".csv").decode("utf-8")


class HandlerXml(Handler):
    def process(self, doc_bytes):
        root = ET.fromstring(self.__get_best_string(doc_bytes))
        return ET.tostring(root, encoding="utf-8", method="text").decode("utf-8")


class HandlerJson(Handler):
    def process(self, doc_bytes):
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            temp.write(doc_bytes)
            temp.flush()
            
            return textract.process(temp.name, extension=".json").decode("utf-8")


class HandlerYml(Handler):
    def process(self, doc_bytes):
        return self.__get_best_string(doc_bytes)


class HandlerHtml(Handler):
    def process(self, doc_bytes):
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            temp.write(doc_bytes)
            temp.flush()
            
            return textract.process(temp.name, extension=".html").decode("utf-8")



