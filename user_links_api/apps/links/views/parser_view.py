from parsel import SelectorList, Selector


class SelectorListF(SelectorList):
    def extract(self):
        return self.getall()

    def extract_first(self, default=None) -> str:
        return self.get(default=default)

def xpath(text: str, query: str, is_regex: bool = False) -> SelectorListF:
    if is_regex:
        namespaces = {"re": "http://exslt.org/regular-expressions"}
    else:
        namespaces = {}
    return Selector(text=text).xpath(query=query, namespaces=namespaces)