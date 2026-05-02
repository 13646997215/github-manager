# Runbook: TF + Controller 联动故障

## 场景背景
机器人 bringup 后控制器未激活，同时导航相关 TF 链不完整。

## 初始症状
- controller inactive
- 上层功能无法正常运动/定位
- TF chain 缺失

## 执行命令
- ros2 control list_controllers
- ros2 control list_hardware_interfaces
- ros2 run tf2_tools view_frames

## 关键输出
- arm_controller inactive 4 6
- 缺少 map->odom->base_link chain

## 证据解释
controller 与 TF 同时异常时，优先处理 controller manager 与接口导出，再确认 TF 发布链。

## 排除路径
- 若 controller active，则优先排查 TF publisher
- 若 TF 正常，则优先排查 ros2_control 配置/接口

## 修复动作
- inspect_controller_manager_logs
- verify_hardware_interface_exports
- inspect_tf_publishers

## 修复后验证
- controller active
- map->odom->base_link chain restored

## 常见误判点
- 只盯 TF，不看 controller manager
- 把空 consumer/topic 误当作 TF 根因
