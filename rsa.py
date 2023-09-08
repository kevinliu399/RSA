"""
Kevin Liu Student ID: 2130352
Project Part 1 
Completing the first part of the RSA project which is to develop the number theoretic tools required to encrypt and decrypt integers
"""
 
from math import *
import random
 
 
def check_prime(n: int):
    """This function uses trial division to check if the number n is prime. If n is prime, return True. If n is not
    prime, return False."""
    if n < 2:
        return False
    sqrt = isqrt(n)
    for i in range(2, sqrt + 1):
        if n % i == 0:
            return False
    return True
 

  
def two_primes(a: int):
    """This function randomly selects distinct primes of size about 2^a."""
    i = 2 ** (a - 1)
    j = 2 ** a
    p = random.randint(i, j)
    while not check_prime(p):
        p = random.randint(i, j)
    q = random.randint(i, j)
    while not check_prime(q):
        q = random.randint(i, j)
    return p, q
 
 
def generate_key(p:int, q:int):
    """
    This function generates the public and private keys for the RSA project by taking two distinct prime numbers. 
    """
    m = p * q
 
    def _gcd(p,q):
        while q != 0:
            p, q = q, p%q
        return p
    phi_m = len([i for i in range(1,m) if _gcd(i,m)==1])
 
    k = random.randint(2, phi_m - 1)
    while _gcd(k, phi_m) != 1:
        k = random.randint(2, phi_m - 1)
 
    e = pow(k, -1, phi_m)
 
    return ((m,k), (p,q,e))
 
 
def decrypt (private_key: tuple[int , int , int], encrypted_message: int):
    """ This function decrypts an encrypted message using the given private key . The
    message input into this encrypted message should be one block from a possibly
    longer encrypted message . """
    m = private_key[0] * private_key[1]
 
    message = pow(encrypted_message, private_key[2], m)
 
    return message
 
 
 
def encrypt(public_key: tuple[int , int], message: int ):
    """ This function encrypts a message using the given public key . The message
    input into this message should be one block from a possibly longer message ."""
 
    encrypted_message = pow(message, public_key[1], public_key[0])
 
    return encrypted_message


from math import isqrt
import random
 
def check_prime(n: int):
    """ This function uses trial division to check if the number n is prime . If
n is prime , return True . If n is not prime , return False ."""
 
    sqrt_n = isqrt(n)
    if n == 2 or n == 3:
        return True
    elif n == 1:
        return False
    elif n > 1:
        for i in range(2,sqrt_n+1):
            if n % i == 0:
                return False
    return True
 
 
def two_primes(a):
    """Randomly select two distinct primes of size about 2^a."""
    while True:
        p = random.randint(2**(a-1), 2**a) #Random integers from 2**(a-1), 2**a
        if check_prime(p):
            break
    while True:
        q = random.randint(2**(a-1), 2**a) #Random integers from 2**(a-1), 2**a
        if check_prime(q) and p != q:
            break
    return p, q
 
 
 
def generate_key(p:int, q:int):
    """ This key generating function takes two primes p and q and returns a tuple of
two tuples . The first tuple is the public key (m, k) and the second tuple is
the private key (p, q, e)."""
 
    m = p * q
 
    def _gcd(p,q): #Helper function to find gcd
        while q != 0:
            p, q = q, p%q
        return p
    phi_m = len([i for i in range(1,m) if _gcd(i,m)==1]) #Phi m is basically the length of this list 
 
    k = random.randint(2, phi_m - 1)
    while _gcd(k, phi_m) != 1:
        k = random.randint(2, phi_m - 1)
 
    e = pow(k, -1, phi_m)
 
    return ((m,k), (p,q,e)) #Private, Public
 
 
def decrypt (private_key: tuple[int , int , int], encrypted_message: int):
    """ This function decrypts an encrypted message using the given private key . The
    message input into this encrypted message should be one block from a possibly
    longer encrypted message . """
    m = private_key[0] * private_key[1] #p * q
 
    message = pow(encrypted_message, private_key[2], m)
 
    return message
 
 
 
def encrypt(public_key: tuple[int , int], message: int ):
    """This function encrypts a message using the given public key. The message input into this message should be one block from a possibly longer message ."""
 
    encrypted_message = pow(message, public_key[1], public_key[0])
 
    return encrypted_message
 
 
def encrypt_text_to_integer_blocks(public_key: tuple[int, int, int], message: str, block_length: int):
    """ This function converts a typed message into a list of encrypted blocks . If
someone wants to send Alice a secret message , this function returns what they
should send . """
 
    in_unicode = []
 
    for letter in message:
        in_unicode.append(str(ord(letter)).zfill(3)) #Fill 0s with unicode 
    
    message = "".join(in_unicode) #Make it into a string
    
    blocks = []
    # splits the message into blocks of the specified length
    #If the message length is not a multiple of the block length, it adds a final block with the remaining characters
 
    while len(message) > block_length: 
        blocks.append(message[:block_length])
        message = message[block_length:]
 
    if len(message) > 0: 
        blocks.append(message)
    
    int_form = [int(i) for i in blocks] #Convert to int
    
    encrypted_mesage = []
 
    for i in int_form: #Encrypt
        encrypted = encrypt(public_key[:2], i)
        encrypted_mesage.append(encrypted)
 
    return encrypted_mesage
 
 
 
 
def decrypt_integer_blocks_to_text(private_key: tuple[int, int, int], encrypted_message: list[int], block_length: int):
    """ This function takes a list of encrypted integers , decrypts them , and then converts them to text using UTF -8.
    This is what Alice will see once she decrypts Bob’s message ."""

    # Decrypt list
    decrypted_list = []
    for block in encrypted_message:
        decrypted_list.append(decrypt(private_key, block))

    a = decrypted_list.pop()
    b = len(decrypted_list)
    c = len(str(a))
    if (b * 4 + c) % 3 == 0:
        b = str(a)
    elif (b * 4 + c) % 3 == 2:
        b = '0' + str(a)
    else:
        b = '00' + str(a)
    decrypted_message_string = [str(x).zfill(4) for x in decrypted_list]
    # convert to string and pad all blocks (except last one) to full length
    decrypted_message_string.append(b)

    # Concatenate
    number_message = ""
    for i in decrypted_message_string:
        number_message += str(i)

    # Numbers to string
    final_message = ""
    while number_message:
        block = number_message[:block_length - 1]
        final_message += chr(int(block))
        number_message = number_message[block_length - 1:]

    return final_message

 
 
 
 
def menu():
    """
    Menu of the system. Gives the user the choices to either encrypt, decrypt or set up RSA encryption.
    """
    using_menu = True
    while using_menu:
 
        user_choice = input("""\nPlease Select Your Choice by pressing entering 1,2,3 or 4 in the terminal
        
        1. You have your public key and a message that you wish to encrypt        
        2. You have a private key and you would like to decrypt a message
        3. You need help setting up RSA
        4. Exit the application
        
        """)
 
        if user_choice == "1":
            print("\n You have chosen choice 1, encrypting a message with your public key\n")
 
            while True:
                public_key_str = input("Please enter your public key with this format: (m,k) where m and k are integers (Make sure to include the parentheses)\n")
                public_key_ls = public_key_str.split(",")
 
                #Remove parentheses and any extra spaces
                m = public_key_ls[0][1:]
                m = m.strip()
                k = public_key_ls[1][:-1]
                k = k.strip()
 
                valid_input = (m.isdigit() and k.isdigit()) #Checks whether the input is valid, if not it will loop 
                
                if valid_input:
                    break
            
            public_key_ls = [int(m),int(k)]
 
            while True: #Exits the ult when the user decides so
                message_to_encrypt = input("\nPlease enter the message that you wish to encrypt: ")
                
                while True: #Only accepts valid inputs (Integers)
                    block_length = input("How would you like your block length? ")
                    valid_input2 = block_length.isdigit()
                    if valid_input2:
                        break
 
                block_length_int = int(block_length)
                encrypted_message = encrypt_text_to_integer_blocks(public_key_ls, message_to_encrypt, block_length_int)
                print(f"Your encrypted message: {encrypted_message}")
 
 
                another = input("Would you like to encrypt another message using the same public key? Type 'Yes' to do it again and 'No' to exit to the menu\n")
                if another.i() == "no":
                    break
                elif another.i() == "yes":
                    print("")
                else:
                    print("Please enter a valid input\n")
                    break
 
 
        elif user_choice == "2":
            print("\n You have chosen choice 2, decrypting a message with your private key\n")
            while True:#Loop ends when the input is valid
 
                private_key_str = input("\nPlease enter your public key with this format: (p,q,e) where p q and e are integers (Make sure to include the parentheses)\n")
                private_key_ls = private_key_str.split(',')
 
                #For formatting purposes
                p = private_key_ls[0][1:]
                p = p.strip()
                q = private_key_ls[1]
                q = q.strip()
                e = private_key_ls[2][:-1]
                e = e.strip()
 
                valid_input = (p.isdigit() and q.isdigit() and e.isdigit())
                if valid_input:
                    break
 
            private_key_ls = [int(p), int(q), int(e)]
 
            while True: #Loops until the user decides so
                message_to_decrypt = input("\nPlease enter the message that you wish to decrypt: ")
                message_to_decrypt = message_to_decrypt[1:]
                message_to_decrypt = message_to_decrypt[:-1]
 
                message_to_decrypt_ls = message_to_decrypt.split(",")
                message_to_decrypt_ls = [i.strip() for i in message_to_decrypt_ls]
                message_to_decrypt_ls = [int(i) for i in message_to_decrypt_ls]
 
 
                while True: #Similar
                    block_length = input("How would you like your block length? ")
                    valid_input = block_length.isdigit()
                    if valid_input:
                        break
                
                block_length = int(block_length)
                decrypted_message = decrypt_integer_blocks_to_text(private_key_ls, message_to_decrypt_ls, block_length)
                print(f"The decrypted message: {decrypted_message}")
 
                another = input("Would you like to decrypt another message using the same private key? Type 'Yes' to do it again and 'No' to exit to the menu\n")
                if another.i() == "no":
                    break
                elif another.i() == "yes":
                    print("")
                else:
                    print("Please enter a valid input\n")
                    break
    
        elif user_choice == "3":
            print("You have chosen choice 3, assisting you with your RSA")
 
            choose_or_give = input("Type 'Me' to choose two prime numbers yourself and 'Give' if you would like two randomly generated prime numbers \n")
 
            if choose_or_give.i() == "me":
 
                while True:
                    prime1 = input("Enter a prime number: ")
                    
                    if prime1.isdigit():
                        prime1_int = int(prime1)
                        valid_p1 = check_prime(prime1_int)
                        if not valid_p1 or prime1 == '1':
                            print("Please enter another number as your last was either not prime or 1")
                        else:
                            break
                    else:
                        print("Please enter a valid integer")
 
 
 
                while True:
                    prime2 = input("Enter a prime number: ")
 
                    if prime2.isdigit():
                        prime2_int = int(prime2)
                        valid_p2 = check_prime(prime2_int)
                        if not valid_p2 or prime2 == '1':
                            print("Please enter another number as your last was either not prime or 1")
                        else:
                            break
                    else:
                        print("Please enter a valid integer")
 
                
                print(f"You have chosen {prime1}, and {prime2}. Now, the program is going to generate a public key and a private key based on your choice")
                keys = generate_key(prime1_int, prime2_int)
                print(f"     \nKeys generated!\n Your public key is {keys[0]}\n Your private key is {keys[1]}")
                print("\n Now that your keys are generated, you can use them to either decrypt or encrypt a message \n You can do it with this application by choosing option 1 or 2 in the menu \n")
 
            elif choose_or_give.i() == "give":
                print("You have chosen the option to generate two random prime numbers")
                print("Because of the density of the primes, the program should be able to generate two primes between 2^ (a - 1) and 2 · 2^ (a-1) = 2^a.")
 
                
                
                while True: #Gets out of loop when conditions are satisfied 
 
                    a_val = input("What 'a' value would you want? ")
 
                    if a_val.isdigit(): #Valid input
                        a_val = int(a_val)
 
                        if a_val < 3:
                            print("Enter a larger a value (Bigger than 3)")
                        elif a_val > 15:
                            print("Enter a smaller a value (Smaller than 15)")
 
                        else:
                            break
                        
                    
 
                prime1,prime2 = two_primes(a_val)
 
                print(f"The two generated primes are {prime1} and {prime2}")
                keys = generate_key(prime1, prime2)
                print(f"     \nKeys generated!\n Your public key is {keys[0]}\n Your private key is {keys[1]}")
                print("\n Now that your keys are generated, you can use them to either decrypt or encrypt a message \n You can do it with this application by choosing option 1 or 2 in the menu \n")
            
            else:
                print("Please enter a valid input")
 
        elif user_choice == "4":
            print("\nThank you for using RSA encryption/decryption, see you next time!\n")
            break
 
        else: print("\n Please enter a valid input\n")
 
                    
                    
if __name__ == '__main__':
    menu()