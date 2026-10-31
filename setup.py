"""setup.py —— 仅用于在 pip install 后把 Python Scripts 目录加入用户 PATH。"""
from __future__ import annotations

import os
import sys

from setuptools import setup
from setuptools.command.install import install


def _add_scripts_to_user_path() -> None:
    """把当前 Python 的 Scripts 目录追加到用户 PATH（持久化到注册表）。"""
    if sys.platform != "win32":
        return

    scripts_dir = os.path.join(os.path.dirname(sys.executable), "Scripts")
    if not os.path.isdir(scripts_dir):
        return

    try:
        import winreg

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ
        ) as key:
            current_path, _ = winreg.QueryValueEx(key, "Path")

        paths = [p for p in current_path.split(";") if p]
        if scripts_dir.lower() in [p.lower() for p in paths]:
            print(f"[conv] Scripts 已在 PATH 中: {scripts_dir}")
            return

        paths.append(scripts_dir)
        new_path = ";".join(paths)

        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_SET_VALUE
        ) as key:
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)

        # 通知系统环境变量已变更（新打开的终端会生效）
        try:
            import ctypes

            ctypes.windll.user32.SendMessageTimeoutW(
                0xFFFF, 0x001A, 0, "Environment", 0, 5000, None
            )
        except Exception:
            pass

        print(f"[conv] 已添加到用户 PATH: {scripts_dir}")
        print("[conv] 请重开终端使 conv 命令生效。")
    except Exception as e:
        print(f"[conv] 自动添加 PATH 失败: {e}")


class ConvInstall(install):
    def run(self):
        super().run()
        _add_scripts_to_user_path()


setup(cmdclass={"install": ConvInstall})
