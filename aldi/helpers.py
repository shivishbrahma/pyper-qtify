from PIL import Image
import numpy as np
import tflite_runtime.interpreter as tflite
import matplotlib.pyplot as plt


class AlDiModel():
    def __init__(self, filename) -> None:
        self.filename = filename

        self.interpreter = tflite.Interpreter(model_path=filename)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height, self.width = self.input_details[0]['shape'][1:3]

    def read_labels(self, file_path):
        """
        Helper for loading labels.txt
        """
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            ret = {}
            for line in lines:
                pair = line.strip().split(maxsplit=1)
                ret[int(pair[0])] = pair[1].strip()
        return ret

    def set_input_tensor(self, image):
        tensor_index = self.interpreter.get_input_details()[0]["index"]
        input_tensor = self.interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image

    def classify_image(self, image, top_k=1):
        """Returns a sorted array of classification results."""
        self.set_input_tensor(image)
        self.interpreter.invoke()
        output_details = self.interpreter.get_output_details()[0]
        output = np.squeeze(
            self.interpreter.get_tensor(output_details["index"]))

        # If the model is quantized (uint8 data), then dequantize the results
        if output_details["dtype"] == np.uint8:
            scale, zero_point = output_details["quantization"]
            output = scale * (output - zero_point)

        ordered = np.argpartition(-output, top_k)
        return [(i, output[i]) for i in ordered[:top_k]]

    def recogniseImage(self, image) -> dict:
        resized_image = image.resize((self.width, self.height),
                                     Image.ANTIALIAS).convert('L')

        labels = [str(i) for i in range(10)]
        labels.extend([chr(i) for i in range(65, 91)])

        resized_image = (255 - np.array(resized_image)) / 255
        resized_image = resized_image.reshape(-1, self.width, self.height, 1)

        results = self.classify_image(image=resized_image)

        data = {}
        data['label_id'], data['prob'] = results[0]
        data['label_id'] = labels[data['label_id']]

        return data
