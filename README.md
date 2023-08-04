# ManiSkill2 RLDS Dataset

This repo is forked from [RLDS Dataset Builder](https://github.com/kpertsch/rlds_dataset_builder), and contains the ManiSkill2 dataset in RLDS format for X-embodiment experiment integration.

[ManiSkill2](https://github.com/haosulab/ManiSkill2) is a unified benchmark for learning generalizable short-horizon manipulation skills powered by SAPIEN. Currently, the ManiSkill2 RLDS dataset contains the following rigid-body environments from ManiSkill2 with a single-arm fixed-based Panda robot:
- LiftCube-v0
- PickCube-v0
- StackCube-v0
- PlugCharger-v0
- PegInsertionSide-v0
- AssemblingKits-v0
- PickSingleYCB-v0
- PickSingleEGAD-v0
- PickClutterYCB-v0
- TurnFaucet-v0

The definitions and details of these environments can be viewed [in ManiSkill2 Documentation](https://haosulab.github.io/ManiSkill2/concepts/environments.html).

Since the full ManiSkill2 dataset is large (>150G), we have also provided a subset of ManiSkill2 dataset named `mani_skill2_small_dataset`. This smaller dataset contains at most 500 demonstration trajectories per environment and has a total size of 20G.

## More Details on Demonstrations

### Rigid-Body, Single-Arm, Fixed-Base Panda

Rendered RGB-D resolution: 256x256, from a main 3rd-view camera and another camera mounted on the end-effector.

Arm control mode: `arm_pd_base_ee_delta_pose`, i.e., the end-effector delta pose movement recorded in the base frame, with the following controller configuration in `agents/configs/panda/defaults.py` of the ManiSkill2 repo:

```
arm_pd_base_ee_delta_pose = PDEEPoseControllerConfig(
            self.arm_joint_names,
            -0.1,
            0.1,
            0.1,
            self.arm_stiffness,
            self.arm_damping,
            self.arm_force_limit,
            ee_link=self.ee_link_name,
            frame="base",
        )
```

When transforming the demonstrations for X-embodiment training using `example_transform/transform.py`, the demonstration actions (in the range of [-1, 1]) will be mapped to the delta `xyz` movements in meters and the delta `yaw, pitch, roll` movements in radians.

Gripper control mode: `gripper_pd_joint_pos`, i.e., joint position controller.

