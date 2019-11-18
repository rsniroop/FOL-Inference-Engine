import copy

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
        return self

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
        self.newclauses = []

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
                    if predicate.is_negation:
                        self.kb_map["~" + predicate.name] = [sentence_obj]
                    else:
                        self.kb_map[predicate.name] = [sentence_obj]

    def dump_kb(self):
        print("----------------Knowledge Base-------------------")
        print(f"KB : {self.kb_map}")
        print(f"Queries : {self.queries}")
        print("-------------------------------------------------")

    def ask(self, queries):
        query_result = []
        for query in queries:
            query_obj = Sentence(query)
            self.queries.append(query_obj)
            print(f"Querying : {query}")

            query_result.append(self.resolve_query(query_obj, idx))
            print(f"Query result : {query_result[-1]}")
        return query_result

    def resolve_query(self, query_obj, idx):
        result = False

        query_predicate = ~query_obj.predicates[0]

        if not query_predicate:
            return False

        self.newclauses.append(query_predicate)

        resolution_sentences = []

        if query_predicate.is_negation:
            query_name = query_predicate.name
        else:
            query_name = "~" + query_predicate.name

        if query_name in self.kb_map:
            resolution_sentences = self.kb_map[query_name]

        for s in resolution_sentences:
            resolved = self.resolve(query_obj, s)

            if not resolved:
                continue

            if len(self.newclauses) >= idx + 1:
                    self.newclauses[index] = resolved[0]
            else:
                self.newclauses.append(resolved[0])

            result = self.resolve_query(resolved[0], idx + 1)
            if result == True:
                return True

        if result == False:
            return False


    def resolve(self, s1, s2):
        new_sentence = []
        query_predicate = s1.predicates[0]

        if query_predicate.is_negation:
            query_name = query_predicate.name
        else:
            query_name = "~" + query_predicate.name

        for predicate in s2.predicates:
            theta = {}
            self.unify(query_predicate, predicate, theta)
            if 'failure' not in theta:
                print(f"Theta : {theta}")

                new_predicate = self.duplicate_predicate(predicate, s2.predicates[:])
                self.substitute(new_predicate, theta)
                self.substitute(query_predicate, theta)
                new_sentence.extend([new_predicate, query_predicate])

        return new_sentence

    def duplicate_predicate(self, predicate, predicate_list):
            if isinstance(predicate, Predicate):
                new_predicate_list = copy.deepcopy(predicate_list)
                return list(filter(lambda a: a != predicate, new_predicate_list))[0]

    def substitute(self, predicate, theta):
        print(f"New predicate : {predicate}")
        for i in range(len(predicate.args)):
            if predicate.args[i] in theta:
                predicate.args[i] = theta[predicate.args[i]]

    def unify(self, s1, s2, theta):

        if 'failure' in theta:
            return theta

        if s1 == s2:
            return theta
        elif is_variable(s1):
            return self.unify_var(s1, s2, theta)
        elif is_variable(s2):
            return self.unify_var(s2, s1, theta)
        elif isinstance(s1, Predicate) and isinstance(s2, Predicate):
            return self.unify(s1.args, s2.args, self.unify(s1.name, s2.name, theta))
        elif isinstance(s1, list) and isinstance(s2, list):
            return self.unify(s1[1:], s2[1:], self.unify(s1[0], s2[0], theta))
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
