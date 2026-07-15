from agents.research_state import ResearchState
from agents.research_planner import generate_research_questions
from agents.research_reporter import generate_research_report
from agents.evidence_synthesizer import synthesize_evidence

from evaluation.evidence_evaluator import evaluate_evidence
from rag.rag import ask_rag
from app.logging_config import logger


def run_autonomous_research(goal):
    logger.info("Autonomous research started | goal=%s", goal)

    state = ResearchState(goal)

    final_evaluation = {
        "complete": False,
        "confidence": 0,
        "reason": "Not started"
    }

    try:
        while state.should_continue():
            iteration_number = state.iteration + 1

            print(f"\n[Research Iteration {iteration_number}]")

            logger.info(
                "Research iteration started | goal=%s | iteration=%s",
                goal,
                iteration_number
            )

            questions = generate_research_questions(
                state.goal,
                state.evidence
            )

            if not questions:
                logger.warning(
                    "No research questions generated | goal=%s | iteration=%s",
                    goal,
                    iteration_number
                )

                state.finished = True
                break

            for question in questions:
                print(f"Question: {question}")

                logger.info(
                    "Research question generated | goal=%s | question=%s",
                    goal,
                    question
                )

                try:
                    raw_context = ask_rag(question)

                    logger.info(
                        "RAG retrieval completed | question=%s",
                        question
                    )

                    answer = synthesize_evidence(
                        question,
                        raw_context
                    )

                    print(f"Evidence: {answer}")

                    logger.info(
                        "Evidence synthesis completed | question=%s",
                        question
                    )

                    state.add_question(question)

                    state.add_evidence({
                        "question": question,
                        "answer": answer
                    })

                except Exception:
                    logger.exception(
                        "Research question failed | goal=%s | question=%s",
                        goal,
                        question
                    )

                    state.add_question(question)

                    state.add_evidence({
                        "question": question,
                        "answer": (
                            "I could not complete this research question "
                            "because an internal error occurred."
                        )
                    })

            final_evaluation = evaluate_evidence(state)

            print(
                f"Evidence Evaluation: "
                f"{final_evaluation['reason']} "
                f"Confidence={final_evaluation['confidence']}%"
            )

            logger.info(
                "Evidence evaluated | goal=%s | confidence=%s | complete=%s | reason=%s",
                goal,
                final_evaluation["confidence"],
                final_evaluation["complete"],
                final_evaluation["reason"]
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

        logger.info(
            "Autonomous research completed | goal=%s | iterations=%s | confidence=%s",
            goal,
            result["iterations"],
            result["confidence"]
        )

        return {
            "result": result,
            "report": report
        }

    except Exception as error:
        logger.exception(
            "Autonomous research failed | goal=%s",
            goal
        )

        return {
            "result": {
                "goal": goal,
                "iterations": state.iteration,
                "questions": state.questions,
                "evidence": state.evidence,
                "finished": False,
                "confidence": final_evaluation["confidence"],
                "evaluation_reason": str(error)
            },
            "report": (
                "Autonomous research failed because an internal "
                f"error occurred: {error}"
            )
        }