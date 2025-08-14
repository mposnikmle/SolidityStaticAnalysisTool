from solcAST import get_ast

solidity_file_path = "/Users/maximilian/Documents/03_Coding/02_Audits/SolidityStaticAnalysisTool/.venv/lib/python3.9/site-packages/Solidity/HelloWorld.sol"
ast = get_ast(solidity_file_path)


class Node:
    def __init__(self, ast_node): # constructor
        self.node = ast_node # The ast_node we're passing to the __init__ method is just one single dictionary from that entire nested structure, not the whole thing.
        self.nodeType = ast_node.get("nodeType") # We're extracting the nodeType field, which is critical because it tells us what kind of node we're dealing with (e.g., FunctionDefinition, VariableDeclaration, ContractDefinition)
        # and .get() is a python dictionary method

# VariableDeclaration inherits from the Node class.
# It's an "is-a" relationship: a VariableDeclaration is a type of Node.
class VariableDeclaration(Node):
    def __init__(self, ast_node):
        super().__init__(ast_node)
    def get_name(self):
        return self.node.get("name")
    def get_src(self):
        return self.node.get("src")

class ContractDefinition(Node):
    def __init__(self, ast_node):
        super().__init__(ast_node)
    def get_name(self):
        return self.node.get("name")

class FunctionDefinition(Node):
    def __init__(self, ast_node):
        super().__init__(ast_node)
    def get_name(self):
        return self.node.get("name")
    def get_params(self):
        params_node = self.node.get("parameters")
        if params_node:
            # Return a smart ParameterList object
            return ParameterList(params_node)
        return None
    def get_body(self):
        body_node = self.node.get("body")
        if body_node:
            # Return a smart Block object, not the raw dictionary
            return Block(body_node)
        return None

class ParameterList(Node):
    def __init__(self, ast_node):
        super().__init__(ast_node)
    def get_parameters(self):
        # The 'parameters' key holds a list of VariableDeclaration nodes
        param_nodes = self.node.get("parameters", [])
        # Use the factory to turn each raw dictionary into a smart VariableDeclaration object
        return [create_node_object(p) for p in param_nodes]

class SourceUnit(Node):
    def __init__(self, ast_node):
        super().__init__(ast_node)

class PragmaDirective(Node):
    def __init__(self, ast_node):
        super().__init__(ast_node)

class ElementaryTypeName(Node):
    def __init__(self, ast_node):
        super().__init__(ast_node)

class Literal(Node):
    def __init__(self, ast_node):
        super().__init__(ast_node)

class Block(Node):
    def __init__(self, ast_node):
        super().__init__(ast_node)
    def get_statements(self):
        # The 'statements' key in the AST usually holds a list of node dictionaries
        statement_nodes = self.node.get("statements", [])
        # Use your factory to turn each raw dictionary into a smart object
        return [create_node_object(stmt) for stmt in statement_nodes]

class Return(Node):
    def __init__(self, ast_node):
        super().__init__(ast_node)
    def get_expression(self):
        expression_node = self.node.get("expression")
        return create_node_object(expression_node) if expression_node else None

class Identifier(Node):
    def __init__(self, ast_node):
        super().__init__(ast_node)
    def get_name(self):
        return self.node.get("name")
    def get_referenced_declaration(self):
        # This ID is a direct link to the VariableDeclaration node in the AST
        return self.node.get("referencedDeclaration")

class Assignment(Node):
    def __init__(self, ast_node):
        super().__init__(ast_node)
    def get_left_hand_side(self):
        lhs_node = self.node.get("leftHandSide")
        return create_node_object(lhs_node) if lhs_node else None
    def get_right_hand_side(self):
        rhs_node = self.node.get("rightHandSide")
        return create_node_object(rhs_node) if rhs_node else None

class ExpressionStatement(Node):
    def __init__(self, ast_node):
        super().__init__(ast_node)
    def get_expression(self):
        expression_node = self.node.get("expression")
        if expression_node:
            # Return the inner smart object (e.g., an Assignment)
            return create_node_object(expression_node)
        return None

# A dictionary to map AST nodeTypes to our classes
NODE_TYPES = {
    "SourceUnit": SourceUnit,
    "VariableDeclaration": VariableDeclaration,
    "ContractDefinition": ContractDefinition,
    "FunctionDefinition": FunctionDefinition,
    "ParameterList": ParameterList,
    "PragmaDirective": PragmaDirective,
    "ElementaryTypeName": ElementaryTypeName,
    "Literal": Literal,
    "Block": Block,
    "Return": Return,
    "Identifier": Identifier,
    "Assignment": Assignment,
    "ExpressionStatement": ExpressionStatement,
}

# factory pattern
def create_node_object(ast_node):
    node_type_str = ast_node.get("nodeType")
    # Check if we have a specific class for this node type
    node_class = NODE_TYPES.get(node_type_str)

    if node_class:
        # If we do, create an instance of that specific class
        return node_class(ast_node)
    else:
        # If not, fall back to the generic Node class
        return Node(ast_node)
