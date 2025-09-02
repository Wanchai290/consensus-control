# Formation drawing app

## Usage

| Key                             | Action                       |
|---------------------------------|------------------------------|
| Left-click (on background)      | Create a node                |
| Left-click (on node)            | Drag & drop to new location  |
| Right-click (on node)           | Remove node                  |
| Mouse wheel click (first time)  | Start linking node (A)       |
| Mouse wheel click (second time) | Finish linking node (A -> B) |

Note: arcs created are directed (one-way only)

If you perform the same steps to link node A to node B, the link will be removed.
The application does not support multiple links to the same node.

## Development
The main module is called `drawing_formation.py` and is where the pygame window is created.
It handles mouse & keyboard events, and the logic to interact with the screen

In general, the application is designed to be manipulated with the control functions provided
by each module. Do not attempt to re-create behaviour provided by these functions (for example,
trying to link two nodes without calling `node_handler.link()`) 

### Modules
- `node_handler`
Handles creation, deletion, and linking of nodes. To access all available nodes,
access the field `node_handler.nodes`.


- `node_mover`
When the user left-clicks on an existing node, this module saves the node selected and
updates the node's `is_moving` field accordingly. Once the user releases the left-click button,
the saved node's position is set to the current mouse position.


- `linker`
Handles the mouse wheel click event. This module's functions are called when trying to link a node to another,
by saving the latest node middle-clicked by the user. If this node is not None, a link will be created
(or deleted, if a link was already present).
