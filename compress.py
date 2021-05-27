import sys

def elements_in_array_plus_char(check_elements, char, elements):
    i = 0
    offset = 0

    if char != -1:
        check_elements = check_elements + [char]

    for element in elements:
        if len(check_elements) <= offset:
            # All of the elements in check_elements are in elements
            return i - len(check_elements)
        
        if check_elements[offset] == element:
            offset += 1
        else:
            offset = 0

        i += 1
    return -1

def elements_in_array(check_elements, elements):
    return elements_in_array_plus_char(check_elements, -1, elements)

encoding = "utf-8"

def encode(text, max_sliding_window_size=255):
    text_bytes = text.encode(encoding)

    search_buffer = [] # Array of integers, representing bytes
    check_characters = [] # Array of integers, representing bytes
    output = [] # Output array

    i = 0
    moved_past = 0

    for char in text_bytes:

        search_buffer_text = bytes(search_buffer).decode(encoding)

        if elements_in_array_plus_char(check_characters, char, search_buffer) == -1 or i == len(text_bytes) - 1:
            if i == len(text_bytes) - 1 and elements_in_array_plus_char(check_characters, char, search_buffer) != -1:
                # Only if it's the last character then add the next character to the text the token is representing
                check_characters.append(char)
                check_characters_text = bytes(check_characters).decode(encoding)
            
            if len(check_characters) > 1:
                index = elements_in_array(check_characters, search_buffer)

                len_sb = len(search_buffer)
                len_cc = len(check_characters)
                pos = len(search_buffer)-index

                offset = len(search_buffer)-index # Calculate the relative offset
                length = len(check_characters) # Set the length of the token (how many character it represents)
                token = f"<{offset},{length}>" # Build our token
                search_buffer
                found_characters = search_buffer[-offset:][:length]
                found_characters_text = bytes(found_characters).decode(encoding)
                output.extend(token.encode(encoding)) # Output our token
                output_text = bytes(output).decode(encoding)
                search_buffer.extend(check_characters) # Add the characters to our search buffer   


            else:
                output.extend(check_characters) # Output the character  
                output_text = bytes(output).decode(encoding)
                search_buffer.extend(check_characters) # Add the characters to our search buffer   

            check_characters = []
            check_characters_text = bytes(check_characters).decode(encoding)
   
        
        check_characters.append(char)
        check_characters_text = bytes(check_characters).decode(encoding)

        if len(search_buffer) > max_sliding_window_size: # Check to see if it exceeds the max_sliding_window_size
            diff = len(search_buffer) - max_sliding_window_size
            moved_past += diff
            search_buffer = search_buffer[diff:] # Remove the first element from the search_buffer

        i += 1

    if len(check_characters) > 0:
        output.extend(check_characters)
        output_text = bytes(output).decode(encoding)
    
    return bytes(output)

if __name__ == "__main__":

    window_size = 255

    if len(sys.argv) < 2:
        print(encode(sys.stdin.read(), window_size).decode(encoding))
    else:
        with open(sys.argv[1]) as f:
            print(encode(f.read(), window_size).decode(encoding))
