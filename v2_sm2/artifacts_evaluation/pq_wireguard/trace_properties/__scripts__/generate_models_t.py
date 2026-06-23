#!/usr/bin/env python3.6
'''
Artifacts for Usenix 2025 paper "A Tale of Two Worlds, a Formal Story of WireGuard Hybridization"
'''


# Define the expression as a string
data = "Rs & (Ka | Ki | Ra) & (Ka | Ki | Tr)"

# Find the position of the first '&'
pos = data.find('&')

# Remove everything before (and including) the first '&'
if pos != -1:
    simp = data[pos + 1:].strip()
else:
    # If no '&' is found, return the original expression (or handle as needed)
    simp = data

# Print the simplified expression
print(f"Simplified Expression: {simp}")
