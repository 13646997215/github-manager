# broken case: missing workspace package metadata

## Scenario
A workspace has a src directory, but package metadata is incomplete or absent.

## Expected diagnosis direction
- workspace has no valid package.xml inventory
- repair_workspace
- do not proceed directly to build
