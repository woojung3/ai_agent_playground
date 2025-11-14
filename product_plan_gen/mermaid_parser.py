import re
import json

class MermaidParser:
    @staticmethod
    def parse(mermaid_content: str):
        """
        Parses a mermaid flowchart to extract structured data using a two-pass approach.
        It handles multiple flowchart sections separated by markdown headers.
        """
        sections = re.split(r'(^## .*)', mermaid_content, flags=re.MULTILINE)
        parsed_data = []

        # This pattern finds nodes, which can have forms like:
        # ID, ID(Label), ID[Label], ID:::type, ID(Label):::type
        node_pattern = re.compile(r'([a-zA-Z0-9_]+)(?:[\(\[]([^\]\)]+)[\)\]])?(?::+([a-zA-Z_]+))?')

        for i in range(1, len(sections), 2):
            title = sections[i].strip().replace('## ', '')
            content = sections[i+1]

            if 'flowchart' not in content:
                continue

            nodes_map = {}
            edges = []
            lines = content.strip().split('\n')

            # 1st Pass: Find all nodes defined anywhere.
            for line in lines:
                line = line.strip()
                if not line or line.startswith('%%') or line.startswith('flowchart') or line.startswith('classDef'):
                    continue
                
                # Find all node-like structures in the line
                found_nodes = node_pattern.findall(line)
                for node_id, label, node_type in found_nodes:
                    # Add or update the node in the map. This ensures we capture all of them
                    # and avoid duplicates.
                    if node_id and node_id not in nodes_map:
                         nodes_map[node_id] = {
                            "id": node_id,
                            "label": label.strip() if label else '',
                            "type": node_type.strip() if node_type else 'event'
                        }

            # 2nd Pass: Find all edges.
            for line in lines:
                line = line.strip()
                if '-->' in line:
                    # To correctly parse edges, we remove the labels and types, leaving only IDs and arrows.
                    # Example: A(Label) --> B[Label]:::type becomes A --> B
                    cleaned_line = re.sub(r'[\(\[].*?[\)\]]', '', line) # Remove labels
                    cleaned_line = re.sub(r':::\w+', '', cleaned_line)    # Remove types

                    parts = [p.strip() for p in cleaned_line.split('-->')]
                    for j in range(len(parts) - 1):
                        source_id = parts[j]
                        target_id = parts[j+1]
                        if source_id and target_id:
                            edges.append({"source": source_id, "target": target_id})

            parsed_data.append({
                "title": title,
                "nodes": list(nodes_map.values()),
                "edges": edges
            })

        return parsed_data

if __name__ == '__main__':
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sample_file = os.path.join(script_dir, 'samples', 'mermaid_flowchart.md')

    with open(sample_file, 'r', encoding='utf-8') as f:
        sample_mermaid = f.read()
    
    parsed = MermaidParser.parse(sample_mermaid)
    print(json.dumps(parsed, indent=2, ensure_ascii=False))
