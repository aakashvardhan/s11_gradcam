import math
from matplotlib import pyplot as plt
import numpy as np

def display_gradcam_output(misclass_data,
                           classes,
                           model,
                           inv_normalize: A.Normalize,
                           target_layers: list['model_layer'],
                           targets=None,
                           no_samples:int = 10,
                           transparence:float = 0.60):
    """
        Function to visualize GradCam output on the data
    :param data: List[Tuple(image, label)]
    :param classes: Name of classes in the dataset
    :param inv_normalize: Mean and Standard deviation values of the dataset
    :param model: Model architecture
    :param target_layers: Layers on which GradCam should be executed
    :param targets: Classes to be focused on for GradCam
    :param number_of_samples: Number of images to print
    :param transparency: Weight of Normal image when mixed with activations
    """

    # Plot configuration
    fig = plt.figure(figsize=(10, 10))
    x_count = 5
    if no_samples is None:
        y_count = 1
    else:
        y_count = math.floor(no_samples / x_count)

    # Create an object for GradCAM
    cam = GradCAM(model=model, target_layers=target_layers,use_cuda=True)

    # Iterate over number of specified images
    for i in range(no_samples):
        plt.subplot(y_count,x_count,i+1)
        input_tensor = misclass_data[i][0]

        # Get the activations of the layer for the images
        grayscale_cam = cam(input_tensor=input_tensor,targets=targets)
        grayscale_cam = grayscale_cam[0,:]



        # Get the original image
        img = input_tensor.squeeze(0).to('cpu')
        img = inv_normalize(img)
        rgb_img = np.transpose(img.cpu().numpy(), [1, 2, 0])

        # mix the normal image with the activations
        visualization = show_cam_on_image(rgb_img, grayscale_cam,use_rgb=True,image_weight=transparence)

        # Plot the GradCAM output along with the original image
        plt.imshow(visualization)
        plt.title("Pred: {} Act: {}".format(classes[misclass_data[i][2].item()],classes[misclass_data[i][1].item()]))
        plt.xticks([])
        plt.yticks([])
    plt.tight_layout()
    plt.show()