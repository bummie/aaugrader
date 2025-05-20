import hashlib
import json
import sys

def chained_hash_sequence(function_sequence):
    """Hash a sequence of function names as done in the C program."""
    h = bytes([0] * 32)
    for name in function_sequence:
        h = hashlib.sha256(h + name.encode()).digest()
    return h.hex()

def load_trusted_hashes(path="trusted_cfg.json"):
    with open(path, "r") as f:
        return json.load(f)

def is_trusted(trace, trusted_data):
    candidate_hash = chained_hash_sequence(trace)
    for entry in trusted_data:
        if entry["final_hash"] == candidate_hash:
            return True, candidate_hash
    return False, candidate_hash

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate_trace.py trace.txt")
        sys.exit(1)

    trace_file = sys.argv[1]

    with open(trace_file, "r") as f:
        trace = [line.strip() for line in f.readlines() if line.strip()]

    trusted = load_trusted_hashes()
    ok, h = is_trusted(trace, trusted)

    print(f"\nTrace:")
    for fn in trace:
        print(f"  {fn}")
    print(f"\nFinal Hash: {h}")

    if ok:
        print("✅ Trace is trusted.")
    else:
        print("❌ ALERT: Trace is NOT trusted.")

if __name__ == "__main__":
    main()
