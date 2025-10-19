import math
import sys
import matplotlib.pyplot as plt

def shannon_entropy(data: bytes) -> float:
    if not data:
        return 0.0

    freq = [0]*256
    
    for b in data:
        freq[b]+=1
    
    total = len(data)
    ent = 0.0
    
    for f in freq:
        if f:
            p = f/total
            ent -= p * math.log2(p)
    
    return ent

def compare_entropy(file1, file2, block_size = 4096):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        d1 = f1.read()
        d2 = f2.read()
    
    e1 = shannon_entropy(d1)
    e2 = shannon_entropy(d2)
    
    print(f"{file1}: {e1:.4f} bits/byte")
    print(f"{file2}: {e2:.4f} bits/byte")
    
    if len(d1) != len(d2):
        minlen = min(len(d1), len(d2))

        d1 = d1[:minlen]
        d2 = d2[:minlen]
    
    segs = range(0, len(d1), block_size)
    
    ent1 = [shannon_entropy(d1[i:i+block_size]) for i in segs]
    ent2 = [shannon_entropy(d2[i:i+block_size]) for i in segs]
    
    plt.plot(ent1, label=file1)
    plt.plot(ent2, label=file2)
    
    plt.xlabel("Blokc index")
    plt.ylabel("entropy in bits/byte")
    
    plt.legend()
    plt.show()