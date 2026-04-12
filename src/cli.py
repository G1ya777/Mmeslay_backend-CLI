import argparse
import os
import warnings
import subprocess


warnings.filterwarnings("ignore")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--gradio", action="store_true", help="Launch gradio UI")
    parser.add_argument("--server", action="store_true", help="Launch flask server")
    parser.add_argument("--test", action="store_true", help="Launch test")
    parser.add_argument("--infer", help="Path to audio file for infernace")
    parser.add_argument("--audio_location", help="Path to audio files")
    args = parser.parse_args()

    if args.gradio:
        subprocess.run(["python", "src/gradio_app.py"])

    if args.infer:
        if not os.path.exists(args.infer):
            print(f"File not found: {args.infer}")
            return
        from inference_file import inference

        result = inference(args.infer)
        print(result)
    if args.test:
        if args.audio_location:
            if not os.path.exists(args.audio_location):
                print(f"Folder not found: {args.audio_location}")
                return
            os.environ["AUDIO_LOCATION"] = args.audio_location
            subprocess.run(["python", "src/model_test.py"])
        else:
            print("Missings option --audio_location")
    if args.server:
        subprocess.run(["python", "src/flask_server.py"])


if __name__ == "__main__":
    main()
