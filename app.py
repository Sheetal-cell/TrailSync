from app import create_app
app = create_app()
if __name__ == "__main__":
    app.run(debug=True)
    print("Starting app...")

from app import create_app

print("Imported create_app")

app = create_app()

print("Created app")

if __name__ == "__main__":
    print("Running server...")
    app.run(debug=True)