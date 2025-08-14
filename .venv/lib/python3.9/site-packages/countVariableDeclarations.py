from traverseAST import create_node_object, ast, VariableDeclaration

def traverse_and_count_declarations(node):
    count = 0

    # First, create our smart object from the raw dictionary
    current_object = create_node_object(node)

    # Use isinstance to check if it's a VariableDeclaration
    if isinstance(current_object, VariableDeclaration):
        count += 1
        print(f"Found variable: {current_object.get_name()}")
        print(f"src: {current_object.get_src()}")

    # Find all children of the current node to continue the traversal
    children = []
    for key, value in node.items():
        if isinstance(value, dict):
            children.append(value)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    children.append(item)

    # Recursively call the function on all children
    for child in children:
        count += traverse_and_count_declarations(child)

    return count

# How this is working:
# traverse_and_count_declarations function is initially called on the top-level, outermost dictionary which has the key "nodeType": "SourceUnit"
#

if ast:
    print("Successfully received the AST. Starting traversal...")

    declaration_count = traverse_and_count_declarations(ast)
    print(f"\nNumber of VariableDeclaration nodes found: {declaration_count}")

else:
    print("Failed to get the AST. Check the logs for details.")