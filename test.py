import os

class FileReader:
    def __init__(self, directory_path):
        self.directory_path = directory_path

    def read_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def load_data(self):
        documents = []
        for filename in os.listdir(self.directory_path):
            file_path = os.path.join(self.directory_path, filename)
            if os.path.isfile(file_path):
                content = self.read_file(file_path)
                documents.append({
                    'filename': filename,
                    'content': content,
                })
        return documents

# Example usage
file_reader = FileReader('c:/Users/promact.DESKTOP-RHBFB7T/Documents')
documents = file_reader.load_data()

for document in documents:
    print(f"Filename: {document['filename']}")
    print(f"Content: {document['content'][:200]}...")  # Print the first 200 characters
