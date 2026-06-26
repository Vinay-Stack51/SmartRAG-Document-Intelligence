import os
import sys

if __name__ == "__main__":
    if os.getenv("STREAMLIT_SERVER_PORT"):
        # Running on Streamlit Cloud; do nothing.
        pass
    else:
        os.execv(
            sys.executable,
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                os.path.join(os.path.dirname(__file__), "frontend", "app.py"),
            ],
        )
