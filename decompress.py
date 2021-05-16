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
            referenced_text = output[-offset_num:][:length_num]

            output.extend(referenced_text) # referenced_text is a list of bytes so we use extend to add each one to output

            # Reset length and offset
            length, offset = [], []
        elif inside_token:
            if scanning_offset:
                offset.append(char)
            else:
                length.append(char)
        else:
            output.append(char) # Add the character to our output

    
    return bytes(output)

if __name__ == "__main__":
    with open("andham-py.txt") as f:
        contents = f.read()
        print(decode(contents).decode(encoding))
