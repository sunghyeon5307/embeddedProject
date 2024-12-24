import os

def rename_files_sequentially(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # 파일을 순차적으로 번호를 매기기
    for index, filename in enumerate(files, start=1):
        file_path = os.path.join(folder_path, filename)
        
        # 새 파일 이름 생성 (1, 2, 3, ...)
        new_filename = f"{index}{os.path.splitext(filename)[1]}"  
        new_file_path = os.path.join(folder_path, new_filename)
        
        # 파일 이름 변경
        os.rename(file_path, new_file_path)
        print(f"파일 이름 변경: {file_path} -> {new_file_path}")

# 사용 예시
folder_path = "/Users/bagseonghyeon/Documents/융합프로젝트/face/dataset/surprise" 
rename_files_sequentially(folder_path)