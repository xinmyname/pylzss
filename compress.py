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

def encode(text, max_sliding_window_size=4096):
    text_bytes = text.encode(encoding)

    search_buffer = [] # Array of integers, representing bytes
    check_characters = [] # Array of integers, representing bytes
    output = [] # Output array

    i = 0
    moved_past = 0

    for char in text_bytes:

        if elements_in_array_plus_char(check_characters, char, search_buffer) == -1 or i == len(text_bytes) - 1:
            if i == len(text_bytes) - 1 and elements_in_array_plus_char(check_characters, char, search_buffer) != -1:
                # Only if it's the last character then add the next character to the text the token is representing
                check_characters.append(char)
            
            if len(check_characters) > 1:
                index = elements_in_array(check_characters, search_buffer)
                offset = i - index - len(check_characters) - moved_past # Calculate the relative offset
                length = len(check_characters) # Set the length of the token (how many character it represents)

                token = f"<{offset},{length}>" # Build our token

                if len(token) > length:
                    # Length of token is greater than the length it represents, so output the characters
                    output.extend(check_characters) # Output the characters
                else:
                    output.extend(token.encode(encoding)) # Output our token
                
                search_buffer.extend(check_characters) # Add the characters to our search buffer   
            else:
                output.extend(check_characters) # Output the character  
                search_buffer.extend(check_characters) # Add the characters to our search buffer   

            check_characters = []   
        
        check_characters.append(char)

        if len(search_buffer) > max_sliding_window_size: # Check to see if it exceeds the max_sliding_window_size
            diff = len(search_buffer) - max_sliding_window_size
            moved_past += diff
            search_buffer = search_buffer[diff:] # Remove the first element from the search_buffer

        i += 1
    
    return bytes(output)

if __name__ == "__main__":

    with open("greeneggs.txt") as f:
        contents = f.read()
        print(encode(contents, 256).decode(encoding))
