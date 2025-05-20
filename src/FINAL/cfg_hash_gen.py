import hashlib
import json

# Function to hash a sequence of function names like in the C program
def chained_hash_sequence(function_sequence):
    h = bytes([0] * 32)  # Start with 32 null bytes (same as memset 0)
    for name in function_sequence:
        h = hashlib.sha256(h + name.encode()).digest()
    return h.hex()

# Example: list of known good paths (you can expand or load from file)
trusted_paths = [
    ["main", "getUsername", "retrieveGrades", "findUser", "findUser", "findUser", "findUser","findUser", "printGrades","EXIT_OK"],
    ["main", "getUsername", "retrieveGrades", "findUser", "findUser", "findUser", "findUser", "printGrades","EXIT_OK"], 
    ["main", "getUsername", "retrieveGrades", "findUser", "findUser", "findUser", "printGrades","EXIT_OK"],
    ["main", "getUsername", "retrieveGrades", "findUser", "findUser", "printGrades","EXIT_OK"],
    ["main", "getUsername", "retrieveGrades", "findUser", "printGrades","EXIT_OK"],              
]

# Compute and store the hash for each path
trusted_hashes = []
for path in trusted_paths:
    final_hash = chained_hash_sequence(path)
    trusted_hashes.append({
        "path": path,
        "final_hash": final_hash
    })

# Save to JSON file
with open("trusted_cfg.json", "w") as f:
    json.dump(trusted_hashes, f, indent=2)

print("Trusted CFG hashes saved to trusted_cfg.json")
