class ResearchState:

    def __init__(self, goal):

        self.goal = goal
        self.questions = []

        self.evidence = []

        self.iteration = 0

        self.finished = False

        self.max_iterations = 5

    def add_question(self, question):

        self.questions.append(question)

    def add_evidence(self, evidence):

        self.evidence.append(evidence)

    def next_iteration(self):

        self.iteration += 1

    def should_continue(self):

        return (
            not self.finished
            and
            self.iteration < self.max_iterations
        )