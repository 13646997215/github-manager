# broken case: missing launch params

## Scenario
A launch file exists, but a required parameter YAML file is missing.

## Expected diagnosis direction
- params_file_missing
- verify launch assets
- do not assume Gazebo/TF/controller is the first root cause
