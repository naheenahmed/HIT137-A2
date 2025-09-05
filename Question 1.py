import string
from pathlib import Path

# Define 13-letter halves
LOWER_FIRST  = string.ascii_lowercase[:13]   # a-m
LOWER_SECOND = string.ascii_lowercase[13:]   # n-z
UPPER_FIRST  = string.ascii_uppercase[:13]   # A-M
UPPER_SECOND = string.ascii_uppercase[13:]   # N-Z

def shift_in_subset(ch: str, shift: int, subset: str) -> str:
    """Shift ch by 'shift' positions within the given 13-char subset (wraps in that subset)."""
    i = subset.find(ch)
    if i == -1:
        return ch
    L = len(subset)  # 13
    return subset[(i + shift) % L]

def encrypt(text: str, shift1: int, shift2: int) -> str:
    out = []
    for ch in text:
        if ch in LOWER_FIRST:
            k = (shift1 * shift2) % 13
            out.append(shift_in_subset(ch, k, LOWER_FIRST))
        elif ch in LOWER_SECOND:
            k = -((shift1 + shift2) % 13)
            out.append(shift_in_subset(ch, k, LOWER_SECOND))
        elif ch in UPPER_FIRST:
            k = -(shift1 % 13)
            out.append(shift_in_subset(ch, k, UPPER_FIRST))
        elif ch in UPPER_SECOND:
            k = (shift2 * shift2) % 13
            out.append(shift_in_subset(ch, k, UPPER_SECOND))
        else:
            out.append(ch)  # spaces, digits, punctuation, etc.
    return "".join(out)

def decrypt(text: str, shift1: int, shift2: int) -> str:
    out = []
    for ch in text:
        if ch in LOWER_FIRST:
            k = -((shift1 * shift2) % 13)
            out.append(shift_in_subset(ch, k, LOWER_FIRST))
        elif ch in LOWER_SECOND:
            k = ((shift1 + shift2) % 13)
            out.append(shift_in_subset(ch, k, LOWER_SECOND))
        elif ch in UPPER_FIRST:
            k = (shift1 % 13)
            out.append(shift_in_subset(ch, k, UPPER_FIRST))
        elif ch in UPPER_SECOND:
            k = -((shift2 * shift2) % 13)
            out.append(shift_in_subset(ch, k, UPPER_SECOND))
        else:
            out.append(ch)
    return "".join(out)

def encrypt_file(src: str, dst: str, shift1: int, shift2: int) -> None:
    text = Path(src).read_text(encoding="utf-8")
    Path(dst).write_text(encrypt(text, shift1, shift2), encoding="utf-8")

def decrypt_file(src: str, dst: str, shift1: int, shift2: int) -> None:
    text = Path(src).read_text(encoding="utf-8")
    Path(dst).write_text(decrypt(text, shift1, shift2), encoding="utf-8")

def verify(original_file: str, decrypted_file: str) -> None:
    a = Path(original_file).read_text(encoding="utf-8")
    b = Path(decrypted_file).read_text(encoding="utf-8")
    if a == b:
        print("✅ Decryption successful! Files match.")
    else:
        print("❌ Decryption failed! Files do not match.")

def main():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    encrypt_file("raw_text.txt", "encrypted_text.txt", shift1, shift2)
    decrypt_file("encrypted_text.txt", "decrypted_text.txt", shift1, shift2)
    verify("raw_text.txt", "decrypted_text.txt")

if __name__ == "__main__":
    main()
