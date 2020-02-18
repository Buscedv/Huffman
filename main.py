# Huffman compression/coding example.
# 1.4
# 29.4.2019 Edvard Busck-Nielsen
# A program that takes in text as input or from a text file and outputs stats on how the file would be
# like if it was compressed using Huffman coding.

# License: GNU GPL v.3


import os
import yaml

# Function for decompressing.
def decompress(huffman_tree, binary):
    text = ""

    # Sets the current working branch to the last branch in the huffman_tree
    branch = list(huffman_tree)[-1]
    branch = huffman_tree[branch]

    # Loops over every bit in the binary string.
    for chr in binary:
        # Converts the bit to an int.
        chr = int(chr)
        # Gets the future current branch name.
        current = branch[chr]

        # Checks if the future current branch name is a letter (1 character long)
        if len(current) == 1:
            # The current branch is a letter witch means the current character has been reached and decompressed.
            # Adds the decompressed character to the final string.
            text = text+current
            # Resets the branch to the starting branch (same as on line 16,17,18)
            branch = list(huffman_tree)[-1]
            branch = huffman_tree[branch]
        else:
            # The current branch is not letter witch means the current character has not been reached and decompressed.
            # Sets the current working branch so that the loop can continue.
            branch = huffman_tree[current]
    return text

# Function for converting text to 8-bit binary.
def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

# Function for sorting dictionaries by value; low to high.
def sort_dict(dict):
    from collections import OrderedDict
    sorted_dict = sorted(dict.items(), key=lambda kv: kv[1])
    sorted_dict = OrderedDict(sorted_dict)
    return sorted_dict

# Compresses text using the huffman algorythm.
def compress(raw_data):
    import time
    # Gets time of compression start so that we can calculate how long the compression took.
    start = time.time()

    appearences = []
    tree = {}
    tree_history = []
    huffman_tree = {}
    tmp_huffman_tree = {}

    compression_tree = {}

    # Indexes the raw data and counts appearences (frequenzes) of characters
    for chr in raw_data:
        if chr in appearences:
            tree[chr] += 1
        elif chr not in appearences:
            appearences.append(chr)
            tree[chr] = 1
        else:
            print ("Error indexing")
    # Sorts the dictionary with characters and their frequenzes from low to high.
    tree = sort_dict(tree)

    # Gets the most common (last in the tree) and the least common (first in the tree) character.
    most_common = list(tree)[-1]
    least_common = list(tree)[0]

    tmp_tree_history = {}

    # Loops over all base nodes in the tree and adds them to a
    # temporary dictionary that then gets added to the tree_history dictionary.
    for key in tree:
        tmp_tree_history[str(key)] = str(tree[key])
    tree_history.append(tmp_tree_history)

    # Constructing the huffman tree

    # Adds together base nodes (single chrs) until you get to the root.
    while len(tree_history[0]) > 1:
        tmp_tree_history = {}

        # The first node in the tree.
        node_one = list(tree_history[0])[0]
        # The node next to the first.
        node_next = list(tree_history[0])[0+1]
        # What the new node (the first and next added together) will be called.
        tmp_node = str(node_one+node_next)
        # What the new node's frequenzy will be.
        tmp_node_val = int(tree[node_one])+int(tree[node_next])

        # Deletes the first and second node in the tree
        # Replaces the two nodes with a new node (their names and frequenses together).
        del tree[node_one]
        del tree[node_next]

        tree[tmp_node] = tmp_node_val

        # Sorts the tree so that the new node gets placed at the correct position in the tree.
        tree = sort_dict(tree)

        # Updates the tree_history with the new 'layer'.
        tree_history[0][tmp_node] = tmp_node_val
        del tree_history[0][node_one]
        del tree_history[0][node_next]

        # Adds the new node and it's childs to the huffman_tree dict used for compressing and decompressing.
        tmp_huffman_tree = {}
        tmp_huffman_tree[0] = node_one
        tmp_huffman_tree[1] = node_next
        huffman_tree[tmp_node] = tmp_huffman_tree

        # Adds the correct binary values to the new nodes in the huffman_tree.
        compression_tree[node_one] = "0"
        compression_tree[node_next] = "1"

    # Gets the huffman tree root.
    root = str(list(tree_history[0])[0])+str(tree[list(tree_history[0])[0]])

    # Compression.
    bits = []
    bits_str = ""
    status = ""
    stat = 0
    # Loops over every character in the raw data.
    for x,chr in enumerate(raw_data):
        # Shows status info.
        os.system("clear")
        print (status)
        print (str(stat)+"%")

        tmp_bits = []
        parent = chr

        # Loops until the current node's parent is the root of the tree.
        while parent+str(len(raw_data)) != root:
            node = parent
            position = 0
            next_position = 0
            next_node = ""
            # Loops over the compression_tree to find the index of the current node.
            for index,key in enumerate(compression_tree):
                if key == node:
                    position = index
            # The index of the node next to the current node.
            next_position = position-1

            # Appends the bit value of the current node to the current character's bit list.
            tmp_bits.append(compression_tree[node])

            # Gets the next node
            next_node = list(compression_tree)[next_position]

            # Checks what the parent of the current node is.
            # The parent can be either:
            # - The node+the next node(-1)
            # - The next node(-1)+node
            # - The node+the next node(+1)
            # - The next node(+1)+node
            if node+next_node in compression_tree:
                # node+node(-1)
                parent = node+next_node
            elif node+next_node+str(len(raw_data)) == root:
                # The parent (node+node(-1)) is root.
                break
            elif next_node+node in compression_tree:
                # next node(-1)+node
                parent = next_node+node
            else:
                if next_node+node+str(len(raw_data)) == root:
                    # The parent (next node(-1)+node) is root.
                    break

                # The next node is not -1 it's +1
                next_position = position+1
                next_node = list(compression_tree)[next_position]
                if node+next_node in compression_tree:
                    # node+node(+1)
                    parent = node+next_node
                elif node+next_node+str(len(raw_data)) == root:
                    # The parent (node+node(+1)) is root.
                    break
                elif next_node+node in compression_tree:
                    # next node(+1)+node
                    parent = next_node+node
                elif next_node+node+str(len(raw_data)) == root:
                    # The parent (next node(+1)+node) is root.
                    break
        # Reverses the current character's bit list.
        tmp_bits = tmp_bits[::-1]
        # Loops over the temporary bit list and adds the bits to the combined bit list.
        for chr in tmp_bits:
            bits.append(chr)
        # Updates the status (claculates percentage)
        status = "Character: "+str(x)+"/"+str(len(raw_data))
        stat = 100*x
        stat = stat/len(raw_data)
        stat = int(stat)
    # The bits are currently stored in a list this loop converts the list to a string of bits.
    for chr in bits:
        bits_str = bits_str+chr

    os.system("clear")
    # Stops the time
    end = time.time()
    # calculates the time the compression took.
    end = end - start

    # Claculates the compression percentage.
    raw_data_lenght = len(raw_data)*8
    percentage = 100*len(bits_str)
    percentage = percentage/raw_data_lenght
    percentage = 100-percentage

    # Asks if the user want to see the bits or just how many bits there are.
    action = input("\033[1mDone compressing, do you want to show the bits before and after? y/n: \033[0m")
    if action == "y":
        print ("")
        print ("\033[1m\033[4mBefore:\033[0m\033[2m"+"("+str(len(text_to_bits(raw_data)))+" bits)\033[0m")
        print ("\033[91m"+text_to_bits(raw_data)+"\033[0m")
        print ("\033[1m\033[4mAfter:\033[0m\033[2m"+"("+str(len(bits_str))+" bits)\033[0m")
        print ("\033[92m"+bits_str+"\033[0m")
    else:
        print ("\033[1m\033[4mBefore:\033[0m\033[2m"+"("+str(len(text_to_bits(raw_data)))+" bits)\033[0m")
        print ("\033[1m\033[4mAfter:\033[0m\033[2m"+"("+str(len(bits_str))+" bits)\033[0m")


    # Prints out results.
    print ("")
    # Asks if the user wants to decompress the text.
    action = input("\033[1mDo you want to decompress and print out result? y/n: \033[0m")
    if action == "y":
        # decompresses the text using the huffman_tree and the compressed bits.
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
        return percentage,huffman_tree,bits_str
    else:
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
        return percentage,huffman_tree,bits_str

# Start function for returning to 'menu'
def startup():
    os.system("clear")
    # Startup
    os.system("figlet H u f f m a n")
    print ("")
    # Asks if the user wants to compress or decompress.
    action = input("\033[1m[c]ompress or [d]compress? (Ctrl+C to quit) \033[0m")
    if action == "d":
        file_name = input("\033[1mFile name (without .txt): \033[0m")
        huffman_tree_file_name = input("\033[1mHuffman tree file name (blank for [file name]_tree): \033[0m")

        if huffman_tree_file_name == "":
            huffman_tree_file_name = file_name+"_tree.txt"

        file_name = file_name+".txt"

        with open(file_name, 'r') as binary_file:
            bits = binary_file.read().replace('\n', ' ')

        with open(huffman_tree_file_name, 'r') as huffman_tree_file:
            huffman_tree_str = huffman_tree_file.read().replace('\n', ' ')
        huffman_tree = yaml.load(huffman_tree_str, Loader=yaml.FullLoader)
        print(decompress(huffman_tree,bits))
        tmp = input("continue...")
        startup()
    else:
        # Asks for file or line input.
        action = input("\033[1m[f]ile or [i]nput? \033[0m")
        if action == "i":
            # Line input
            raw_data = input("\033[1mText: \033[0m")
        elif action == "f":
            # Asks for file name
            file_name = input("\033[1mFile name (without .txt): \033[0m")

            if file_name == "":
                file_name = "data.txt"
            else:
                file_name = file_name+".txt"

            with open(file_name, 'r') as file:
                data = file.read().replace('\n', ' ')
                raw_data = data
        else:
            raw_data = input("\033[1mText: \033[0m")

        # Compresses and gets percentage result.
        percentage, huffman_tree, bits = compress(raw_data)
        print ("\033[1mCompressed to \033[92m"+str(percentage)+'% \033[1msmaller\033[0m')
        print("")

        # Asks if the user wants to save the compressed file.
        action = input("\033[1mDo you want to save the compressed file? y/n: \033[0m")
        if action == "y":
            name = input("\033[1mOutput file name (without .txt): \033[0m")

            with open(name+".txt", "w+") as f:
                f.write(bits)
            with open(name+"_tree.txt", "w+") as f:
                f.write(str(huffman_tree))

            print("Files: "+name+".txt (bits) & "+name+"_tree.txt (huffman_tree) saved.")
            tmp = input("continue...")
            startup()

startup()
