def cleanup(filename):
    proceed = input("Do you want to remove duplicate lines and format the file? (Y/N)").lower()
    
    if proceed == 'y':
        char_limit = 1000
        discord_nitro = input("Do you have Discord Nitro (not Basic)? (Y/N)").lower()
        if discord_nitro == 'y':
            char_limit = 2000

        with open(filename, 'r+') as file:
            # Use a set to keep track of unique lines
            unique_lines = set()

            # Keep track of the number of characters written so far
            char_count = 0

            # Iterate over each line in the file
            lines = file.readlines()
            file.seek(0)
            file.truncate()
            for line in lines:
                # Strip any whitespace from the beginning and end of the line
                line = line.strip()

                # Only write the line back to the file if it hasn't already been written
                if line not in unique_lines:
                    # Add the line to the set of unique lines
                    unique_lines.add(line)

                    # Add the length of the line to the character count
                    char_count += len(line)

                    # Write the line to the file
                    file.write(line + '\n')

                    # If we've written the character limit or more, add a blank line
                    if char_count >= char_limit:
                        file.write('\n')

                        # Reset the character count
                        char_count = 0
                else:
                    # If the line is a duplicate, don't count it towards the character count
                    continue

            # If the last line didn't end in a newline character, add one to ensure the file ends with a newline
            if lines[-1][-1] != '\n':
                file.write('\n')
    else:
        print("Operation cancelled.")
