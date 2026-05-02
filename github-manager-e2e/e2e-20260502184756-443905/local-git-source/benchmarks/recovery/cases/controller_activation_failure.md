# Recovery Case: controller activation failure

broken_state:
- controller inactive
- required interfaces > claimed interfaces

suggested_fix:
- inspect controller manager logs
- verify hardware interface exports

verification:
- controller becomes active
- claimed interfaces satisfy required interfaces
