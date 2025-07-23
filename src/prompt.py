from langchain.schema import HumanMessage, SystemMessage

def resume_analysis_prompt(context_string: str, percentage) -> str:
   messages = [
    SystemMessage(content=(
        "You are a resume analyzer. "
        "You will be given resume text which matches the job description. "
        "Similarity percentage will be given between JD and resume so analyze accordingly but remeber this is the best resume among all. "
        "Give brief reasons why this resume has this percent and how this resume is a great fit."
        "Don't behave like a chat model directly give analysis of resume\n\n"
        f"{context_string}"
    )),
    HumanMessage(content=str(percentage))  # Minimal dummy prompt
    ]
   return messages