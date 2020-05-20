# -*- coding: utf-8 -*-
"""
Created on Tue May 19 14:04:13 2020

@authors: Murat Cihan Sorkun, Elif Sorkun

Huffman Encoding 
"""

import pandas as pd

class Node:

    def __init__(self, char=None, freq=None, node1=None, node2=None):
        
        
        self.left = node1
        self.right = node2
        
        if(char==None):
            self.char = node1.char+node2.char
            self.freq = node1.freq+node2.freq
        else:
            self.char = char
            self.freq = freq
                

        
    def PrintTree(self, level=0):
        
        dashes=""
        for x in range(level):
            dashes=dashes+"--"
            
        print(dashes,self.char,":",self.freq)
        level=level+1
        if(self.left!=None):
            self.left.PrintTree(level=level)
        if(self.right!=None):
            self.right.PrintTree(level=level)
            
    def CreateHuffmanDict(self, level=0, code=""):
        level=level+1
        
        huffman_dict={}
        
        if(self.left==None and self.right==None):
            huffman_dict[self.char] = code
            return huffman_dict
        
        else:
            if(self.left!=None):
                huffman_dict_left=self.left.CreateHuffmanDict(level=level, code= code + "0")
                huffman_dict.update(huffman_dict_left)
            if(self.right!=None):
                huffman_dict_right=self.right.CreateHuffmanDict(level=level, code=code + "1")       
                huffman_dict.update(huffman_dict_right)
                
        return huffman_dict
        
        
def huffman_encode(huffman_dict,text):
        
    encoded_text=""
    
    for char in text:
        # print(char)
        # print(huffman_dict[char])
        encoded_text=encoded_text + huffman_dict[char]

    return encoded_text


def huffman_decode(root_node,encoded_text):
        
    decoded_text=""  
    next_node=root_node
    
    for bit in encoded_text:               
        if(next_node.left==None and next_node.right==None):
            decoded_text=decoded_text + next_node.char
            if(bit=="0"):
                next_node=root_node.left
            if(bit=="1"):
                next_node=root_node.right      
                               
        elif(bit=="0"):
            next_node=next_node.left       
        else:
            next_node=next_node.right

    decoded_text=decoded_text + next_node.char

    return decoded_text




#########START############


#Read original text from file  
    
file_name="text1"
f = open("input/"+file_name+".txt", "r", encoding='utf8')
text=f.read()
f.close()



#Create a dataframe contains each unique char with frequency and node

char_list=[]
freq_list=[]
node_list=[]

unique_char_set=set(text)

freq_dict = {}
for char in unique_char_set:
    freq_dict[char]=0


for char in text:
    freq_dict[char]=freq_dict[char]+1
    
for key, value in freq_dict.items():
    char_list.append(key)
    freq_list.append(value)
    node_list.append(Node(char=key,freq=value))
    
    
data_tuples = list(zip(char_list,freq_list,node_list))

huffman_df= pd.DataFrame(data_tuples, columns=['Char','Freq','Node'])

print(huffman_df)


#Create Huffman Tree from frequencies

while(len(huffman_df)>1):
    huffman_df=huffman_df.sort_values(by=['Freq'])
    merged_node = Node(node1=huffman_df['Node'].values[0],node2=huffman_df['Node'].values[1])
    huffman_df = huffman_df.iloc[2:]
    
    merged_node_tuples = (merged_node.char,merged_node.freq,merged_node)
    merged_node_df= pd.DataFrame([merged_node_tuples], columns=['Char','Freq','Node'])
    
    huffman_df=huffman_df.append(merged_node_df)



#Print Tree indentation shows level of node)
huffman_df["Node"][0].PrintTree()

#Create a dictionary (Key:Char, Value=huffman code)
huffman_dict=huffman_df["Node"][0].CreateHuffmanDict()


#Encode the text
encoded_text=huffman_encode(huffman_dict,text)

#Decode the text
decoded_text=huffman_decode(huffman_df["Node"][0],encoded_text)



#Write encoded text to file   
bit_strings = [encoded_text[i:i + 8] for i in range(0, len(encoded_text), 8)]
byte_list = [int(b, 2) for b in bit_strings]
with open("output/"+file_name+'.bin', 'wb') as f:
    f.write(bytearray(byte_list))
    


#Read encoded text from file        
encoded_read_text=""          
with open("output/"+file_name+".bin", "rb") as f:
    bytes_read = f.read()      
for byte in bytes_read:
    # print( '{:08b}'.format(byte))
    encoded_read_text=encoded_read_text+'{:08b}'.format(byte)

#Decode the text from file      
decoded_read_text=huffman_decode(huffman_df["Node"][0],encoded_read_text)    








