import subprocess

def auto_push_evolution(commit_message="AI cognitive OS self-update"):
    """Pushes newly learned states or code tweaks back to GitHub automatically."""
    try:
        subprocess.run(["git", "add", "."], check=True)
        # Check if there are changes to commit
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if status.stdout.strip():
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("[Evolution] Successfully synced new intelligence state to GitHub!")
        else:
            print("[Evolution] No structural changes to push.")
    except Exception as e:
        print(f"[Evolution Error] Git sync failed: {e}")

if __name__ == "__main__":
    auto_push_evolution("Trained on new C++/Python notes")
