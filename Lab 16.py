import itertools

# Known PNG header bytes
png_header = [0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]


# Function to simulate the LFSR
def lfsr(taps, state, length):
    output = []
    for _ in range(length):
        bit = state & 1
        state >>= 1
        if bit:
            state ^= taps
        output.append(bit)
    return state, output


# Brute-force the initial states
def brute_force_lfsr(encrypted_header):
    for state1 in range(2 ** 12):
        for state2 in range(2 ** 19):
            # Taps for each LFSR (x^12 + x^2 + x + 1) and (x^19 + x^5 + x^2 + x + 1)
            taps1 = 0b100000000101
            taps2 = 0b1000000000000010001

            # Initialize LFSRs with the current states
            lfsr1_state = state1
            lfsr2_state = state2

            # Generate 8 bytes of keystream from the LFSRs
            keystream = []
            for _ in range(8):
                lfsr1_state, bits1 = lfsr(taps1, lfsr1_state, 12)
                lfsr2_state, bits2 = lfsr(taps2, lfsr2_state, 19)

                # Combine the bits to form a byte for each LFSR
                byte1 = int(''.join(str(bit) for bit in bits1), 2)
                byte2 = int(''.join(str(bit) for bit in bits2), 2)

                # Modulo 256 addition of outputs from both LFSRs
                random_byte = (byte1 + byte2) % 256
                keystream.append(random_byte)

            # XOR the generated keystream with the encrypted header
            decrypted_header = [enc_byte ^ ks_byte for enc_byte, ks_byte in zip(encrypted_header, keystream)]

            # Check if the decrypted header matches the known PNG header
            if decrypted_header == png_header:
                print(f"Found matching LFSR states! LFSR1: {state1:012b}, LFSR2: {state2:019b}")
                return state1, state2

    print("No matching LFSR states found.")
    return None, None


# Load the first 8 bytes of the encrypted file
with open('flag.enc', 'rb') as f:
    encrypted_header = list(f.read(8))

# Call the brute force function
brute_force_lfsr(encrypted_header)
