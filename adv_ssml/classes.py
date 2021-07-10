from _typeshed import StrPath
from typing import Union, List
from ssml_exceptions import NoBreakStrengthOrTimeGiven



class Element():
    """Everything, excluding speech. Convertable"""
    
class Speech():
    """Main object. Convertable"""
    __tag = "speak"
    def __init__(self, elements: List[Element, str]):
        self.__elements = list()
    
    def compile(self):
        start_tag = "<{self.__tag}>"
        end_tag = "</{self.__tag}>"
        data = ""
        for element in self.__elements:
            data += element.compile() if not isinstance(element, str) else element
        return f"""{start_tag}\n{data}\n{end_tag}"""


class NotContainerElement(Element):
    """Container for breaks, audios, etc. Convertable"""


class Container(Element):
    __tag = ""
    """Container for any of data. Convertable"""

    def __init__(self, elements: List[Element, str]):
        self.__elements = list(elements)

    def compile(self):
        start_tag = f"<{self.__tag}>"
        end_tag = f"</{self.__tag}>"
        data = ""
        for element in self.__elements:
            data += element.compile() if not isinstance(element, str) else element
        return "{start_tag}\n{data}\n{end_tag}"

class OnlyStrContainer(Container):
    __tag = ""
    """Defines element with container, which supports only text as input"""

    def __init__(self, elements: List[str]):
        self.__elements = list(elements)

    def compile(self):
        start_tag = '<{self.__elements}>'
        end_tag = '</{self.__elements}>'
        return f"{start_tag}\n{''.join(self.__elements)}\n{end_tag}"



class Break(NotContainerElement):
    """Defines break timing"""
    __tag = "break"
    def __init__(self, **kwargs):
        self.__strength = kwargs.get('strength', None)
        if not self.__strength:
            self.__time = kwargs.get('time', None)
            if self.__time:
                raise NoBreakStrengthOrTimeGiven

    def compile(self):
        return """<{self.__tag} {'strength="' + str(self.__strength) + '"' if self.__strength != None else ""} {'time="' + str(self.__time) + '"' if self.__time != None else ""} />\n"""


class Paragraph(Container):
    """Makes diffrence by pauses"""
    __tag = "p"


class Sentence(Container):
    """Container for sentences, can contain sen"""
    __tag = "s"

class Emphasis(Container):
    """Makes text inside it being pronounced in another way."""
    __tag = "emphasis"
    def __init__(self, text: List[OnlyStrContainer, NotContainerElement, str], emphs):
        self.__elements = list(text)
        self.__emphs = emphs

    def compile(self):
        start_tag = f"<{self.__tag} level='{self.__emphs}'>"
        end_tag = f"</{self.__tag}>"
        data = ""
        for element in self.__elements:
            data += element.compile() if not isinstance(element, str) else element
        return f"""{start_tag}\n{data}\n{end_tag}"""

class Sub(OnlyStrContainer):
    """Defines the pronounciation of sth. like """
    def __init__(self, text: List[str], alias):
        self.__elements = list(text)
        self.__alias = alias

    def compile(self):
        start_tag = f'<{self.__tag} alias={self.__alias}>'
        end_tag = f'</{self.__tag}>'

        return f"{start_tag}\n{''.join(self.__text)}\n{end_tag}"

class Audio(OnlyStrContainer):
    __tag = "audio"
    """Defines element, which can contain nothing as text, but will play audio. Very useful."""
    def __init__(self, text: Union[List[str], None], src: str):
        self.__elements = list(text) if text != None else None
        self.__src = src

    def compile(self):
        if not self.__elements:
            start_tag = f'<{self.__tag} src="{self.__src}">'
            end_tag = f'</{self.__tag}>'
            tag = f"{start_tag}\n{''.join(self.__elements)}\n{end_tag}"
