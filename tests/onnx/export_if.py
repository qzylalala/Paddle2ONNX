import onnx
import numpy as np
from base_expect import expect

if __name__ == "__main__":
    # Given a bool scalar input cond.
    # return constant tensor x if cond is True, otherwise return constant tensor y.

    then_out = onnx.helper.make_tensor_value_info(
        "then_out", onnx.TensorProto.FLOAT, [5]
    )
    else_out = onnx.helper.make_tensor_value_info(
        "else_out", onnx.TensorProto.FLOAT, [5]
    )

    x = np.array([1, 2, 3, 4, 5]).astype(np.float32)
    y = np.array([5, 4, 3, 2, 1]).astype(np.float32)

    then_const_node = onnx.helper.make_node(
        "Constant",
        inputs=[],
        outputs=["then_out"],
        value=onnx.numpy_helper.from_array(x),
    )

    else_const_node = onnx.helper.make_node(
        "Constant",
        inputs=[],
        outputs=["else_out"],
        value=onnx.numpy_helper.from_array(y),
    )

    then_body = onnx.helper.make_graph(
        [then_const_node], "then_body", [], [then_out]
    )

    else_body = onnx.helper.make_graph(
        [else_const_node], "else_body", [], [else_out]
    )

    if_node = onnx.helper.make_node(
        "If",
        inputs=["cond"],
        outputs=["res"],
        then_branch=then_body,
        else_branch=else_body,
    )

    cond = np.array(1).astype(bool)
    res = x if cond else y
    expect(
        if_node,
        inputs=[cond],
        outputs=[res],
        name="test_if",
        opset_imports=[onnx.helper.make_opsetid("", 11)],
    )