import re
from typing import Dict, List, Union
from fasthtml.common import *

def parse_markdown_file(file_path: str) -> Dict[str, str]:
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Split the content into chunks using a delimiter like "## Chunk X"
    chunks = re.split(r'(?=## Chunk \d+)', content)
    
    # Parse chunk numbers and content
    parsed_chunks = {}
    for chunk in chunks:
        if chunk.strip():
            match = re.match(r'## Chunk (\d+)', chunk)
            if match:
                chunk_number = int(match.group(1))
                chunk_content = re.sub(r'## Chunk \d+\n', '', chunk).strip()
                parsed_chunks[chunk_number] = chunk_content
    
    return parsed_chunks

def markdown_to_fasthtml(markdown_content: str, additional_cls: str = "") -> List[FT]:
    components = []
    lines = markdown_content.split('\n')
    
    for line in lines:
        component = parse_line(line, additional_cls)
        if component:
            components.append(component)
    
    return components

def parse_line(line: str, additional_cls: str = "") -> Union[FT, None]:
    line = line.strip()
    if not line:
        return None
    
    parsers = {
        r'^# (.+)': lambda m: H1(*parse_inline(m.group(1)), cls=f"text-3xl font-bold mb-4 text-gray-900 dark:text-white {additional_cls}".strip()),
        r'^## (.+)': lambda m: H2(*parse_inline(m.group(1)), cls=f"text-2xl font-semibold mb-3 text-gray-900 dark:text-white {additional_cls}".strip()),
        r'^### (.+)': lambda m: H3(*parse_inline(m.group(1)), cls=f"text-xl font-semibold mb-2 text-gray-900 dark:text-white {additional_cls}".strip()),
        r'^!\[(.+)\]\((.+)\)': lambda m: Img(src=m.group(2), alt=m.group(1), cls=f"mb-4 max-w-full h-auto {additional_cls}".strip()),
        r'^- (.+)': lambda m: Li(*parse_inline(m.group(1)), cls=f"mb-2 {additional_cls}".strip()),
    }
    
    for pattern, parser in parsers.items():
        match = re.match(pattern, line)
        if match:
            return parser(match)
    
    return P(*parse_inline(line), cls=f"mb-4 text-gray-700 dark:text-gray-300 {additional_cls}".strip())

def parse_inline(text: str) -> List[Union[str, FT]]:
    parts = []
    current_text = ""

    def append_current_text():
        nonlocal current_text
        if current_text:
            parts.append(current_text)
            current_text = ""

    i = 0
    while i < len(text):
        if text[i:i+2] == '**':
            append_current_text()
            end = text.find('**', i+2)
            if end != -1:
                parts.append(Strong(text[i+2:end]))
                i = end + 2
            else:
                current_text += '**'
                i += 2
        elif text[i] == '*':
            append_current_text()
            end = text.find('*', i+1)
            if end != -1:
                parts.append(Em(text[i+1:end]))
                i = end + 1
            else:
                current_text += '*'
                i += 1
        else:
            current_text += text[i]
            i += 1

    append_current_text()
    return parts
