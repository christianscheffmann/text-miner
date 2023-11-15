import re
from langdetect import detect
from collections import defaultdict
from tqdm import tqdm
import spacy

from Handler import DocumentHandler

from pathlib import Path

from gensim.corpora import Dictionary

import pickle
import json

def defaultdict_list(lst):
    d = defaultdict(list)
    
    for k, v in lst:
        d[k].append(v)
        
    return d
    
    
    
class CorpusMiner:
    # Iterator of file paths and document bytes
    def __init__(self, byte_ref_iterator, save_blobs=False):
        extracted_data = {}
        corpus_dict = Dictionary()
        for ref, doc_bytes in tqdm(byte_ref_iterator):
            text = DocumentHandler.process(Path(fn).suffix, doc_bytes)
            miner = DocumentMiner(text)
            
            if save_blobs:
                path = Path("blobs/" + ref + ".pkl").mkdir(parents=True, exist_ok=True)
                with path.open('wb') as fp:
                    pickle.dump(miner.lemmas, fp)

            extracted_data[ref] = miner.extracted_data

            d = defaultdict(dict)

            for k, v in miner.inverted_index_entries:
                d[k][ref] = v

            corpus_dict.add_documents([miner.lemmas])

        path = Path("extracted_data.json")
        with path.open("w") as fp:
            json.dump(extracted_data, fp, indent=4)

        corpus_dict.save("dictionary.dct")

        
    @classmethod
    def from_path_iterator(cls, path_iterator):
        return cls(list((e, e.read_bytes()) for e in path_iterator))


class DocumentMiner:
    language_dict = {"en": "en_core_web_lg"}

    regex_dict = {"email": r"^[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$",\
         "domain": r"^[-a-zA-Z0-9@:%._\\+~#=]{1,256}\\.[a-zA-Z0-9()]{1,6}\\b(?:[-a-zA-Z0-9()@:%_\\+.~#?&\\/=]*)$",\
          "md5": r"([a-fA-F\d]{32})",\
          "ipv4": r"^(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"}
    
    def __init__(self, text, default_language="en"):
        language = detect(text)
        
        if language not in DocumentMiner.language_dict.keys():
            language = default_language

        nlp = spacy.load(DocumentMiner.language_dict[language])
        doc = nlp(text)


        self.extracted_data = {n: re.findall(DocumentMiner.regex_dict[n], text) for n in DocumentMiner.regex_dict.keys()}
        self.extracted_data["entities"] = set([(e.text, e.label_) for e in doc.ents])

        filtered_words = [w for w in doc if not w.is_stop and not w.is_punct and not w.is_space]
        
        # Get lemmas for bag-of-words representation
        self.lemmas = [w.lemma_ for w in filtered_words]

        # Get lemmas with indices for inverted index
        self.inverted_index_entries = defaultdict_list([(w.lemma_, w.i) for w in filtered_words])

            
            



