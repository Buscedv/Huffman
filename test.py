# Huffman copression/coding example.
# 1.1
# 29.4.2019 Edvard Busck-Nielsen
# A program that takes in text as input or from a text file and outputs stats on how the file would be if it where to be
# compressed using Huffman coding.
# This is just and example and this program dosen't actually compress or decompress files.
# License: GNU GPL v.3


import os

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
    tmp_compression_tree = {}

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

    print (compression_tree)

    root = str(list(tree_history[0])[0])+str(tree[list(tree_history[0])[0]])

    bits = []
    position = 0
    next_position = 0
    for chr in raw_data:
        print ("Character: "+chr)
        parent = ""
        bits.append(compression_tree[chr])

        for x,node in enumerate(compression_tree):
            if node == chr:
                position = x
                break
        if position != 0:
            next_position = position-1
        else:
            next_position = position+1
        print ("Current node: "+str(list(compression_tree)[position]))
        print ("Current next node: "+str(list(compression_tree)[next_position]))
        parent = str(list(compression_tree)[next_position])+str(list(compression_tree)[position])
        if parent+str(len(raw_data)) == root:
            print ("Was root: ("+parent+")")
            break
        else:
            if parent not in compression_tree:
                if parent+str(len(raw_data)) == root:
                    print ("Was root: ("+parent+")")
                    break
                else:
                    print ("1:st not in. ("+parent+")")
                    parent = str(list(compression_tree)[position])+str(list(compression_tree)[next_position])
                    if parent not in compression_tree:
                        if parent+str(len(raw_data)) == root:
                            print ("Was root: ("+parent+")")
                            break
                        else:
                            print ("2:nd not in.("+parent+")")
                            next_position = position+1
                            parent = str(list(compression_tree)[next_position])+str(list(compression_tree)[position])

        while parent+str(len(raw_data)) != root:
            print ("Parent to add: "+str(parent))
            bits.append(compression_tree[parent])
            print ("Bit added: "+str(compression_tree[parent]))
            position = 0
            next_position = 0
            for x,node in enumerate(compression_tree):
                if node == parent:
                    position = x
                    break
            if position != 0:
                next_position = position-1
            else:
                next_position = position+1
            print ("Current node: "+str(list(compression_tree)[position]))
            print ("Current next node: "+str(list(compression_tree)[next_position]))
            parent = str(list(compression_tree)[next_position])+str(list(compression_tree)[position])
            if parent+str(len(raw_data)) == root:
                print ("Was root: ("+parent+")")
                break
            else:
                if parent not in compression_tree:
                    if parent+str(len(raw_data)) == root:
                        print ("Was root: ("+parent+")")
                        break
                    else:
                        print ("1:st not in. ("+parent+")")
                        parent = str(list(compression_tree)[position])+str(list(compression_tree)[next_position])
                        if parent not in compression_tree:
                            if parent+str(len(raw_data)) == root:
                                print ("Was root: ("+parent+")")
                                break
                            else:
                                print ("2:nd not in.("+parent+")")
                                next_position = position+1
                                parent = str(list(compression_tree)[next_position])+str(list(compression_tree)[position])
                                if parent not in compression_tree:
                                    if parent+str(len(raw_data)) == root:
                                        print ("Was root: ("+parent+")")
                                        break
                                    else:
                                        print ("3:d not in.("+parent+")")
                                        next_position = position+1
                                        parent = str(list(compression_tree)[position])+str(list(compression_tree)[next_position])
                                        print ("gggg: "+parent)
            print ("New Parent: "+str(parent))
        print (bits)
    print (bits)


    # binary = "111010011100"
    # branch = list(huffman_tree)[-1]
    # branch = huffman_tree[branch]
    # for chr in binary:
    #     chr = int(chr)
    #     current = branch[chr]
    #     if len(current) == 1:
    #         print (current)
    #         branch = list(huffman_tree)[-1]
    #         branch = huffman_tree[branch]
    #     else:
    #         branch = huffman_tree[current]

    print (tree)
    print (tree_history)
    print(root)

    end = time.time()
    end = end - start
    print ("Compression time: ")
    print (str(end)+" seconds.")
    print (str(end*1000)+" milliseconds.")
    return end

os.system("figlet H u f f m a n")
print ("")
raw_data = input("Text: ")
print ("Compressed to "+str(compress(raw_data))+'% smaller')
