# broken workspace fixture: missing package.xml

This fixture intentionally contains a ROS2-like package directory without a valid `package.xml`.

Goal:
- test workspace inspection behavior when metadata inventory is incomplete
- support the `missing_package_metadata` broken-case scenario
