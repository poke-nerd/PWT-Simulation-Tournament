import os


def delete_error_files(directory="Tour100"):
    deleted_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "Error:" in content:
                        os.remove(file_path)
                        deleted_files.append(filename)
            except Exception as e:
                print(f"⚠️ Could not read {filename}: {e}")

    print(f"✅ Deleted {len(deleted_files)} files containing 'Error:'")
    if deleted_files:
        print("🗑️ Files removed:")
        for f in deleted_files:
            print(" -", f)


if __name__ == "__main__":
    delete_error_files()

