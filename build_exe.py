import os
import platform
import subprocess
import sys

def build_executable():
    """
    使用PyInstaller打包程序为可执行文件
    支持macOS和Windows系统
    """
    # 确保已安装所需依赖
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # 根据操作系统设置输出文件名
    is_mac = platform.system() == "Darwin"
    output_name = "发票处理工具"
    
    # PyInstaller命令行参数
    pyinstaller_args = [
        "pyinstaller",
        "--noconfirm",  # 覆盖输出目录
        "--clean",      # 清理临时文件
        f"--name={output_name}",  # 输出文件名
        "--onefile",    # 打包成单个文件
    ]
    
    # Windows特定配置
    if not is_mac:
        pyinstaller_args.append("--noconsole")  # Windows下不显示控制台窗口
    
    # 添加数据文件
    pyinstaller_args.append(f"--add-data=README.md{':.' if is_mac else ';.'}")
    
    # 添加主程序文件
    pyinstaller_args.append("extract_invoice.py")
    
    # 执行打包命令
    subprocess.check_call(pyinstaller_args)
    
    print("\n打包完成！")
    if is_mac:
        executable_path = f"dist/{output_name}"
        print(f"可执行文件位置：{executable_path}")
        # 添加执行权限
        if os.path.exists(executable_path):
            os.chmod(executable_path, 0o755)
            print("已添加执行权限")
    else:
        print(f"可执行文件位置：dist/{output_name}.exe")

if __name__ == "__main__":
    build_executable() 