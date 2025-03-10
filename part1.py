import os
import argparse
import heapq
import struct

def main():
    parser = argparse.ArgumentParser(description='Huffman encoding')
    parser.add_argument('file', type=str, help='File to compress')
    args = parser.parse_args()
    file_path = args.file
    file_size = os.path.getsize(file_path)

    # Build frequency table
    frequency = {}
    with open(file_path, 'r') as file:
        for line in file:
            for char in line:
                if char.islower():
                    frequency[char] = frequency.get(char, 0) + 1

    print("Frequency Table: " + str(frequency))

    # Build Huffman tree
    order = 0 
    heap = [(freq, order, char, None, None) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        order += 1
        merged = (left[0] + right[0], order, None, left, right)  # Internal node
        heapq.heappush(heap, merged)

    # Generate Huffman Codes
    def generate_codes(node, prefix=""):
        if node[2] is not None:  # Leaf node
            huffman_codes[node[2]] = prefix
        else:  # Internal node
            generate_codes(node[3], prefix + "0")
            generate_codes(node[4], prefix + "1")

    huffman_codes = {}
    generate_codes(heap[0])

    # Compress file
    bit_string = ""
    with open(file_path, 'r') as file:
        for line in file:
            for char in line:
                if char in huffman_codes:
                    bit_string += huffman_codes[char]

    padding = 8 - len(bit_string) % 8
    bit_string += "0" * padding

    byte_array = bytearray()
    for i in range(0, len(bit_string), 8):
        byte_array.append(int(bit_string[i:i+8], 2))

    compressed_file_path = file_path + ".compressed"
    with open(compressed_file_path, 'wb') as file:
        file.write(struct.pack('B', padding))
        file.write(byte_array)

    # Print required output
    compressed_file_size = os.path.getsize(compressed_file_path)

    print("\nFile size before compression:", file_size, "bytes")
    print("File size after compression:", compressed_file_size, "bytes")

if __name__ == "__main__":
    main()
