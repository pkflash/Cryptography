# steganography
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from math import ceil
from codec import Codec, CaesarCypher, HuffmanCodes

class Steganography():
    
    def __init__(self):
        self.text = ''
        self.binary = ''
        self.delimiter = '#'
        self.codec = None

    def encode(self, filein, fileout, message, codec):
        image = cv2.imread(filein)
        #print(image) for debugging
        
        # calculate available bytes
        max_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("Maximum bytes available:", max_bytes)

        # convert into binary
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            try:
                shift = int(input("Enter your desired shift: "))
                self.codec = CaesarCypher(shift)
            except TypeError:
                print("Invalid Input. Please enter an integer.")
        elif codec == 'huffman':
            self.codec = HuffmanCodes()
        binary = self.codec.encode(message+self.delimiter)
        
        # check if possible to encode the message
        num_bytes = ceil(len(binary)//8) + 1 
        if  num_bytes > max_bytes:
            print("Error: Insufficient bytes!")
        else:
            print("Bytes to encode:", num_bytes) 
            self.text = message
            self.binary = binary
            bits_left = binary
            #iterate through image array
            for i in range(len(image)):
                if bits_left == "":
                    break
                for j in range(len(image[0])):
                    if bits_left == "":
                        break
                    for k in range(len(image[0][0])):
                        if bits_left == "":
                            break
                        binary_num = bin(image[i][j][k])
                        bits_to_encode = bits_left[0:2]
                        bits_left = bits_left[2:]
                        if binary_num[-2:] == bits_to_encode:
                            continue
                        else:
                            binary_num_list = [*binary_num]
                            binary_num_list[-2] = bits_to_encode[0]
                            binary_num_list[-1] = bits_to_encode[1]

                            new_num = "".join(binary_num_list)
                            image[i][j][k] = int(new_num, 2)

                    
                        
                    
            cv2.imwrite(fileout, image)
                   
    def decode(self, filein, codec):
        image = cv2.imread(filein)
        #print(image) # for debugging      
        flag = True
        
        # convert into text
        if codec == 'binary':
            self.codec = Codec() 
        elif codec == 'caesar':
            try:
                shift = int(input("Enter your desired shift: "))
                self.codec = CaesarCypher(shift)
            except TypeError:
                print("Invalid Input. Please enter an integer.")
        elif codec == 'huffman':
            if self.codec == None or self.codec.name != 'huffman':
                print("A Huffman tree is not set!")
                flag = False
        if flag:
            binary_data = "" #change this
            # your code goes here
            # extract image bits
            for i in range(len(image)):
                for j in range(len(image[0])):
                    for k in range(len(image[0][0])):
                        binary_num = '{0:08b}'.format(image[i][j][k])
                        binary_data += binary_num[-2] + binary_num[-1]
            #update data attributes
            self.text = self.codec.decode(binary_data)
            self.binary = self.codec.encode(self.text+self.delimiter)
                 
        
    def print(self):
        if self.text == '':
            print("The message is not set.")
        else:
            print("\nText message:", self.text)
            print("Binary message:", self.binary)          

    def show(self, filename):
        plt.imshow(mpimg.imread(filename))
        plt.show()

if __name__ == '__main__':
    
    s = Steganography()

    s.encode('fractal.jpg', 'fractal.png', 'hello', 'binary')
    # NOTE: binary should have a delimiter and text should not have a delimiter
    assert s.text == 'hello'
    print(s.binary)
    assert s.binary == '011010000110010101101100011011000110111100100011'

    s.decode('fractal.png', 'binary')
    print(s.text)
    assert s.text == 'hello'
    print(s.binary)
    assert s.binary == '011010000110010101101100011011000110111100100011'
    print('Everything works!!!')
   
