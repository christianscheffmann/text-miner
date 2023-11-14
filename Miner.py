import re
from langdetect import detect
from collections import defaultdict
from tqdm import tqdm
import spacy

from Handler import DocumentHandler

from pathlib import Path

def defaultdict_list(lst):
    d = defaultdict(list)
    
    for k, v in lst:
        d[k].append(v)
        
    return d
    
    
    
class CorpusMiner:
    def __init__(self, byte_filename_iterator, save_blobs=False):
        # Iterator of file paths and document bytes
        for fn, doc_bytes in tqdm(byte_filename_iterator):
            text = DocumentHandler.process(Path(fn).suffix, doc_bytes)
            miner = DocumentMiner(text)
            
            if save_blobs:
                text.save()
                
    def keyword_search():
        pass
        
    def corpus_overview():
        pass
        
        
    @classmethod
    def from_path_iterator(cls, path_iterator):
        return cls(list((e, e.read_bytes()) for e in path_iterator))




class DocumentMiner:
    language_dict = {"en": "en_core_web_lg"}
    
    def __init__(self, text):
        language = detect(text)
        
        # TODO: Handle case where inferred language is not supported
        nlp = spacy.load(language_dict[language])
        doc = nlp(text)

        regex_dict = {"email":}
        
        self.extract_dict = {"email": re.findall(regex_dict["email"], text)}
        

        if doc is not None:
            entities = set([(e.text, e.label_) for e in doc.ents])
            filtered_words = [w for w in doc if not w.is_stop and not w.is_punct and not w.is_space]
            lemmas = [w.lemma_ for w in filtered_words]
            
            inverted_index_entries = defaultdict_list([(w.lemma_, w.i) for w in filtered_words])
            
            



