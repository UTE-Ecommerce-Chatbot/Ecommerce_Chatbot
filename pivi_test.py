# from pyvi import ViTokenizer, ViPosTagger

# ViTokenizer.tokenize(u"Trường đại học bách khoa hà nội")

# ViPosTagger.postagging(ViTokenizer.tokenize(u"Trường đại học Bách Khoa Hà Nội"))

# from pyvi import ViUtils
# ViUtils.remove_accents(u"Trường đại học bách khoa hà nội")

# from pyvi import ViUtils
# print(ViUtils.add_accents(u'truong dai hoc bach khoa ha noi'))

import spacy
nlp1 = spacy.load('vi_core_news_lg')
doc1 = nlp1('Cộng đồng xử lý ngôn ngữ tự nhiên')
for token in doc1:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)
from spacy.lang.vi import Vietnamese
nlp = Vietnamese()
doc = nlp('Cộng đồng xử lý ngôn ngữ tự nhiên')
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)