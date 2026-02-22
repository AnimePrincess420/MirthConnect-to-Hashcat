import base64
import sys

# --- ANSI COLOR CODES | MAKE IT PRETTY ---
G = '\033[92m'       # Green (Borders)
C = '\033[96m'       # Cyan (Title)
M = '\033[95m'       # Magenta (Brackets)
R = '\033[91m'       # Red (Status Indicators * and !)
O = '\033[38;5;208m' # Orange (Menu Text/Prompts)
P = '\033[38;5;135m' # Purple (Numbers/Iterations)
Y = '\033[93m'       # Yellow (Hash Output)
RES = '\033[0m'      # Reset

def convert_mirth_to_hashcat(b64_string, iterations):
    try:
        decoded_bytes = base64.b64decode(b64_string)
        
        # Mirth format: First 8 bytes are the Salt, the next 32 are the Hash
        salt_bytes = decoded_bytes[:8]
        hash_bytes = decoded_bytes[8:]
        
        salt_b64 = base64.b64encode(salt_bytes).decode('utf-8')
        hash_b64 = base64.b64encode(hash_bytes).decode('utf-8')
        
        # Format: sha256:iterations:salt:hash
        return f"sha256:{iterations}:{salt_b64}:{hash_b64}"

    except Exception as e:
        return f"{M}[{R}!{M}] {R}Error parsing base64: {str(e)}{RES}"

def main():
    print(f"\n{G}==================================={RES}")
    print(f"{C}   MirthConnect 2 Hashcat v1.1   {RES}")
    print(f"{G}==================================={RES}")

    mirth_hash = input(f"\n{O}Enter raw Mirth Base64 Hash: {RES}").strip()
    
    if not mirth_hash:
        sys.exit(0)

    # Sanity check for pooro typing and mistakes 
    if mirth_hash.startswith("sha256:"):
        print(f"\n{M}[{R}!{M}] {R}Error: This is already a formatted string.{RES}")
        sys.exit(1)

    # Iteration input with a default at 60000 so check your version
    iter_input = input(f"{O}Iterations (Default: {P}600000{O}): {RES}").strip()
    iterations = int(iter_input) if iter_input.isdigit() else 600000

    print(f"\n{M}[{R}*{M}] {O}Converting for Hashcat Mode {P}10900{O}...{RES}")
    
    result = convert_mirth_to_hashcat(mirth_hash, iterations)

    print(f"\n{O}--- HASHCAT FORMAT ---{RES}")
    print(f"{Y}{result}{RES}")
    print(f"{O}----------------------{RES}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{M}[{R}!{M}] {R}Operation cancelled.{RES}")
        sys.exit(0)
