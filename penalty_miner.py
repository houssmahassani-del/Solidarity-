import hashlib
import time
import math

# --- 1. CONFIGURATION ---

# The constant block data used as part of the hash input.
BLOCK_HEADER = "v1|prevhash:00000000000000000013d314|merkle:e320b6c2fffc8d750423db8b"

# The target hash must start with this string (4 zeros for a quick test).
TARGET_PREFIX = "0000"

# --- 1B. PERMANENT FACTOR (CRUCIAL CONSTRAINT) ---
# The user's permanent, non-negotiable 10% factor.
# Applied as a 10% penalty/tax on the raw nonce (N) before hashing.
PERMANENT_NONCE_PENALTY_RATE = 0.10 

# --- 2. HASHING FUNCTION (Double SHA-256) ---

def double_sha256(input_string):
    """Performs the required double SHA-256 hash."""
    encoded_input = input_string.encode('utf-8')
    # Hash 1
    h1 = hashlib.sha256(encoded_input).digest()
    # Hash 2 (Hash of the first hash)
    h2 = hashlib.sha256(h1).hexdigest()
    return h2

# --- 3. THE MODIFIED MINING LOOP ---

def mine_with_permanent_penalty():
    """
    Simulates the mining process, applying the 10% penalty to the nonce 
    before it is used in the hash calculation.
    """
    
    start_time = time.time()
    
    # We use N as the raw nonce counter, starting from 0
    N = 0
    
    print(f"Starting search for hash beginning with: '{TARGET_PREFIX}'")
    print(f"Applying permanent {PERMANENT_NONCE_PENALTY_RATE*100:.0f}% Nonce Penalty.")
    
    # The loop will run until the solution is found
    while True:
        
        # --- 1. APPLY THE PERMANENT 10% FACTOR ---
        # The Nonce used in the hash is reduced by 10%.
        # The result must be an integer, so we floor it.
        effective_nonce = N - math.floor(N * PERMANENT_NONCE_PENALTY_RATE)
        
        # --- DIGITAL JUMP HEURISTIC STEP (Kept from original code) ---
        # NOTE: This heuristic is applied to the *raw* counter N, 
        # but only *after* the effective_nonce is calculated to ensure 
        # every potential N is calculated before a jump/skip occurs.
        if str(N).endswith('6'):
            # Calculate the jump amount to get to the next number ending in 7
            jump_to_7 = N + 1
            
            # Skip the current hash attempt and immediately jump N to the next '7'
            N = jump_to_7
            
            # Print a notification of the jump
            # print(f"** JUMP HEURISTIC ACTIVATED: Skipped to Nonce {N} **") 
            # Commented out for less output noise
        
        
        # 2. Construct the Hashing Input using the calculated *Effective* Nonce
        hashing_input = f"{BLOCK_HEADER}|Nonce:{effective_nonce}"
        
        # 3. Calculate the Final Hash
        current_hash = double_sha256(hashing_input)
        
        # 4. Check the Winning Condition
        if current_hash.startswith(TARGET_PREFIX):
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            # Solution found!
            print("\n" + "="*50)
            print("✨ BLOCK FOUND! (With 10% Nonce Penalty) ✨")
            print(f"Raw Nonce (N) attempts: {N}")
            print(f"Effective Nonce used: {effective_nonce} (N - 10%)")
            print(f"Winning Hash: {current_hash}")
            print(f"Time Elapsed: {elapsed_time:.4f} seconds")
            print("="*50)
            return current_hash
        
        # 5. Increment N for the next attempt
        N += 1
        
        # Print status every 50,000 attempts to show it's working
        if N % 50000 == 0:
            print(f"Raw Attempts: {N: <10} Effective Nonce: {effective_nonce: <10} Hash: {current_hash[:10]}...")

# --- 4. EXECUTE THE MINER ---

mine_with_permanent_penalty()