

IMPLICATION = "=>"
CONJUNCTION = "&"
NEGATION = "~"

class Predicate:

    def __init__(self, literal):
        self.name = ""
        self.args = []
        self.is_negation = False

        self.parse_literal(literal)

        print(f"Predicate : {self.name}")
        print(f"is_neg : {self.is_negation}")
        print(f"args : {self.args}")

    def parse_literal(self, literal):

        if NEGATION in literal:
            self.is_negation = True
            literal = literal.lstrip(NEGATION)

        print(f"Literal : {literal}")
        self.name, args = literal.rstrip(")").split("(")
        self.args = args.split(",")

class Sentence:

    def __init__(self, sentence_str):
        self.predicates = []
        self.premise = []
        self.conclusion = []

        self.create_predicates(sentence_str)

    def create_predicates(self, sentence_str):

        if IMPLICATION in sentence_str:
            self.premise, self.conclusion = sentence_str.split(IMPLICATION)
        else:
            self.premise = sentence_str

        print(f"Premise : {self.premise}")
        print(f"conclusion : {self.conclusion}")

        for literal in self.premise.split(CONJUNCTION) + [self.conclusion]:
            if literal:
                print(f"Literal  : {literal}")          
                self.predicates.append(Predicate(literal.strip()))
            
        

class KnowledgeBase:
    def __init__(self, sentences, queries):
        self.sentences = []
        self.queries = queries
        print(self.sentences)
        print(f"queries : {self.queries}")

        self.create_sentences(sentences)

    def create_sentences(self, sentences):

        for sentence_str in sentences:
            self.sentences.append(Sentence(sentence_str))


if __name__ == "__main__":
    in_list = None
    with open("input.txt", "r") as in_file:
        in_list = in_file.readlines()
        idx = 1
        queries = []
        for i in range(int(in_list[0].strip("\n"))):
            queries.append(in_list[idx].strip("\n"))
            idx += 1

        n_sentences = int(in_list[idx].strip("\n"))
        idx += 1
        sentences = []
        for i in range(n_sentences):
            sentences.append(in_list[idx].strip("\n"))
            idx += 1
            
            
    KnowledgeBase(sentences, queries)
