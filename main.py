# Huffman copression/coding example.
# 1.2
# 29.4.2019 Edvard Busck-Nielsen
# A program that takes in text as input or from a text file and outputs stats on how the file would be if it where to be
# compressed using Huffman coding.
# This is just and example and this program dosen't actually compress or decompress files.
# License: GNU GPL v.3


import os

def decompress(huffman_tree, binary):
    text = ""
    branch = list(huffman_tree)[-1]
    branch = huffman_tree[branch]
    for chr in binary:
        chr = int(chr)
        current = branch[chr]
        if len(current) == 1:
            text = text+current
            branch = list(huffman_tree)[-1]
            branch = huffman_tree[branch]
        else:
            branch = huffman_tree[current]
    return text

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
    tree_history = []
    huffman_tree = {}
    tmp_huffman_tree = {}

    compression_tree = {}

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

    most_common = list(tree)[-1]
    least_common = list(tree)[0]

    tmp_tree_history = {}

    for key in tree:
        tmp_tree_history[str(key)] = str(tree[key])
    tree_history.append(tmp_tree_history)

    while len(tree_history[0]) > 1:
        tmp_tree_history = {}

        node_one = list(tree_history[0])[0]
        node_next = list(tree_history[0])[0+1]
        tmp_node = str(node_one+node_next)
        tmp_node_val = int(tree[node_one])+int(tree[node_next])

        del tree[node_one]
        del tree[node_next]

        tree[tmp_node] = tmp_node_val
        tree = sort_dict(tree)

        tree_history[0][tmp_node] = tmp_node_val
        del tree_history[0][node_one]
        del tree_history[0][node_next]

        tmp_huffman_tree = {}
        tmp_huffman_tree[0] = node_one
        tmp_huffman_tree[1] = node_next
        huffman_tree[tmp_node] = tmp_huffman_tree

        compression_tree[node_one] = "0"
        compression_tree[node_next] = "1"

    root = str(list(tree_history[0])[0])+str(tree[list(tree_history[0])[0]])

    # Compressing
    bits = []
    bits_str = ""
    for chr in raw_data:
        tmp_bits = []
        parent = chr
        #print ("Chr: "+parent)
        while parent+str(len(raw_data)) != root:
            node = parent
            position = 0
            next_position = 0
            next_node = ""
            for index,key in enumerate(compression_tree):
                if key == node:
                    position = index
            next_position = position-1

            tmp_bits.append(compression_tree[node])
            #print(tmp_bits)

            #node = list(compression_tree)[position]
            next_node = list(compression_tree)[next_position]

            if node+next_node in compression_tree:
                parent = node+next_node
            elif node+next_node+str(len(raw_data)) == root:
                break
            elif next_node+node in compression_tree:
                parent = next_node+node
            else:
                if next_node+node+str(len(raw_data)) == root:
                    break
                next_position = position+1
                next_node = list(compression_tree)[next_position]
                if node+next_node in compression_tree:
                    parent = node+next_node
                elif node+next_node+str(len(raw_data)) == root:
                    break
                elif next_node+node in compression_tree:
                    parent = next_node+node
                elif next_node+node+str(len(raw_data)) == root:
                    break
        tmp_bits = tmp_bits[::-1]
        for chr in tmp_bits:
            bits.append(chr)
    for chr in bits:
        bits_str = bits_str+chr
    print ("")
    print ("\033[1m\033[4mBefore:\033[0m\033[2m"+"("+str(len(text_to_bits(raw_data)))+" bits)\033[0m")
    print ("\033[91m"+text_to_bits(raw_data)+"\033[0m")
    print ("\033[1m\033[4mAfter:\033[0m\033[2m"+"("+str(len(bits_str))+" bits)\033[0m")
    print ("\033[92m"+bits_str+"\033[0m")

    raw_data_lenght = len(raw_data)*8
    percentage = 100*len(bits_str)
    percentage = percentage/raw_data_lenght

    end = time.time()


    end = end - start
    print ("")
    print("\033[1mDecompressed: \033[0m"+decompress(huffman_tree,bits_str))
    print ("")
    print ("\033[1m\033[4mCompression time: \033[0m\033[94m")
    print (str(end)+"\033[0m\033[1m seconds.\033[94m")
    print (str(end*1000)+"\033[0m\033[1m milliseconds.\033[0m")
    print ("")
    print("\033[1mMost common character: \033[94m"+most_common)
    print("\033[0m\033[1mLeast common character: \033[94m"+least_common)
    print ("")
    print("\033[0m\033[1mTree Root: \033[94m"+root+"\033[0m")
    print ("")
    return percentage

os.system("figlet H u f f m a n")
print ("")
raw_data = input("\033[1mText: \033[0m")
print ("\033[1mCompressed to \033[92m"+str(compress(raw_data))+'% \033[1msmaller\033[0m')
