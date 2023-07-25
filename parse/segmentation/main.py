import argparse
from utils import load_cmp_dict, identify_item, identify_paragraph, parsing, get_item_paragraph, clean_item_paragraph, sentencize_item_paragraph, remove_empty_keys, reset_paragraph_sent_num, set_spacy_nlp
from collections import OrderedDict 

import os


cmp_fp = 'test_comp_file_list.txt'
cmp_dict = load_cmp_dict(cmp_fp)
nlp = set_spacy_nlp()
output = open(f'test_collections.txt', 'w', encoding='utf-8')


abnormal_cmp = []
for i, (cmp, fp_list) in enumerate(cmp_dict.items()):
    for f in fp_list:
        cik = f.split('/')[-1].split('_')[4]
        year = f.split('/')[-1].split('_')[5].split('-')[1]
        print(f'Parsing... {cik}-{year}')

        with open(f) as fh:     
            data = fh.readlines()
            data = " ".join(data)

        data = identify_paragraph(data)    
        # document_items = parsing(data)
        document_items_paragraphs_sentences = OrderedDict()
        
        data = data.split('\n')
        item_paragraph = get_item_paragraph(data)
        # print( item_paragraph)
        item_paragraph_dict = sentencize_item_paragraph(item_paragraph, nlp)
        # print( item_paragraph_dict)
        item_paragraph_dict = remove_empty_keys(item_paragraph_dict)
        item_paragraph_dict = reset_paragraph_sent_num(item_paragraph_dict)
        document_items_paragraphs_sentences = item_paragraph_dict
        
        if len(document_items_paragraphs_sentences) == 0:
            abnormal_cmp.append(f)

        print("~"*150)
        
        for paragraph_num, sentence_dicts in document_items_paragraphs_sentences.items():
            for sent_num, sentence in sentence_dicts.items():
                output.write(f'{cik}_{year}_P{paragraph_num}_S{sent_num}\t{sentence}\n')

output.close()

