import sys

encoding = "utf-8"

def decode(text):
	
    text_bytes = text.encode(encoding) # The text encoded as bytes
    output = [] # The output characters

    inside_token = False
    scanning_offset = True

    length = [] # Length number encoded as bytes
    offset = [] # Offset number encoded as bytes

    for char in text_bytes:
        if char == "<".encode(encoding)[0]:
            inside_token = True # We're now inside a token
            scanning_offset = True # We're now looking for the length number
        elif char == ",".encode(encoding)[0] and inside_token:
            scanning_offset = False
        elif char == ">".encode(encoding)[0]:
            inside_token = False # We're no longer inside a token

            # Convert length and offsets to an integer
            length_num = int(bytes(length).decode(encoding))
            offset_num = int(bytes(offset).decode(encoding))

            # Get text that the token represents
            back_ref = output[-offset_num:][:length_num]
            back_ref_text = bytes(back_ref).decode(encoding)

            output.extend(back_ref) # back_ref is a list of bytes so we use extend to add each one to output
            output_text = bytes(output).decode(encoding)

            # Reset length and offset
            length, offset = [], []
        elif inside_token:
            if scanning_offset:
                offset.append(char)
            else:
                length.append(char)
        else:
            output.append(char) # Add the character to our output
            output_text = bytes(output).decode(encoding)
            output_text = output_text

    
    return bytes(output)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(decode(sys.stdin.read()).decode(encoding))        
    else:
        with open(sys.argv[1]) as f:
            print(decode(f.read()).decode(encoding))
