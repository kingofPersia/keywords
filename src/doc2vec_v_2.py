import locale
import glob
import os.path
import requests
import tarfile

dirname = 'aclImdb'
filename = 'aclImdb_v1.tar.gz'
locale.setlocale(locale.LC_ALL, 'C')


# Convert text to lower-case and strip punctuation/symbols from words
def normalize_text(text):
    norm_text = text.lower()

    # Replace breaks with spaces
    norm_text = norm_text.replace('<br />', ' ')

    # Pad punctuation with spaces on both sides
    for char in ['.', '"', ',', '(', ')', '!', '?', ';', ':']:
        norm_text = norm_text.replace(char, ' ' + char + ' ')

    return norm_text


if not os.path.isfile('aclImdb/alldata-id.txt'):

    # Concat and normalize test/train data
    folders = ['train/pos', 'train/neg', 'test/pos', 'test/neg', 'train/unsup']
    alldata = u''

    for fol in folders:
        temp = u''
        output = fol.replace('/', '-') + '.txt'

        # Is there a better pattern to use?
        #=======================================================================
        # txt_files = glob.glob('/'.join([dirname, fol, '*.txt']))
        #=======================================================================
        path='C:/Users/avinashchandra/workspace/PARMENIDES/Wiki'
        for filename in glob.glob(os.path.join(path, '*.txt')):
            with open(filename,'r',encoding='UTF8') as t:
                control_chars = [chr(0x85)]
                t_clean = t.read()

                for c in control_chars:
                    t_clean = t_clean.replace(c, ' ')

                temp += t_clean

            temp += "\n"


#===============================================================================
#         for txt in txt_files:
#             with open(txt, 'r', encoding='utf-8') as t:
#                 control_chars = [chr(0x85)]
#                 t_clean = t.read()
# 
#                 for c in control_chars:
#                     t_clean = t_clean.replace(c, ' ')
# 
#                 temp += t_clean
# 
#             temp += "\n"
#===============================================================================

        temp_norm = normalize_text(temp)
        with open('/'.join([dirname, output]), 'w', encoding='utf-8') as n:
            n.write(temp_norm)

        alldata += temp_norm

    with open('/'.join([dirname, 'alldata-id.txt']), 'w', encoding='utf-8') as f:
        for idx, line in enumerate(alldata.splitlines()):
            num_line = "_*{0} {1}\n".format(idx, line)
            f.write(num_line)