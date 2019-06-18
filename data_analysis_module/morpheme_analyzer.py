from konlpy.tag import Komoran
from tqdm import tqdm
from collections import Counter
import pickle
import os
from time import time


def pos_analyzer():
    for conference in os.listdir('../paper_data'):
        for year in os.listdir('../paper_data/{}/'.format(conference)):
            if not os.path.isdir('../morpheme_analyzed_data/{}/{}'.format(conference, year)):
                os.makedirs('../morpheme_analyzed_data/{}/{}/'.format(conference, year))

            for file_name in os.listdir('../paper_data/{}/{}/'.format(conference, year)):
                sentence = []
                result = []
                with open('../paper_data/{}/{}/{}'.format(conference, year, file_name), 'r', encoding='utf-8') as fp:
                    data = fp.readlines()
                raw_sentence = data[0] + data[1]
                for word in raw_sentence.replace('(', '').replace(')', '').replace('-', ' ').replace('.', '').replace(',', '').replace("’", '').split(' '):
                    flag = 0
                    for alpha in word:
                        if alpha.isupper():
                            flag += 1
                    if flag == 1:
                        sentence.append(word.lower())
                    else:
                        sentence.append(word)
                sentence = ' '.join(sentence)

                for tags in komoran.pos(sentence):
                    if tags[1] == 'SH':
                        try:
                            result.append(upper_to_lower[tags[0]])
                        except KeyError:
                            if tags[0] == 'privacy':
                                print('WTF')
                            if tags[0] == 'malware':
                                result.append('malicious code')
                            else:
                                result.append(tags[0])

                with open('../morpheme_analyzed_data/{}/{}/{}'.format(conference, year, file_name), 'w', encoding='utf-8') as save_fp:
                    for val2 in Counter(result).most_common():
                        save_fp.write('{}, {}\n'.format(val2[0], val2[1]))


if __name__ == '__main__':
    with open('./upper_to_lower.pkl', 'rb') as fp:
        upper_to_lower = pickle.load(fp)
    komoran = Komoran(userdic='./user_dic.txt')
    pos_analyzer()
