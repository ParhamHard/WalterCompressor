import math
import itertools
import hashlib

def sha256_hash(data):
    """
    Compute SHA-256 hash of the input data
    
    Args:
        data: Input string to be hashed
        
    Returns:
        hex string representing the SHA-256 hash
    """
    # Create a new sha256 hash object
    sha256 = hashlib.sha256()
    
    # Update the hash object with the bytes of the data
    if isinstance(data, str):
        data = data.encode('utf-8')
    sha256.update(data)
    
    # Return the hexadecimal digest
    return sha256.hexdigest()

# Example usage
if __name__ == "__main__":
    test_string = "Hello, world!"
    print(f"SHA-256 hash of '{test_string}':")
    print(sha256_hash(test_string))

class QRGenerator:
    """
    Basic QR Code generator (simplified version)
    Note: This is a simplified implementation - real QR codes use complex error correction
    and encoding schemes (like Reed-Solomon codes) which we won't implement here.
    """
    
    def __init__(self, data):
        self.data = data
        self.version = 1  # Simplest QR version
        self.size = 21  # Version 1 QR code size (21x21)
        self.modules = [[False for _ in range(self.size)] for _ in range(self.size)]
        
    def add_finders(self):
        """Add finder patterns (those big squares in corners)"""
        # Positions for version 1 QR
        positions = [(0, 0), (0, self.size-7), (self.size-7, 0)]
        
        for x, y in positions:
            for i in range(7):
                for j in range(7):
                    # Outer square
                    if i == 0 or i == 6 or j == 0 or j == 6:
                        self.modules[x+i][y+j] = True
                    # Inner square
                    elif 2 <= i <=4 and 2 <= j <=4:
                        self.modules[x+i][y+j] = True
                    # Empty space between
                    else:
                        self.modules[x+i][y+j] = False
    
    def add_data(self):
        """Very basic data encoding (doesn't follow QR specs)"""
        binary_str = ''.join(format(ord(c), '08b') for c in self.data)
        x, y = 8, 20  # Starting position
        
        for bit in binary_str:
            if x < self.size and y < self.size:
                self.modules[y][x] = bit == '1'
                x += 1
                if x >= self.size - 1:  # Simple zig-zag pattern
                    x = 8
                    y -= 1
                    if y < 0:
                        break
    
    def render(self):
        """Simple console-friendly rendering"""
        output = []
        for row in self.modules:
            line = []
            for module in row:
                line.append('██' if module else '  ')
            output.append(''.join(line))
        return '\n'.join(output)
    
    def generate(self):
        """Generate the complete QR code"""
        self.add_finders()
        self.add_data()
        return self.render()

def generate_qr(data, output_console=True):
    """
    Generate a basic QR code from input data
    
    Args:
        data: String to encode (short strings work best)
        output_console: If True, prints QR to console
    Returns:
        The QR code as a string (console representation)
    """
    qr = QRGenerator(data)
    result = qr.generate()
    if output_console:
        print(result)
    return result

# Example usage
if __name__ == "__main__":
    print("Simple QR Code Generator")
    text = input("Enter text to encode (short messages work best): ")
    generate_qr(text)

