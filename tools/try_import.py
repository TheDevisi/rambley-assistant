def tryImport():
    try: 
        import flet as ft
        print("Successfully imported flet")
    except ImportError:
        print("Failed to import flet, installing it now...")
        os.system("pip install flet")
        import flet as ft


    try:
        import google.generativeai as genai
        print("Successfully imported google.generativeai")

    except ImportError:
        print("Failed to import google.generativeai, installing it now...")
        os.system("pip install google-generativeai")
        import google.generativeai as genai

    try:
        import pygame
        print("Successfully imported pygame")

    except ImportError:
        print("Failed to import pygame, installing it now...")
        os.system("pip install pygame")
        import pygame
    try:
        import edge_tts
        print("Successfully imported edge_tts")
    except ImportError:
        print("Failed to import edge_tts, installing it now...")
        os.system("pip install edge-tts")
        import edge_tts
    try:
        from rvc_python.infer import infer_file, infer_files

    except ImportError:
        os.system("pip install rvc-python")
        os.system("pip install tensorboardX")
        from rvc_python.infer import infer_file, infer_files