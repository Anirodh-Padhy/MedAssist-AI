# =========================================================
# PATIENT MEMORY SYSTEM
# =========================================================

def build_patient_memory(history):

    if not history:

        return "No previous patient history."

    memory = []

    for item in history[-5:]:

        question = item[0]

        memory.append(question)

    return "\n".join(memory)