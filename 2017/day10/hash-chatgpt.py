def knot_hash(input_string):
    # Step 1: Convert input string to list of ASCII codes
    lengths = [ord(char) for char in input_string.strip()]
    # Step 2: Append standard length suffix values
    lengths.extend([17, 31, 73, 47, 23])

    # Step 3: Initialize variables
    sparse_hash = list(range(256))
    current_position = 0
    skip_size = 0

    # Step 4: Perform 64 rounds
    for _ in range(64):
        for length in lengths:
            # Reverse sublist
            sublist = []
            for i in range(length):
                sublist.append(sparse_hash[(current_position + i) % 256])
            sublist.reverse()
            for i in range(length):
                sparse_hash[(current_position + i) % 256] = sublist[i]
            # Move current position forward
            current_position = (current_position + length + skip_size) % 256
            # Increase skip size
            skip_size += 1

    # Step 5: Calculate dense hash
    dense_hash = []
    for block_start in range(0, 256, 16):
        block = sparse_hash[block_start:block_start + 16]
        dense_hash.append(f"{block[0] ^ block[1] ^ block[2] ^ block[3] ^ block[4] ^ block[5] ^ block[6] ^ block[7] ^ block[8] ^ block[9] ^ block[10] ^ block[11] ^ block[12] ^ block[13] ^ block[14] ^ block[15]:02x}")

    # Step 6: Concatenate hexadecimal values
    knot_hash = ''.join(dense_hash)

    return knot_hash

# Test with provided examples
print(knot_hash(""))  # Expected: a2582a3a0e66e6e86e3812dcb672a272
print(knot_hash("AoC 2017"))  # Expected: 33efeb34ea91902bb2f59c9920caa6cd
print(knot_hash("1,2,3"))  # Expected: 3efbe78a8d82f29979031a4aa0b16a9d
print(knot_hash("1,2,4"))  # Expected: 63960835bcdc130f0b66d7ff4f6a5a8e

# Puzzle input
puzzle_input = "212,254,178,237,2,0,1,54,167,92,117,125,255,61,159,164"
print(knot_hash(puzzle_input))  # Solve for puzzle input
