from typing import Any, Dict
import numpy as np
from PIL import Image
from transforms3d.euler import axangle2euler


################################################################################################
#                                        Target config                                         #
################################################################################################
# features=tfds.features.FeaturesDict({
#     'steps': tfds.features.Dataset({
#         'observation': tfds.features.FeaturesDict({
#             'image': tfds.features.Image(
#                 shape=(128, 128, 3),
#                 dtype=np.uint8,
#                 encoding_format='jpeg',
#                 doc='Main camera RGB observation.',
#             ),
#         }),
#         'action': tfds.features.Tensor(
#             shape=(8,),
#             dtype=np.float32,
#             doc='Robot action, consists of [3x EEF position, '
#                 '3x EEF orientation yaw/pitch/roll, 1x gripper open/close position, '
#                 '1x terminate episode].',
#         ),
#         'discount': tfds.features.Scalar(
#             dtype=np.float32,
#             doc='Discount if provided, default to 1.'
#         ),
#         'reward': tfds.features.Scalar(
#             dtype=np.float32,
#             doc='Reward if provided, 1 on final step for demos.'
#         ),
#         'is_first': tfds.features.Scalar(
#             dtype=np.bool_,
#             doc='True on first step of the episode.'
#         ),
#         'is_last': tfds.features.Scalar(
#             dtype=np.bool_,
#             doc='True on last step of the episode.'
#         ),
#         'is_terminal': tfds.features.Scalar(
#             dtype=np.bool_,
#             doc='True on last step of the episode if it is a terminal step, True for demos.'
#         ),
#         'language_instruction': tfds.features.Text(
#             doc='Language Instruction.'
#         ),
#         'language_embedding': tfds.features.Tensor(
#             shape=(512,),
#             dtype=np.float32,
#             doc='Kona language embedding. '
#                 'See https://tfhub.dev/google/universal-sentence-encoder-large/5'
#         ),
#     })
################################################################################################
#                                                                                              #
################################################################################################


def transform_step(step: Dict[str, Any]) -> Dict[str, Any]:
    """Maps step from source dataset to target dataset config.
       Input is dict of numpy arrays."""
    img = Image.fromarray(step['observation']['image']).resize(
        (128, 128), Image.Resampling.LANCZOS)
    action_translation = step['action'][:3] * 0.1 # actual translation in meters
    action_axis_angle = step['action'][3:6] * 0.1
    action_axis_angle_norm = np.linalg.norm(action_axis_angle)
    action_axis = action_axis_angle / (action_axis_angle_norm + 1e-8)
    action_angle = action_axis_angle_norm # actual angle in radians
    # print(action_translation, action_axis_angle, action_axis, action_angle)
    transformed_step = {
        'observation': {
            'image': np.array(img),
        },
        'action': np.concatenate(
            [action_translation,
             np.array(axangle2euler(action_axis, action_angle, axes='szyx')) if action_axis_angle_norm > 1e-4 else np.zeros(3), # yaw, pitch, roll
             # step['action'][3:6] * np.pi, 
             np.clip(step['action'][-1:], -1, 1),
             np.array([step['is_terminal']], dtype=np.float32)]).astype(np.float32),
    }

    # copy over all other fields unchanged
    for copy_key in ['discount', 'reward', 'is_first', 'is_last', 'is_terminal',
                     'language_instruction', 'language_embedding']:
        transformed_step[copy_key] = step[copy_key]

    return transformed_step

