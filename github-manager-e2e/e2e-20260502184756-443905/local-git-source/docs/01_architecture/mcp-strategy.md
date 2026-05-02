# ROS2-Agent MCP Strategy

## Why MCP matters

MCP is the future bridge between ROS2-Agent and external robotics systems, services, and datasets.

## Planned connection directions

1. Simulation backends
   - Gazebo / Ignition / Isaac-related service wrappers
2. Experiment and training systems
   - run tracking / artifact stores / evaluation services
3. Repository and CI services
   - GitHub / issue tracking / regression dashboards
4. Lab infrastructure
   - internal APIs for task queues, reservation systems, device status

## Repository plan

- `mcp/servers/` for planned local MCP service definitions
- `mcp/connectors/` for integration design notes and future adapters

## Principle

Do not overbuild MCP on day one.
First define the interfaces and integration strategy, then connect the highest-value systems.
