import os
import shutil
import zipfile

PREFIX = "Egbuchiem-FelixOnuora_92133564_OOFPP_Habits"
ROOT = PREFIX

def run_packaging():
    phase1_dir = os.path.join(ROOT, "OOFPP_Habits_Phase1")
    phase2_dir = os.path.join(ROOT, "OOFPP_Habits_Phase2")
    phase3_dir = os.path.join(ROOT, "OOFPP_Habits_Phase3")

    for d in [phase1_dir, phase2_dir, phase3_dir]:
        os.makedirs(d, exist_ok=True)

    # Move phase 1 pdf
    if os.path.exists("Egbuchiem-FelixOnuora_92133564_OOFPP_Habits_Submission_Conception.pdf"):
        shutil.copy("Egbuchiem-FelixOnuora_92133564_OOFPP_Habits_Submission_Conception.pdf", phase1_dir)

    # Move phase 2 pdf
    if os.path.exists("Egbuchiem-FelixOnuora_92133564_OOFPP_Habits_Submission_Development.pdf"):
        shutil.copy("Egbuchiem-FelixOnuora_92133564_OOFPP_Habits_Submission_Development.pdf", phase2_dir)

    # Abstract PDF goes into Phase 3 alongside code
    if os.path.exists("Egbuchiem-FelixOnuora_92133564_OOFPP_Habits_Submission_Abstract.pdf"):
        shutil.copy("Egbuchiem-FelixOnuora_92133564_OOFPP_Habits_Submission_Abstract.pdf", phase3_dir)

    # Create inner ZIP containing the actual code and dependencies
    inner_zip_path = os.path.join(phase3_dir, f"{PREFIX}_Submission_Final.zip")
    with zipfile.ZipFile(inner_zip_path, 'w') as z:
        core_files = [
            "main.py", "habit.py", "analytics.py", 
            "test_habit.py", "test_analytics.py", "test_data_generator.py", 
            "README.md", "habits.json", 
            "Egbuchiem-FelixOnuora_92133564_OOFPP_Habits_Submission_Conception.md",
            "generate_pdf.py", "generate_presentation.py", "generate_abstract.py", "packager.py"
        ]
        for f in core_files:
            if os.path.exists(f):
                z.write(f)

    # Zip the outermost directory
    shutil.make_archive(PREFIX, 'zip', ".", ROOT)
    print("Packaging completely and perfectly finished!")

if __name__ == '__main__':
    run_packaging()
