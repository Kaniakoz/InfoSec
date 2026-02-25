## Chapter 1: Introduction

### 1.1 The Cast of Characters

- **Alice & Bob** — the good guys (communicating parties)
- **Trudy** — the generic adversary ("intruder"); could also be Eve (eavesdropper), etc.
- These characters need not be humans; Alice could be a laptop, Bob a server, Trudy a human

### 1.2 The CIA Triad

|Property|Definition|Example Threat|
|---|---|---|
|**Confidentiality**|Prevents unauthorized _reading_ of data|Trudy reads Bob's bank balance|
|**Integrity**|Prevents/detects unauthorized _modification_ of data|Trudy changes account balances|
|**Availability**|Ensures data/services remain accessible|Denial-of-Service (DoS) attacks|

> Note: Confidentiality ≠ Integrity. Trudy can modify encrypted data without being able to read it.

### 1.3 Beyond CIA

- **Authentication** — verifying that "Bob" is really Bob (different on local machines vs. over a network)
- **Authorization** — restricting what authenticated users can _do_
- **Access Control** = Authentication + Authorization combined
- **Non-repudiation** — preventing denial of having sent a message (via digital signatures)

### 1.4 The Four Pillars of Information Security

As outlined by Lampson:

1. **Specification/Policy** — What should the system do?
2. **Implementation/Mechanism** — How does it do it?
3. **Correctness/Assurance** — Does it actually work?
4. **Human Nature** — Can it survive "clever" users? _(Stamp's addition)_

### 1.5 The People Problem

- Users are often the weakest link in security
- Example: Bob ignoring SSL warnings allows man-in-the-middle attacks despite flawless cryptography
- Assigning complex passwords may cause users to write them down, making things _less_ secure
- Key insight: **Remove humans from the equation as much as possible**

### 1.6 Book Structure Overview

- **Part I: Cryptography** — Symmetric, public key, hash functions, cryptanalysis
- **Part II: Access Control** — Passwords, biometrics, authorization, firewalls
- **Part III: Protocols** — SSH, SSL, IPSec, Kerberos, WEP, GSM
- **Part IV: Software** — Malware, reverse engineering, OS security

---

## Chapter 2: Crypto Basics

### 2.1 Key Terminology

|Term|Definition|
|---|---|
|**Cryptology**|The art and science of making and breaking secret codes|
|**Cryptography**|Making secret codes|
|**Cryptanalysis**|Breaking secret codes|
|**Plaintext**|Original unencrypted data|
|**Ciphertext**|Result of encryption|
|**Key**|Secret value used to configure a cryptosystem|
|**Symmetric cipher**|Same key for encryption and decryption|
|**Public key cipher**|Different keys for encryption (public) and decryption (private)|

### 2.2 Kerckhoffs' Principle

> _A cipher "must not be required to be secret, and it must be able to fall into the hands of the enemy without inconvenience."_ — Auguste Kerckhoffs, 1883

- The **design** of a cryptosystem should not be secret — only the **key** is secret
- **Why?** Secret designs rarely stay secret (reverse engineering); secret algorithms have a bad track record when exposed
- "Security through obscurity" is not real security
- A cipher is **presumed insecure until cryptographers fail to break it**
- Extended meaning: security _designs_ in general should be open to public scrutiny ("more eyeballs = more bugs found")

### 2.3 Classic Ciphers

#### 2.3.1 Simple Substitution Cipher

- Each plaintext letter is replaced by a fixed ciphertext letter
- **Caesar's Cipher**: Shift each letter by 3 positions
    - Plaintext: `a b c d e ...`
    - Ciphertext: `D E F G H ...`
- **Key space with shifts only**: 26 keys → easily broken by exhaustive search
- **Key space with any permutation**: 26! ≈ 2^88 keys → exhaustive search infeasible
- **BUT**: Still broken by **frequency analysis** — letter frequencies in ciphertext match known language frequencies
    - Most common English letter: **E**
    - If 'F' appears most often in ciphertext → probably substitutes for 'E'
- **Lesson**: A large keyspace is _necessary_ but _not sufficient_ for security

#### 2.3.2 Cryptanalysis of Simple Substitution

Attack procedure:

1. Count letter frequencies in ciphertext
2. Compare to known English frequency distribution
3. Map most frequent ciphertext letters to most frequent English letters
4. Guess common words; use context to fill in remaining letters
5. No mathematical shortcut needed — pattern analysis breaks it

#### 2.3.3 Definition of "Secure"

A cryptosystem is **secure** if:

> The best-known attack requires as much work as an **exhaustive key search**

- i.e., no "shortcut" attack is known
- A shortcut attack = a **design flaw**
- Note: A secure cipher with a small keyspace can still be weaker than an insecure cipher with a large keyspace
- In practice, need **both**: secure design AND large keyspace

**Key size guidelines** (assuming 2^40 key tests/second):

|Key Size|Time for Exhaustive Search|
|---|---|
|2^56|~18 hours|
|2^64|~half a year|
|2^128|>9 quintillion years|

Modern symmetric ciphers use **128-bit keys or more**.

#### 2.3.4 Double Transposition Cipher

- Plaintext written into an array, then rows and columns are _permuted_
- Key = matrix dimensions + row permutation + column permutation
- Example: `attackatdawn` → 3×4 matrix, permute rows (1,2,3)→(3,2,1), columns (1,2,3,4)→(4,2,1,3)
- Result: `NADWTKCA ATAT`
- **Advantage**: Disperses plaintext statistics throughout ciphertext (diffusion)
- **Disadvantage**: Doesn't disguise which letters appear (no substitution/confusion)
- The concept of **diffusion** (spreading plaintext info) is used in modern block ciphers

#### 2.3.5 One-Time Pad (Vernam Cipher)

- **Only provably secure** cipher
- Key = random bit string the **same length** as the message
- Encryption: Ciphertext = Plaintext XOR Key
- Decryption: Plaintext = Ciphertext XOR Key
- **Why it's secure**: Given the ciphertext, every possible plaintext of the same length is equally likely — the ciphertext reveals _nothing_ about the plaintext (except its length)
- **Limitation**: Key must be:
    - Truly random
    - Same length as the message
    - Used only **once**
    - Securely distributed in advance

**Why key reuse breaks the OTP ("depth" attack)**:

```
C1 ⊕ C2 = (P1 ⊕ K) ⊕ (P2 ⊕ K) = P1 ⊕ P2
```

The key cancels out, exposing the XOR of the two plaintexts → an attacker can guess messages and verify against both decryptions

**Real-world example — Project VENONA**:

- Soviet spies used OTPs in the 1930s–40s
- A flaw in pad generation caused long key stretches to repeat → messages were "in depth"
- American cryptanalysts decoded many messages, exposing nuclear spies (e.g., Julius Rosenberg, Alger Hiss)

#### 2.3.6 Codebook Cipher

- A book mapping plaintext words → 5-digit codewords
- Decryption uses an inverse codebook
- **Famous example**: Zimmermann Telegram (WWI)
    - German Foreign Minister sent encrypted message to Mexico suggesting alliance against US
    - British decoded it using a captured, partial German codebook
    - Helped bring the US into WWI

**Codebook + Additive**:

- Additive = long list of random numbers XORed with codewords after lookup
- Dramatically increases data needed for statistical attack
- Additive reuse = vulnerability (messages using same additive are in depth)

**Key concept**: Modern **block ciphers** are essentially electronic codebooks where the key determines which "codebook" is used

### 2.4 Modern Crypto History

|Year|Event|
|---|---|
|1929|US Secretary of State Stimson shuts down cryptanalysis ("Gentlemen don't read each other's mail")|
|WWII|Allied cryptanalysts break virtually all Axis ciphers; ULTRA (Enigma), MAGIC (Purple), JN-25|
|1949|Shannon's "Information Theory of Secrecy Systems" — proves OTP security; introduces confusion & diffusion|
|1970s|DES developed; public key crypto invented (GCHQ, then Diffie-Hellman)|
|1990s|AES competition begins; Clipper chip controversy|

**Shannon's Two Design Principles**:

- **Confusion** — obscure the relationship between plaintext and ciphertext (e.g., substitution)
- **Diffusion** — spread plaintext statistics throughout ciphertext (e.g., transposition)
- OTP uses only confusion; double transposition uses only diffusion
- Modern block ciphers use **both**

### 2.5 Taxonomy of Cryptography

```
Cryptography
├── Symmetric Key
│   ├── Stream Ciphers (generalize OTP; confusion only)
│   └── Block Ciphers (generalize codebooks; confusion + diffusion)
├── Public Key Cryptography
│   └── (separate encryption/decryption keys; enables digital signatures)
└── Hash Functions
    └── (fixed-size output from any input; collision-resistant)
```

**Symmetric vs. Public Key**:

- Symmetric crypto: orders of magnitude **faster**
- Public key: solves **key distribution problem**; enables **digital signatures**
- In practice: use public key to exchange symmetric keys, then use symmetric for bulk encryption

### 2.6 Taxonomy of Cryptanalysis

|Attack Type|Attacker Knows|
|---|---|
|**Ciphertext-only**|Ciphertext + algorithm|
|**Known plaintext**|Ciphertext + some matched plaintext-ciphertext pairs|
|**Chosen plaintext**|Can choose plaintext and observe resulting ciphertext|
|**Adaptively chosen plaintext**|Chooses next plaintext based on observed ciphertext|
|**Related key**|Knows keys are related; exploits key relationships|

**Forward search attack** (public key specific):

- Trudy intercepts ciphertext encrypted with Alice's public key
- If plaintext space is small (e.g., "yes"/"no"), she encrypts all candidates with Alice's public key
- Matches ciphertext → breaks the message
- Prevention: ensure plaintext message space is always large (add randomness)

---

## Chapter 3: Symmetric Key Crypto

### 3.1 Overview

Two types of symmetric ciphers:

- **Stream ciphers**: generalize OTP; stretch key into long keystream; XOR with plaintext; confusion only
- **Block ciphers**: generalize codebooks; encrypt fixed-size blocks; use both confusion and diffusion

### 3.2 Stream Ciphers

```
StreamCipher(K) = S  (keystream)
Ci = Pi ⊕ Si        (encrypt)
Pi = Ci ⊕ Si        (decrypt)
```

Key insight: The keystream is used exactly like an OTP, but the key is short and manageable (trading provable security for practicality).

#### 3.2.1 A5/1 (GSM Cell Phone Cipher)

- Uses three **Linear Feedback Shift Registers (LFSRs)**: X (19 bits), Y (22 bits), Z (23 bits) = **64 bits total**
- Key K = 64 bits (initial fill for the three registers)
- At each step: majority vote of bits x8, y10, z10 determines which registers step
    - If register's "clocking bit" = majority → that register steps
    - At least 2 registers step per cycle
- Keystream bit = x18 ⊕ y21 ⊕ z22
- Hardware-optimized; generates 1 bit per cycle
- **Weakness**: Known attacks exist on A5/1 making it less secure than its key size suggests

#### 3.2.2 RC4

- Software-optimized stream cipher; generates **1 byte per step** (vs. A5/1's 1 bit)
- Core: a 256-byte **self-modifying lookup table** S that always contains a permutation of {0…255}
- Key can be 1–256 bytes long

**Initialization (KSA)**:

```
for i = 0 to 255: S[i] = i, K[i] = key[i mod N]
j = 0
for i = 0 to 255: j = (j + S[i] + K[i]) mod 256; swap(S[i], S[j])
i = j = 0
```

**Keystream generation (PRGA)**:

```
i = (i + 1) mod 256
j = (j + S[i]) mod 256
swap(S[i], S[j])
t = (S[i] + S[j]) mod 256
keystreamByte = S[t]
```

- **Known weakness**: First 256 bytes of keystream should be discarded (bias in early output)
- Used in SSL and WEP (WEP implementation was broken)
- Optimized for 8-bit processors; aging but widely deployed

### 3.3 Block Ciphers

An **iterated block cipher** applies a round function F over multiple rounds:

- Input: plaintext block + key
- Each round: new output depends on previous round's output + round subkey
- Round subkeys derived from main key via **key schedule**

#### 3.3.1 Feistel Cipher (Design Principle)

Named after Horst Feistel. A general structure (not a specific cipher):

- Split plaintext P into left (L0) and right (R0) halves
- For each round i = 1, 2, ..., n:
    
    ```
    Li = Ri-1Ri = Li-1 ⊕ F(Ri-1, Ki)
    ```
    
- Ciphertext C = (Ln, Rn)

**Decryption** (runs backwards, same key schedule):

```
Ri-1 = Li
Li-1 = Ri ⊕ F(Ri-1, Ki)
```

**Key advantage**: F does _not_ need to be invertible — the XOR structure handles decryption automatically. Security depends entirely on the choice of F and the key schedule.

#### 3.3.2 DES (Data Encryption Standard)

Developed in the 1970s from IBM's Lucifer cipher; involved controversial NSA modifications.

**Specifications**:

|Parameter|Value|
|---|---|
|Block size|64 bits|
|Key size|56 bits (64 bits with 8 parity bits discarded)|
|Rounds|16|
|Subkey size|48 bits|
|Structure|Feistel cipher|

**DES Round Function** F(Ri-1, Ki):

1. **Expansion Permutation**: 32 bits → 48 bits
2. **XOR with subkey**: 48-bit subkey XORed in
3. **S-boxes**: 8 S-boxes, each maps 6 bits → 4 bits (48 → 32 bits)
4. **P-box**: Final permutation of 32 bits

```
F(Ri-1, Ki) = P-box(S-boxes(Expand(Ri-1) ⊕ Ki))
```

**S-boxes** are the _only non-linear element_ of DES — critical for security. The NSA's modifications to the S-boxes (initially controversial) actually _strengthened_ them against differential cryptanalysis (then unknown publicly).

**Key schedule**: Selects 48 of 56 key bits per round via cyclic shifts and compression permutations

**DES Security Status**:

- 56-bit key is too small by modern standards
- Can be brute-forced in hours with dedicated hardware
- No significant shortcut attack on the _design_ — it just needs a longer key
- NSA did NOT insert a backdoor (30+ years of analysis confirm this)

#### 3.3.3 Triple DES (3DES)

Because DES keys are too short, 3DES extends them:

```
C = E(D(E(P, K1), K2), K1)    [EDE with 2 keys = 112-bit effective key]
```

- Uses Encrypt-Decrypt-Encrypt (EDE) for backward compatibility: if K1 = K2, collapses to single DES
- **Double DES is insecure**: Subject to **meet-in-the-middle attack**
    - Pre-compute table of all E(P, K) for all 2^56 keys K
    - Decrypt C with all 2^56 keys, find match in table
    - Work ≈ 2^57 (no better than single DES in practice)
- 3DES resists meet-in-the-middle (pre-computation infeasible)
- Still widely used but being phased out in favor of AES

#### 3.3.4 AES (Advanced Encryption Standard)

Selected via open competition in 2001; algorithm is **Rijndael** (pronounced "rain doll").

**Specifications**:

|Parameter|Value|
|---|---|
|Block size|128 bits|
|Key sizes|128, 192, or 256 bits|
|Rounds|10–14 (depends on key length)|
|Structure|**NOT** a Feistel cipher (all operations must be invertible)|

**Four round functions** (each with a role):

1. **ByteSub** (nonlinear) — Apply S-box lookup to each byte of 4×4 array; equivalent of DES S-boxes
2. **ShiftRow** (linear mixing) — Cyclic shift rows of 4×4 array (row 0: no shift; row 1: 1 byte; row 2: 2 bytes; row 3: 3 bytes)
3. **MixColumn** (nonlinear) — Mix each column using shift/XOR operations
4. **AddRoundKey** (key addition) — XOR round subkey with 4×4 array

**AES reputation**: Believed to be secure "forever" even against advanced computing. The competition was completely transparent (unlike DES), with NSA as a _judge_ (not a hidden designer).

#### 3.3.5 Other Block Ciphers

|Cipher|Creator|Notable Feature|
|---|---|---|
|**IDEA**|Massey|Mixed-mode arithmetic (XOR + mod 2^16 addition + "almost" mod 2^16 multiply) — no explicit S-box|
|**Blowfish**|Schneier|**Key-dependent S-boxes** — S-boxes generated from the key itself|
|**RC6**|Rivest|**Data-dependent rotations** — unusual use of data as part of the cipher operation|
|**TEA**|Wheeler/Needham|Tiny code; simple rounds but requires many (32) of them|

#### 3.3.6 TEA (Tiny Encryption Algorithm)

- 64-bit blocks, 128-bit key, 32 rounds
- "Almost" a Feistel cipher (uses addition/subtraction instead of XOR)
- Needs separate encrypt/decrypt routines (unlike Feistel)
- Trade-off: simple round function → many rounds required
- Known weakness: related-key attack (use XTEA to address)

```
delta = 0x9e3779b9
sum = 0
for i = 1 to 32:
    sum += delta
    L += ((R << 4) + K[0]) ⊕ (R + sum) ⊕ ((R >> 5) + K[1])
    R += ((L << 4) + K[2]) ⊕ (L + sum) ⊕ ((L >> 5) + K[3])
```

### 3.3.7 Block Cipher Modes of Operation

**Problem**: How to encrypt multiple blocks securely with one key?

#### ECB Mode (Electronic Codebook) — DO NOT USE

```
Ci = E(Pi, K)
Pi = D(Ci, K)
```

- **Fatal flaw**: Identical plaintext blocks → identical ciphertext blocks
- Reveals patterns in data (e.g., image encryption shows image structure)
- Subject to **cut-and-paste attacks** (blocks can be rearranged)

#### CBC Mode (Cipher Block Chaining) — Most Common

```
Ci = E(Pi ⊕ Ci-1, K)    [first block: C-1 = IV]
Pi = D(Ci, K) ⊕ Ci-1
```

- Identical plaintext → different ciphertext (due to chaining with prior ciphertext)
- Requires a random **Initialization Vector (IV)** (sent in plaintext; need not be secret)
- **Error propagation**: A single-bit ciphertext error corrupts _two_ plaintext blocks (then recovers)
- Cut-and-paste attacks are harder (but still possible with known structure)

#### CTR Mode (Counter Mode)

```
Ci = Pi ⊕ E(IV + i, K)
Pi = Ci ⊕ E(IV + i, K)
```

- Turns block cipher into a **stream cipher**
- Supports **random access** (decrypt any block independently)
- Single ciphertext bit error → single plaintext bit error (like a stream cipher)
- Can parallelize encryption/decryption

### 3.4 Integrity with Block Ciphers

**Key insight**: Encryption ≠ Integrity. Trudy can modify ciphertext without being able to read it.

#### MAC (Message Authentication Code)

- Compute CBC encryption of all data; keep only the **final ciphertext block** (the "CBC residue")
- Sender: send plaintext + IV + MAC
- Receiver: recompute MAC; if it matches → data is authentic

```
C0 = E(P0 ⊕ IV, K)
C1 = E(P1 ⊕ C0, K)
...
CN-1 = E(PN-1 ⊕ CN-2, K) = MAC
```

**Why it works**: Any change to a plaintext block propagates to all subsequent CBC blocks, almost certainly changing the final MAC value.

**Important distinction**:

- CBC decryption: single ciphertext error affects only 2 plaintext blocks (errors don't propagate)
- MAC computation: single plaintext change propagates to final block (errors DO propagate)

Both confidentiality AND integrity often required → use separate keys for MAC and encryption (or use authenticated encryption schemes like GCM).

---

## Chapter 4: Public Key Cryptography

### 4.1 Introduction

**Public key crypto** (asymmetric crypto):

- One key encrypts, a **different** key decrypts
- Encryption key can be **made public**
- Solves the key distribution problem of symmetric crypto

**Trapdoor one-way function**: Easy to compute in one direction, hard to reverse — _unless_ you have the trapdoor (private key)

**Digital signatures**: "Encrypt" with _private_ key → anyone can verify with public key

- Only the private key holder could have created the signature
- Signature is tied to the _specific document_ (unlike handwritten signatures)
- Forgery is computationally infeasible
- Anyone can verify automatically (no handwriting expert needed)

History: Invented by GCHQ (UK) in late 1960s/early 70s (classified); independently by Diffie, Hellman, and Merkle in academic literature (~1976).

### 4.2 Knapsack Cryptosystem (Merkle-Hellman)

**Background**: Based on the **subset sum problem** (NP-complete in general)

**Superincreasing knapsack**: Each weight > sum of all previous weights

- Example: (3, 6, 11, 25, 46, 95, 200, 411)
- Solving: Greedy from largest element → O(n) time
- If S = 309: 411 > S → a7 = 0; 200 ≤ S → a6 = 1; S' = 109; 95 ≤ 109 → a5 = 1; …

**Key generation**:

1. Choose superincreasing knapsack (private)
2. Choose multiplier m and modulus n (n > sum of all weights; gcd(m,n) = 1)
3. Multiply: public weights = (superincreasing weights × m) mod n
4. **Public key**: general (non-superincreasing) knapsack
5. **Private key**: superincreasing knapsack + (m, n)

**Encryption**: Given plaintext bits b0…bk-1 and public knapsack W0…Wk-1:

```
C = b0·W0 + b1·W1 + ... + bk-1·Wk-1
```

**Decryption**:

1. Compute m^(-1) mod n (modular inverse of m)
2. C' = C · m^(-1) mod n
3. Solve the superincreasing knapsack with sum C' (easy/fast)

**Weakness**: The knapsack cryptosystem has been _broken_ — the transformation from superincreasing to general knapsack is not secure; lattice reduction attacks (Shamir, 1982) recover the private key. It is now primarily of historical/educational interest.

### 4.3 RSA

**Based on**: Difficulty of factoring large numbers (integer factorization problem)

**Key generation**:

1. Choose large primes p and q
2. Compute N = p · q (the modulus; public)
3. Compute φ(N) = (p-1)(q-1) (Euler's totient; kept secret)
4. Choose e such that gcd(e, φ(N)) = 1 (public exponent; typically 65537)
5. Compute d = e^(-1) mod φ(N) (private exponent)
6. **Public key**: (N, e)
7. **Private key**: (N, d) [or equivalently (p, q, d)]

**Encryption**:

```
C = M^e mod N
```

**Decryption**:

```
M = C^d mod N
```

**Why it works** (by Euler's theorem):

```
C^d = (M^e)^d = M^(ed) = M^(1 + k·φ(N)) = M · (M^φ(N))^k = M · 1^k = M (mod N)
```

**Digital signature with RSA**:

- Sign: S = M^d mod N (use private key)
- Verify: M = S^e mod N (use public key)

**Security**:

- Security relies on **integer factorization** being hard for large N
- Recommended key size: 2048 bits minimum (N), 4096 bits for long-term security
- **Forward search attack concern**: Plaintext space must be large; add random padding (OAEP)

### 4.4 Diffie-Hellman Key Exchange

**Purpose**: Allows Alice and Bob to establish a **shared symmetric key** over a public channel without any prior shared secret.

**Based on**: Discrete logarithm problem (DLP): given g, p, and g^x mod p, find x — computationally infeasible for large p

**Protocol**:

1. Agree publicly on prime p and generator g
2. Alice chooses secret a; computes A = g^a mod p; sends A to Bob
3. Bob chooses secret b; computes B = g^b mod p; sends B to Alice
4. Alice computes K = B^a mod p = g^(ab) mod p
5. Bob computes K = A^b mod p = g^(ab) mod p
6. **Shared key** = g^(ab) mod p

**Eavesdropper Trudy** sees: g, p, A = g^a, B = g^b — but cannot compute g^(ab) without solving DLP

**Vulnerability**: Susceptible to **man-in-the-middle (MITM) attack** if the channel is not authenticated:

- Trudy intercepts A and B; establishes separate key exchanges with both Alice and Bob
- Prevention: authenticate the key exchange (e.g., sign the messages with RSA)

**NOT an encryption system** — only used to establish a shared key, which then drives a symmetric cipher.

### 4.5 Elliptic Curve Cryptography (ECC)

**What it is**: An alternative mathematical setting for public key operations, not a new cryptosystem. The same algorithms (RSA-like signatures, DH-like key exchange) can be implemented using elliptic curve arithmetic.

**Elliptic curve over integers mod p**: Points (x, y) satisfying:

```
y² = x³ + ax + b (mod p)
```

Together with a "point at infinity" (O), these form a **group** under a defined addition operation.

**Point addition**: If P and Q are on the curve, P + Q is also on the curve (via specific geometric/algebraic rules)

**ECC discrete logarithm**: Given point P and Q = kP (k times adding P to itself), find k — hard problem

**Advantage**: Equivalent security with **much shorter keys**

|Security Level|RSA key size|ECC key size|
|---|---|---|
|80-bit|1024 bits|160 bits|
|128-bit|3072 bits|256 bits|
|256-bit|15360 bits|512 bits|

**Use cases**: Preferred for resource-constrained environments (mobile devices, IoT, smartcards). All recent US government public key standards are ECC-based.

### 4.6 Public Key Infrastructure (PKI)

**Problem**: How do you know that a public key actually belongs to who it claims to?

- Trudy could post a fake "Alice's" public key

**Solution**: **Digital certificates** issued by trusted **Certificate Authorities (CAs)**

- A certificate = Bob's public key + identity info + CA's digital signature
- Anyone can verify the CA's signature on the certificate using the CA's public key
- **Root CA**: A CA whose public key is trusted by default (pre-installed in browsers/OS)

**Certificate chain (chain of trust)**:

```
Root CA → Intermediate CA → End-entity certificate
```

**Certificate revocation**: If a private key is compromised, the certificate must be revoked before expiration

- Certificate Revocation Lists (CRLs)
- Online Certificate Status Protocol (OCSP)

**Problems with PKI**: Complex trust model; CA compromises can be devastating (e.g., DigiNotar breach)

---

## Key Formulas & Concepts Summary

|Concept|Formula/Description|
|---|---|
|XOR encryption|C = P ⊕ K; P = C ⊕ K|
|One-time pad security|Key random, length = message, used once only|
|OTP depth attack|C1 ⊕ C2 = P1 ⊕ P2 (key disappears)|
|Feistel encryption|Li = Ri-1; Ri = Li-1 ⊕ F(Ri-1, Ki)|
|CBC encryption|Ci = E(Pi ⊕ Ci-1, K)|
|CBC decryption|Pi = D(Ci, K) ⊕ Ci-1|
|CTR mode|Ci = Pi ⊕ E(IV+i, K)|
|MAC (CBC residue)|MAC = final block of CBC encryption|
|RSA encryption|C = M^e mod N|
|RSA decryption|M = C^d mod N|
|RSA key relation|ed ≡ 1 (mod φ(N))|
|DH shared key|K = g^(ab) mod p|

---

## Common Attacks Summary

|Attack|Target|Defense|
|---|---|---|
|Exhaustive key search|Any cipher|Use large key sizes (≥128 bits)|
|Frequency analysis|Simple substitution|Use modern ciphers|
|Known plaintext|Simple substitution, others|Use secure modern ciphers|
|Chosen plaintext|Various|Use randomization, padding|
|Meet-in-the-middle|Double encryption|Use 3DES or AES|
|Forward search|Public key|Add random padding to messages|
|OTP depth attack|Reused OTP/stream key|Never reuse keys|
|Cut-and-paste|ECB mode|Use CBC or authenticated encryption|
|MITM on DH|Unauthenticated DH|Authenticate key exchange|
|Lattice reduction|Knapsack|Don't use knapsack (broken)|

### 5.1 Introduction to Cryptographic Hash Functions

Cryptographic hash functions are essential tools in information security, used for standard applications like digital signatures and message integrity, as well as non-standard uses like online bidding and spam reduction.

### 5.2 Definition and Properties

A cryptographic hash function, denoted as h(x), must satisfy several key properties:

- **Compression**: For any input x, the output h(x) is a small, fixed size (e.g., 160 bits).
    
- **Efficiency**: Computing h(x) must be relatively easy and fast for any input.
    
- **One-way (Pre-image Resistance)**: Given an output y, it is computationally infeasible to find an input x such that h(x)=y.
    
- **Weak Collision Resistance**: Given x, it is infeasible to find a different input y such that h(x)=h(y).
    
- **Strong Collision Resistance**: It is infeasible to find _any_ two distinct inputs x and y that produce the same hash value, h(x)=h(y).
    

#### Digital Signatures and Hashing

Hashing is used to make digital signatures efficient. Instead of signing a large message M, which is computationally expensive, Alice signs the hash of the message: S=[h(M)]Alice​. This "fingerprint" is small and identifies the message; if even one bit of M changes, the hash will change.

### 5.3 The Birthday Problem

The birthday problem is a probability concept fundamental to understanding hash function security:

- **Same Birthday as You**: In a room with N people, N must be 253 for a greater than 1/2 probability that someone shares _your_ specific birthday.
    
- **Any Two People Sharing a Birthday**: You only need N=23 people for a greater than 1/2 probability that _any_ two people share the same birthday.
    
- **Implication for Hashing**: For a hash function with an n-bit output (2n possible values), a collision can be expected after hashing approximately 2n/2 inputs. Consequently, a hash function must have roughly twice the bits of a symmetric cipher key to provide equivalent security against brute-force attacks.
    

### 5.4 Birthday Attack

A "Trudy" can exploit the birthday paradox to forge a digital signature:

1. Trudy creates an "evil" message E and an innocent message I.
    
2. She generates 2n/2 minor variations of both E and I that retain their original meanings.
    
3. She finds a collision where h(Ej​)=h(Ik​) and has Alice sign the innocent Ik​.
    
4. Because the hashes are identical, Alice’s signature on Ik​ is also valid for the evil Ej​.
    

### 5.5 Non-Cryptographic Hashes

Simple checksums and non-cryptographic hashes are unsuitable for security:

- **Summation/Modular Hashes**: These are weak because collisions are easy to construct (e.g., swapping bytes results in the same sum).
    
- **Cyclic Redundancy Check (CRC)**: Designed only to detect random transmission errors, not intentional tampering. An intelligent adversary can easily modify data to maintain the same CRC value.
    

### 5.6 Tiger Hash

Tiger is a cryptographic hash designed for 64-bit processors, producing a 192-bit output.

- **Design**: It uses S-boxes (mapping 8 bits to 64 bits) and a "key schedule" applied to the input blocks, borrowing principles from block ciphers like confusion and diffusion.
    
- **Structure**: It consists of 24 rounds, organized as three outer rounds with eight inner rounds each.
    
- **Avalanche Effect**: It is designed so that any small change in the input causes a large, uncorrelated change in the output.
    

### 5.7 HMAC (Hashed MAC)

Simply sending h(M) with a message does not provide integrity because an attacker can replace both M and h(M). To prevent this, a key K must be mixed into the hash.

- **Naive Approaches**: Both h(K,M) and h(M,K) are vulnerable to specific technical attacks (length extension or known collisions).
    
- **HMAC Standard (RFC 2104)**: The approved method uses a nested structure to thoroughly mix the key: HMAC(M,K)=H(K⊕opad,H(K⊕ipad,M)).
    

### 5.8 Other Uses for Hash Functions

- **Online Bids**: To ensure "sealed" bids, participants submit h(Bid) first. This commits them to a specific value without revealing it until all bids are in.
    
- **Spam Reduction**: Hash functions can be used to require a small amount of computational work (a "proof of work") before an email is accepted.
    
- **Information Hiding**: Includes digital steganography (hiding a message within a file) and digital watermarking.