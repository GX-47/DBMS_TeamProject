import os

def read_files_in_folder(folder_path):
    combined_content = ""
    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.py') or filename.endswith('.sql'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r') as file:
                    relative_path = os.path.relpath(file_path, folder_path)
                    combined_content += f"# {relative_path}\n"
                    combined_content += file.read()
                    combined_content += "\n\n"
    return combined_content

def save_to_single_file(content, output_file):
    with open(output_file, 'w') as file:
        file.write(content)

def main():
    folder_path = 'D:/PES Academy/Sem 5/Database Management Systems/Mini Project/DBMS_TeamProject/src'  # Replace with the path to your folder
    output_file = 'combined_output.txt'  # Replace with the desired output file name
    combined_content = read_files_in_folder(folder_path)
    save_to_single_file(combined_content, output_file)
    print(f"Combined content saved to {output_file}")

if __name__ == "__main__":
    main()