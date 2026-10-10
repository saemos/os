import os
import sys
import sqlite3
import subprocess
from llama_cpp import Llama

# 1. INITIALIZE MEMORY DATABASE (Cognitive State Storage)
class MemoryOS:
    def __init__(self, db_path="cognitive_memory.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT,
                code TEXT,
                status TEXT
            )
        ''')
        self.conn.commit()

    def store(self, prompt, code, status):
        self.cursor.execute("INSERT INTO memory (prompt, code, status) VALUES (?, ?, ?)", (prompt, code, status))
        self.conn.commit()

# 2. TOOL RUNTIME (Compilers & Interpreters)
class ExecutionEnvironment:
    @staticmethod
    def run_code(code: str, lang: str):
        if lang == "python":
            with open("temp.py", "w") as f:
                f.write(code)
            res = subprocess.run([sys.executable, "temp.py"], capture_output=True, text=True)
            return res.returncode == 0, res.stdout or res.stderr

        elif lang in ["c", "cpp"]:
            ext = "c" if lang == "c" else "cpp"
            compiler = "gcc" if lang == "c" else "g++"
            with open(f"temp.{ext}", "w") as f:
                f.write(code)
            
            # Compile step
            compile_res = subprocess.run([compiler, f"temp.{ext}", "-o", "temp.out"], capture_output=True, text=True)
            if compile_res.returncode != 0:
                return False, f"Compilation Error:\n{compile_res.stderr}"
            
            # Run step
            run_res = subprocess.run(["./temp.out"], capture_output=True, text=True)
            return True, run_res.stdout

        return False, "Unsupported Language"

# 3. COGNITIVE REASONING LOOP (The AI Bot)
class CognitiveBot:
    def __init__(self, model_path="model.gguf"):
        print("Loading 1GB Cognitive Model into System Memory...")
        self.llm = Llama(model_path=model_path, n_ctx=2048, verbose=False)
        self.memory = MemoryOS()
        self.env = ExecutionEnvironment()

    def generate_code(self, prompt, lang, error_log=""):
        system_prompt = f"""You are a precise Cognitive Coding AI specializing in {lang}.
Output ONLY executable code without markdown commentary or extra explanation.
"""
        user_prompt = f"Task: {prompt}\nLanguage: {lang}"
        if error_log:
            user_prompt += f"\nPrevious Code Failed With Error:\n{error_log}\nFix the error."

        output = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2
        )
        
        # Extract response and clean triple backticks
        raw_text = output['choices'][0]['message']['content']
        cleaned_code = raw_text.replace("```" + lang, "").replace("```", "").strip()
        return cleaned_code

    def execute_cognitive_cycle(self, task, lang="python", max_retries=3):
        print(f"\n[Cognitive OS] Planning Task: '{task}' in {lang.upper()}")
        error_context = ""
        
        for attempt in range(1, max_retries + 1):
            print(f"[Attempt {attempt}/{max_retries}] Generating Code...")
            code = self.generate_code(task, lang, error_context)
            print(f"--- Generated Code ---\n{code}\n----------------------")
            
            # Execute & Evaluate
            success, output = self.env.run_code(code, lang)
            
            if success:
                print(f"[SUCCESS] Code Executed Perfectly:\n{output}")
                self.memory.store(task, code, "SUCCESS")
                return code
            else:
                print(f"[REFLECTION] Execution Failed:\n{output}")
                error_context = output
                self.memory.store(task, code, "FAILED")

        print("[Cognitive OS] Max retries reached. Unable to self-heal.")
        return None

# RUN THE SYSTEM
if __name__ == "__main__":
    bot = CognitiveBot("model.gguf")
    
    # Test C++ Code Generation with Self-Correction
    bot.execute_cognitive_cycle(
        task="Write a C++ program that initializes a vector of integers, prints the sum, and outputs the result.",
        lang="cpp"
    )
