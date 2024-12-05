from dataclasses import dataclass

@dataclass
class Rule:
    def __init__(self, page_to_print: int, required_pages: list[int],):
        self.page_to_print = page_to_print
        self.required_pages = required_pages

    def add_required_page(self, page: int):
        self.required_pages.append(page)

def parse_input(data):

    page_ordering_rules, pages_to_print = data.split("\n\n")

    page_ordering_rules = [tuple(map(int, rule.split("|"))) for rule in page_ordering_rules.splitlines()]
    
    # Create a dictionary of rules which are relevant for each page
    rule_dict = dict()
    for rule in page_ordering_rules:
        if rule[1] not in rule_dict:
            rule_dict[rule[1]] = Rule(rule[1], [rule[0]])
        else:
            rule_dict[rule[1]].add_required_page(rule[0])

    pages_to_print = [list(map(int, row.split(","))) for row in pages_to_print.splitlines()]

    return rule_dict, pages_to_print

def check_order_and_reorder(pages, rule_dict, reorder=False):
    i = 0
    while i < len(pages):
        relevant_rules = rule_dict.get(pages[i], None)
        
        # Check whether the relevant rules are satisfied
        alread_printed_pages = set(pages[:i])
        if relevant_rules is not None:
            required_pages = set([p for p in relevant_rules.required_pages if p in pages])
            if not required_pages.issubset(alread_printed_pages):
                if reorder:
                    new_pages = pages.copy()
                    for page in required_pages - alread_printed_pages:
                        new_pages.remove(page)
                    for page in required_pages - alread_printed_pages:
                        new_pages.insert(i, page)
                    _, new_pages = check_order_and_reorder(new_pages, rule_dict, reorder)
                    return False, new_pages
                else:
                    return False, pages
        i += 1
    return True, pages

def part1(data):
    rule_dict, pages_to_print = parse_input(data)

    middle_page_sum = 0

    for pages in pages_to_print:
        
        page_order_is_correct, _ = check_order_and_reorder(pages, rule_dict)

        if page_order_is_correct:
            middle_page_sum += pages[len(pages) // 2]

    return middle_page_sum

def part2(data):
    rule_dict, pages_to_print = parse_input(data)

    middle_page_sum = 0

    for pages in pages_to_print:
        original_page_order_is_correct, new_page_order = check_order_and_reorder(pages, rule_dict, reorder=True)

        if not original_page_order_is_correct:
            middle_page_sum += new_page_order[len(new_page_order) // 2]

    return middle_page_sum