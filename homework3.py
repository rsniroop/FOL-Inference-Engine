

IMPLICATION = "=>"
CONJUNCTION = "&"
NEGATION = "~"

args_seen_list = set()
count = 0

def is_variable(arg):

    return isinstance(arg, str) and arg[:1].isalpha() and arg[:1].islower()

def standardize_variable():

    global count
    count += 1
    return "x" + str(int(count))

def standardize():

    for arg_idx in range(len(self.args)):
        if self.is_variable(self.args[arg_idx]):
            if self.args[arg_idx] not in args_seen_list:
                args_seen_list.add(self.args[arg_idx])
            else:
                self.args[arg_idx] = self.standardize_variable(self.args[arg_idx])
                args_seen_list.add(self.args[arg_idx])
class Predicate:

    def __init__(self, literal):
        self.name = ""
        self.args = []
        self.is_negation = False

        self.parse_literal(literal)
        #self.standardize()

    def __invert__(self):
        self.is_negation = not self.is_negation

    def parse_literal(self, literal):

        if NEGATION in literal:
            self.is_negation = True
            literal = literal.lstrip(NEGATION)

        self.name, args = literal.rstrip(")").split("(")
        self.args = args.split(",")

    def dump_predicate(self):
        print(f"\nPredicate : {self.name}")
        print(f"is_neg : {self.is_negation}")
        print(f"args : {self.args}")

class Sentence:

    def __init__(self, sentence_str):
        self.predicates = []
        self.premise = []
        self.conclusion = []
        self.old_vars = []
        self.new_vars = []
        self.is_implication = False

        self.create_predicates(sentence_str)

        self.convert_to_cnf()
        self.extract_variables()


        self.dump_sentences()

    def dump_sentences(self):

        for pred in self.predicates:
            pred.dump_predicate()

    def convert_to_cnf(self):

        # Eliminate Implication
        if self.is_implication:
            for idx in range(len(self.predicates) -1):
                ~self.predicates[idx]

        #distribute and over or??

    def extract_variables(self):

        self.var_map = {}

        for idx in range(len(self.predicates)):

            for arg_id, arg in enumerate(self.predicates[idx].args):
                #print(f"Arg : {arg}")
                if is_variable(arg):
                    if arg in self.var_map:
                        self.predicates[idx].args[arg_id] = self.var_map[arg]
                    else:
                        new_arg = standardize_variable()
                        self.var_map[self.predicates[idx].args[arg_id]] = new_arg
                        self.predicates[idx].args[arg_id] = new_arg


        
    def create_predicates(self, sentence_str):

        if IMPLICATION in sentence_str:
            self.premise, self.conclusion = sentence_str.split(IMPLICATION)
            self.is_implication = True
        else:
            self.premise = sentence_str

        for literal in self.premise.split(CONJUNCTION) + [self.conclusion]:
            if literal:
                #print(f"Literal  : {literal}")
                predicate_obj = Predicate(literal.strip())          
                self.predicates.append(predicate_obj)

    def parse_predicates(self, predicate_obj, literal):

        self.predicate_obj.name, args = literal.rstrip(")").split("(")
        self.predicate_obj.args = args.split(",")


class KnowledgeBase:
    def __init__(self, sentences, queries):
        self.sentences = []
        self.queries = []
        self.kb_map = {}

        self.tell(sentences)

        self.ask(queries)
        self.dump_kb()

    def tell(self, sentences):

        for sentence_str in sentences:
            sentence_obj = Sentence(sentence_str)
            self.sentences.append(sentence_obj)
            for predicate in sentence_obj.predicates:
                if predicate.name in self.kb_map:
                    if sentence_obj not in self.kb_map[predicate.name]:
                        self.kb_map[predicate.name].append(sentence_obj)
                else:
                    self.kb_map[predicate.name] = [sentence_obj]

    def dump_kb(self):
        print("----------------Knowledge Base-------------------")
        print(f"KB : {self.kb_map}")
        print(f"Queries : {self.queries}")
        print("-------------------------------------------------")

    def ask(self, queries):

        for query in queries:
            query_obj = Sentence(query)
            self.queries.append(query_obj)

            self.resolve_query(query_obj)

    def resolve_query(self, query_obj):
        pass

    def unify(self, s1, s2, theta):

        if 'failure' in theta:
            return theta

        if s1 == s2:
            return theta
        elif is_variable(s_1):
            return self.unify_var(s_1, s_2, theta)
        elif is_variable(s_2):
            return self.unify_var(s_2, s_1, theta)
        elif isinstance(s_1, Predicate) and isinstance(s_2, Predicate):
            return self.unify(s_1.args, s_2.args, self.unify(s_1.name, s_2.name, theta))
        elif isinstance(s_1, list) and isinstance(s_2, list):
            return self.unify(s_1[1:], s_2[1:], self.unify(s_1[0], s_2[0], theta))
        else:
            theta['failure'] = 1
            return theta

    def unify_var(self, var_1, s_2, theta):

        if var_1 in theta:
            return self.unify(theta[var_1], s_2, theta)
        elif s_2 in theta:
            return self.unify(var_1, theta[s_2], theta)
        else:
            theta[var_1] = s_2
            return theta

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
