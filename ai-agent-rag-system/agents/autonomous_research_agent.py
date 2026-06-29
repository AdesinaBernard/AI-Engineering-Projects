from agents.research_state import ResearchState
from agents.research_planner import generate_research_questions
from agents.research_reporter import generate_research_report
from evaluation.evidence_evaluator import evaluate_evidence
from rag.rag import ask_rag
from agents.evidence_synthesizer import synthesize_evidence


def run_autonomous_research(goal):
    state = ResearchState(goal)

    final_evaluation = {
        "complete": False,
        "confidence": 0,
        "reason": "Not started"
    }

    while state.should_continue():

        print(f"\n[Research Iteration {state.iteration + 1}]")

        questions = generate_research_questions(
            state.goal,
            state.evidence
        )

        if not questions:
            state.finished = True
            break

        for question in questions:
            print(f"Question: {question}")

            raw_context = ask_rag(question)

            answer = synthesize_evidence(
                question,
                raw_context
            )

            print(f"Evidence: {answer}")

            state.add_question(question)

            state.add_evidence({
                "question": question,
                "answer": answer
            })

        final_evaluation = evaluate_evidence(state)

        print(
            f"Evidence Evaluation: "
            f"{final_evaluation['reason']} "
            f"Confidence={final_evaluation['confidence']}%"
        )

        if final_evaluation["complete"]:
            state.finished = True
            break

        state.next_iteration()

    result = {
        "goal": state.goal,
        "iterations": state.iteration + 1,
        "questions": state.questions,
        "evidence": state.evidence,
        "finished": state.finished,
        "confidence": final_evaluation["confidence"],
        "evaluation_reason": final_evaluation["reason"]
    }

    report = generate_research_report(result)

    return {
        "result": result,
        "report": report
    }