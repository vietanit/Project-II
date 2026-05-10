import subprocess
import base64
import os

def run_judge(submission):
    # 1. Đọc dữ liệu Testcase
    input_file = f"/data/testcases/{submission.problem.id}/input.txt"
    output_file = f"/data/testcases/{submission.problem.id}/output.txt"
    
    if not os.path.exists(input_file) or not os.path.exists(output_file):
        return "System Error", "Không tìm thấy bộ test"

    with open(input_file, "r") as f:
        input_data = f.read()
        
    with open(output_file, "r") as f:
        expected_output = f.read().strip()

    # 2. Thủ thuật Base64: Mã hóa mã nguồn để ném thẳng vào lệnh bash
    code_b64 = base64.b64encode(submission.code.encode('utf-8')).decode('utf-8')
    
    lang = submission.language
    time_limit = submission.problem.time_limit / 1000 # Giây
    mem_limit = submission.problem.memory_limit # MB
    
    # 3. Kịch bản chạy Sandbox cho từng ngôn ngữ
    if lang == 'cpp':
        image = "gcc:latest"
        filename = "main.cpp"
        cmd_script = f"echo '{code_b64}' | base64 -d > {filename} && g++ {filename} -o main && ./main"
        
    elif lang == 'python':
        image = "python:3.10-alpine"
        filename = "main.py"
        cmd_script = f"echo '{code_b64}' | base64 -d > {filename} && python {filename}"
        
    elif lang == 'java':
        image = "eclipse-temurin:17-alpine"
        filename = "Main.java" # Yêu cầu code Java phải dùng public class Main
        cmd_script = f"echo '{code_b64}' | base64 -d > {filename} && javac {filename} && java Main"
        
    else:
        return "System Error", f"Ngôn ngữ '{lang}' chưa được hỗ trợ"

    # Xây dựng lệnh tạo Container cách ly hoàn toàn
    docker_cmd = [
        "docker", "run", "-i", "--rm",
        "--network", "none",               # Chặn code user gọi ra internet
        "--memory", f"{mem_limit}m",       # Chặn code user ăn hết RAM
        "--cpus", "0.5",                   # Giới hạn dùng nửa nhân CPU
        image,
        "sh", "-c", cmd_script
    ]

    # 4. Thực thi và chấm điểm
    try:
        # Popen gửi dữ liệu input qua stdin của Docker container
        process = subprocess.run(
            docker_cmd,
            input=input_data,
            capture_output=True,
            text=True,
            timeout=time_limit + 2 # Cho phép hệ thống chậm 2s để khởi động container
        )
        
        # Nếu có lỗi trong quá trình biên dịch (compile) hoặc chạy (runtime)
        if process.returncode != 0:
            return "Compile/Runtime Error", process.stderr.strip()

        actual_output = process.stdout.strip()
        
        if actual_output == expected_output:
            return "Accepted", "Kết quả chính xác!"
        else:
            return "Wrong Answer", f"Mong đợi:\n{expected_output}\n\nThực tế:\n{actual_output}"

    except subprocess.TimeoutExpired:
        return "Time Limit Exceeded", "Chạy quá thời gian quy định"
    except Exception as e:
        return "System Error", str(e)