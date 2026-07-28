# Window Pin Overlay

A lightweight Windows overlay button for toggling always-on-top windows.

## 使用方法

1. 运行 `钉子插件.exe`。
2. 切换到需要置顶的应用窗口，钉子显示在标题栏右侧。
3. 单击灰色钉子置顶，钉子变蓝；再次单击取消置顶。
4. 右键钉子并选择“退出钉子”可结束程序。

钉子不会显示在桌面、任务栏或通知区域。程序仅调用 Windows 窗口置顶接口，不联网，也不会读取或上传个人文件。

## 运行环境

- Windows 10 或 Windows 11 64 位
- 使用发布版 EXE 无需安装 Python 或运行库

## 从源码构建

安装 Python 和 PyInstaller 后，在项目目录运行：

```powershell
python -m PyInstaller --onefile --noconsole --name "钉子插件" --distpath . --clean "钉子插件.pyw"
```

构建结果为根目录的 `钉子插件.exe`。

## 许可证

本项目采用 [MIT License](LICENSE)。
