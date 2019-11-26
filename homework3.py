import copy
import time

IMPLICATION = "=>"
CONJUNCTION = "&"
NEGATION = "~"

count = 0
start_time = 0

def is_variable(arg):
    """
    " Check if argument is a variable
    " @params arg  string
    " @return Boolean
    """

    return isinstance(arg, str) and arg[:1].isalpha() and arg[:1].islower()

def standardize_variable():
    """
    " Standardize Variable
    " @params None
    " @return string
    """

    global count
    count += 1
    return "x" + str(int(count))

class Predicate:

    def __init__(self, literal):
        self.name = ""
        self.args = []
        self.is_negation = False

        self.parse_literal(literal)

    def __invert__(self):
        self.is_negation = not self.is_negation
        return self

    def __ne__(self, other):

        if self.name != other.name:
            return True

        if self.args != other.args:
            return True

        if (self.is_negation != other.is_negation):
            return True

        return False

    def __eq__(self, other):
        return not self.__ne__(other)

    def parse_literal(self, literal):
        """
        " Parse Literal
        " @params literal string
        " @return None
        """

        if NEGATION in literal:
            self.is_negation = True
            literal = literal.lstrip(NEGATION)

        self.name, args = literal.rstrip(")").split("(")
        self.args = args.strip().split(",")

        self.name = self.name.strip()

        for idx in range(len(self.args)):
            self.args[idx] = self.args[idx].strip()

    def dump_predicate(self):
        """
        " Dump predicate properties
        " @params None
        " @return None
        """
        print(f"\nPredicate : {self.name}")
        print(f"is_neg : {self.is_negation}")
        print(f"args : {self.args}")

class Sentence:

    def __init__(self, sentence_str = None):
        self.predicates = []
        self.premise = []
        self.conclusion = []
        self.old_vars = []
        self.new_vars = []
        self.is_implication = False

        if sentence_str:
            self.create_predicates(sentence_str)

            self.convert_to_cnf()
            self.extract_variables()


    def __eq__(self, other):

        if len(self.predicates) != len(other.predicates):
            return False

        count = 0
        for pred_i in self.predicates:
            for pred_j in other.predicates:
                if pred_i != pred_j:
                    continue
                else:
                    count += 1

        if count == len(self.predicates):
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __contains__(self, predicate):

        for pred_i in self.predicates:
            if pred_i != predicate:
                continue
            else:
                return True

        return False

    def dump_sentences(self):
        """
        " Dump sentences
        " @params None
        " @return None
        """

        for pred in self.predicates:
            pred.dump_predicate()

    def convert_to_cnf(self):
        """
        " Convert sentences to CNF
        " @params None
        " @return None
        """

        # Eliminate Implication
        if self.is_implication:
            for idx in range(len(self.predicates) -1):
                ~self.predicates[idx]

    def extract_variables(self):
        """
        " Extract and standardize variables
        " @params None
        " @return None
        """

        self.var_map = {}

        for idx in range(len(self.predicates)):

            for arg_id, arg in enumerate(self.predicates[idx].args):
                if is_variable(arg):
                    if arg in self.var_map:
                        self.predicates[idx].args[arg_id] = self.var_map[arg]
                    else:
                        new_arg = standardize_variable()
                        self.var_map[self.predicates[idx].args[arg_id]] = new_arg
                        self.predicates[idx].args[arg_id] = new_arg


        
    def create_predicates(self, sentence_str):
        """
        " Create Predicates
        " @params sentence_str string
        " @return None
        """

        if IMPLICATION in sentence_str:
            self.premise, self.conclusion = sentence_str.split(IMPLICATION)
            self.is_implication = True
        else:
            self.premise = sentence_str

        for literal in self.premise.split(CONJUNCTION) + [self.conclusion]:
            if literal:
                predicate_obj = Predicate(literal.strip())          
                self.predicates.append(predicate_obj)


class KnowledgeBase:
    def __init__(self, sentences, queries):
        self.sentences = []
        self.queries = []
        self.kb_map = {}
        self.newclauses = []
        self.query_result = []

        self.timed_out = False

        self.tell(sentences)

        self.ask(queries)

    def tell(self, sentences):
        """
        " Tell KB
        " @params sentences List
        " @return None
        """
        for sentence_str in sentences:
            sentence_obj = Sentence(sentence_str)
            self.sentences.append(sentence_obj)
            for predicate in sentence_obj.predicates:
                pred_name = ""
                if predicate.is_negation:
                    pred_name = "~" + predicate.name
                else:
                    pred_name = predicate.name
                if pred_name in self.kb_map:
                    if sentence_obj not in self.kb_map[pred_name]:
                        self.kb_map[pred_name].append(sentence_obj)
                else:
                    self.kb_map[pred_name] = [sentence_obj]

    def dump_kb(self):
        """
        " Dump KB
        " @params None
        " @return None
        """
        print("----------------Knowledge Base-------------------")
        print(f"KB : {self.kb_map}")
        print(f"Queries : {self.queries}")
        print("-------------------------------------------------")

    def ask(self, queries):
        """
        " Ask KB
        " @params queries List
        " @return None
        """
        self.query_result = []
        for query in queries:
            self.newclauses = []
            query_obj = Sentence(query)
            self.queries.append(query_obj)

            global start_time
            start_time = time.time()
            idx = 1
            path = []
            ~query_obj.predicates[0]
            self.newclauses.append(query_obj)
            indi_result = False
            try:
                indi_result = self.resolve_query(query_obj, path, idx)
            except:
                indi_result = False
            #self.query_result.append(self.resolve_query(query_obj, path, idx)) 
            self.query_result.append(indi_result)

    def is_timed_out(self):
        """
        " Check if resolution is timed out
        " @params None
        " @return None
        """
        if time.time() - start_time > 45:
            self.timed_out = True
            return True
        return False

    def resolve_query(self, query_obj, path, idx):
        """
        " Resolve Query
        " @params query_obj Sentence
        "         path      List
        "         idx       Int
        " @return Boolean
        """
        result = False
        if self.timed_out or self.is_timed_out():
            return False

        if not query_obj or not query_obj.predicates:
            return True

        resolution_sentences = []
    
        if idx > 0:
            path_len = len(path[:idx-1])
            if path_len > 0:
                for i in range(path_len - 1):
                    if path[path_len - 1] == path[i] or path[path_len - 1] == self.newclauses[0]:
                        return False

        for i in range(len(query_obj.predicates)):
            if query_obj.predicates[i].is_negation:
                query_name = query_obj.predicates[i].name
            else:
                query_name = "~" + query_obj.predicates[i].name

            if query_name in self.kb_map:
                resolution_sentences += self.kb_map[query_name]

        if idx > 1:
            resolution_sentences += self.newclauses[:idx]
        for s in resolution_sentences:
            resolved = self.resolve(query_obj, s)

            if not resolved:
                continue

            if len(self.newclauses) >= idx + 1:
                self.newclauses[idx] = resolved[0]
            else:
                self.newclauses.append(resolved[0])

            if len(path) > idx:
                path[idx] = resolved[0]
            else:
                path.append(resolved[0])

            result = self.resolve_query(resolved[0], path, idx + 1)
            if result == True:
                return True

        if result == False:
            return False


    def resolve(self, s1, s2):
        """
        " Resolve two sentences
        " @params s1 Sentence
        "         s2 Sentence
        " @return resolved sentence
        """
        new_sentence = []

        for pred_i in s1.predicates:
            for pred_j in s2.predicates:
                if self.is_valid_pair(pred_i, pred_j):
                    theta = {}
                    self.unify(pred_i, pred_j, theta)
                    if ('failure' not in theta):
                        new_pred_i = self.duplicate_predicate(pred_i, s1.predicates[:])
                        new_pred_j = self.duplicate_predicate(pred_j, s2.predicates[:])
                        self.substitute(new_pred_i, theta)
                        self.substitute(new_pred_j, theta)
                        new_sentence.append(self.create_sentence(new_pred_i, new_pred_j))

        return new_sentence

    def is_valid_pair(self, pred_i, pred_j):
        """
        " Check if two predicates are vaild pair
        " @params pred_i Predicate
        "         pred_j Predicate
        " @return Boolean
        """
        if pred_i.name != pred_j.name:
            return False

        if pred_i.is_negation == pred_j.is_negation:
            return False

        return True

    def duplicate_predicate(self, predicate, predicate_list):
        """
        " Duplicate Predicate
        " @params predicate      Predicate
        "         predicate_list List
        " @return None
        """
        if isinstance(predicate, Predicate):
            new_predicate_list = copy.deepcopy(predicate_list)
            return [ x for x in new_predicate_list if x != predicate]

    def substitute(self, predicate_list, theta):
        """
        " Substitute
        " @params predicate_list List
        "         theta          Dict
        " @return None
        """
        for predicate in predicate_list:
            for i in range(len(predicate.args)):
                if predicate.args[i] in theta:
                    predicate.args[i] = theta[predicate.args[i]]

    def unify(self, s1, s2, theta):
        """
        " Unify Two sentences
        " @params s1    Sentence
        "         s2    Sentence
        :         theta Dict
        " @return None
        """

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

    def unify_var(self, x, y, theta):
        """
        " Unify variables
        " @params x     string
        "         y     string
        "         theta Dict
        " @return None
        """

        if x in theta:
            return self.unify(theta[x], y, theta)
        elif y in theta:
            return self.unify(x, theta[y], theta)
        else:
            if not is_variable(y):
                theta[x] = y
            return theta

    def create_sentence(self, pred_i, pred_j):
        """
        " Create Sentence
        " @params pred_i Predicate
        "         pred_j Predicate
        " @return None
        """

        sentence_obj = Sentence()

        for predicate in pred_i:
            if (predicate is not None) and not (predicate in sentence_obj):
                sentence_obj.predicates.append(predicate)
        for predicate in pred_j:
            if (predicate is not None) and not (predicate in sentence_obj):
                sentence_obj.predicates.append(predicate)

        return sentence_obj

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
    in_file.close()
                 
    my_KB = KnowledgeBase(sentences, queries)

    with open("output.txt", "w+") as out_file :
        out_file.write("\n".join(list(map(str.upper, list(map(str, my_KB.query_result))))))
    out_file.close()
