# Huffman copression/coding example.
# 1.0
# 29.4.2019 Edvard Busck-Nielsen
# A program that takes in text as input or from a text file and outputs stats on how the file would be if it where to be
# compressed using Huffman coding.
# This is just and example and this program dosen't actually compress or decompress files.
# License: GNU GPL v.3


import os
import sys

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def sort_dict(dict):
    from collections import OrderedDict
    sorted_dict = sorted(dict.items(), key=lambda kv: kv[1])
    sorted_dict = OrderedDict(sorted_dict)
    return sorted_dict

def compress(raw_data):
    import time
    start = time.time()

    appearences = []
    tree = {}
    placement = 0
    tree_history = []

    # Indexes the raw data and counts appearences of characters
    for chr in raw_data:
        if chr in appearences:
            tree[chr] += 1
        elif chr not in appearences:
            appearences.append(chr)
            tree[chr] = 1
        else:
            print ("Error indexing")
    tree = sort_dict(tree)
    tmp_tree_history = []
    for key in tree:
        tmp_tree_history.append(str(key))
    tree_history.append(tmp_tree_history)

    while len(tree) >= 2:
        first_node = list(tree)[placement]
        next_node = list(tree)[placement+1]

        tmp_tree_history = []
        tmp_tree_history.append(str(first_node)+str(next_node))
        if len(tree) > 2:
            for index,node in enumerate(tree):
                if index != 0 and index != 1:
                    tmp_node = list(tree)[int(placement+1)+1]
                    tmp_tree_history.append(str(tmp_node))
        tree_history.append(tmp_tree_history)

        tree[first_node] = tree[next_node] + tree[first_node]
        tree[str(first_node)+str(next_node)] = tree.pop(first_node)
        del tree[next_node]
    else:
        print ("")
    end = time.time()
    tree_top = list(tree)[0]
    #print(tree_history)
    print ("RESULT")
    print ("Tree top: "+str(tree_top)+""+str(tree[tree_top]))
    print ("Stats: ")
    end = end - start
    print ("Compression time: ")
    print (str(end)+" seconds.")
    print (str(end*1000)+" milliseconds.")
    print ("Most common character: "+str(tree_history[0][-1]))
    print ("Least common character: "+str(tree_history[0][0]))
    print ("Number of bits before compression: "+str(len(raw_data)*8))
    tree_history = tree_history[0]
    tree_history = tree_history[::-1]
    tree_history_bin = {}
    prefix = ""
    other_num = "0"
    for chr in tree_history:
        if other_num == "1":
            tmp_bin = prefix + "0"
            other_num = "0"
        elif other_num == "0":
            tmp_bin = prefix + "1"
            other_num = "1"
            prefix = prefix+"0"
        tree_history_bin[chr] = tmp_bin

    compressed_bits = ""
    for chr in raw_data:
        compressed_bits = compressed_bits+tree_history_bin[chr]
    print ("Number of bits after compression: "+str(len(compressed_bits)))
    percentage = 100*len(compressed_bits)
    percentage = percentage/len(text_to_bits(raw_data))
    percentage = 100-percentage
    if percentage > 100:
        percentage = "File Could Not Be Compressed! "
    return percentage


os.system("figlet H u f f m a n")
print ("")
action = input("(f) file or (i) input?")
if action == "i":
    raw_data = input("Text: ")
else:
    with open('data.txt', 'r') as f:
        raw_data = f.readlines()
        raw_data = ''.join(raw_data)
        raw_data = raw_data.replace('\n', ' ').replace('\r', '')
print ("Compressed to "+str(compress(raw_data))+'% smaller')
