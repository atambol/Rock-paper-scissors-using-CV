import imgaug as ia
from imgaug import augmenters as iaa
from os import listdir
from os.path import isfile, join, isdir
import imageio
import shutil
import numpy as np

inputDir = "./inputImages"
outputDir = "./augmentedImages"
gestures = ["Rock", "Paper", "Scissors"]

# Transformation functions
rotations = [
    [iaa.Affine(
        rotate=(0, 0),
    )],
    [iaa.Affine(
        rotate=(-30, 30),
    )],
    [iaa.Affine(
        rotate=(-60, 60),
    )],
    [iaa.Affine(
        rotate=(-90, 90),
    )],
    [iaa.Affine(
        rotate=(-120, 120),
    )],
    [iaa.Affine(
        rotate=(-150, 150),
    )],
    [iaa.Affine(
        rotate=(-15, 15),
    )],
    [iaa.Affine(
        rotate=(-45, 45),
    )],
    [iaa.Affine(
        rotate=(-75, 75),
    )],
    [iaa.Affine(
        rotate=(-105, 105),
    )],
    [iaa.Affine(
        rotate=(-135, 135),
    )],
    [iaa.Affine(
        rotate=(-165, 165),
    )],
    [iaa.Affine(
        rotate=(-180, 180),
    )]
]

shears = [
    [iaa.Affine(
        shear=(-8, 8),
    )],
    [iaa.Affine(
        shear=(-16, 16),
    )],
    [iaa.Affine(
        shear=(-24, 24),
    )],
    # [iaa.Affine(
    #     shear=(-30, 30),
    # )],
    # [iaa.Affine(
    #     shear=(-36, 36),
    # )],
    # [iaa.Affine(
    #     shear=(-42, 42),
    # )],
    # # [iaa.Affine(
    #     shear=(-48, 48),
    # )],
    # [iaa.Affine(
    #     shear=(-54, 54),
    # )],
    # [iaa.Affine(
    #     shear=(-60, 60),
    # )],
    # [iaa.Affine(
    #     shear=(-66, 66),
    # )],
    # [iaa.Affine(
    #     shear=(-72, 72),
    # )],
    # [iaa.Affine(
    #     shear=(-78, 78),
    # )]
]

flip = [iaa.Fliplr(1)]

crop = [iaa.Crop(percent=(0, 0.2))]

scale = [iaa.Affine(
        scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
        translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
    )]

# otherTransformations = [
#     iaa.Crop(percent=(0, 0.2)), 
    # iaa.GaussianBlur(sigma=(0, 0.5)),
    # iaa.ContrastNormalization((0.75, 1.5)),
    # iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5),
    # iaa.Multiply((0.8, 1.2), per_channel=0.2),
#     iaa.Affine(
#         scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
#         translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
#     ),
# ]

# Read images from the inputDir as black and white
def readImages():
    print("Reading input images")
    allImages = {}

    for gesture in gestures:
        Dir = join(inputDir, gesture)
        images = []
        for f in listdir(Dir):
            filepath = join(Dir, f)
            if isfile(filepath) and '.DS_Store' not in filepath:
                print("Reading {}".format(filepath))
                # Load in grayscale
                bw = imageio.imread(filepath, pilmode="L")
                # Convert to black and white
                bw[bw < 128] = 0
                bw[bw >= 128] = 255 
                images.append(bw)
        allImages[gesture] = images

    return allImages

# Write images after transformations
def writeImages(augImages):
    print("Writing images")
    if isdir(outputDir):
        shutil.rmtree(outputDir)
    shutil.copytree(inputDir, outputDir)
    total = 0
    for gesture in gestures:
        count = 0
        for image in augImages[gesture]:
            imageio.imwrite(join(outputDir, gesture, '{}.jpg'.format(count)), image)
            count += 1
        total += count
    print("Created {} augmented images".format(total))

# Perform transformations on the image based on the functions above
def transformImages(images):
    print("Transforming images")     
    ia.seed(1)

    augImages = {}
    for gesture in gestures:
        augImages[gesture] = []
        # Rotate the images
        for rotation in rotations:
            seq = iaa.Sequential(rotation, random_order=True)
            augImages[gesture].extend(seq.augment_images(images[gesture]))

        # shear images      
        # for shear in shears:
        #     seq = iaa.Sequential(shear, random_order=True)
        #     augImages[gesture].extend(seq.augment_images(augImages[gesture]))

        # flip images
        seq = iaa.Sequential(flip, random_order=True)
        augImages[gesture].extend(seq.augment_images(augImages[gesture]))

        # Crop images
        seq = iaa.Sequential(crop, random_order=True)
        augImages[gesture].extend(seq.augment_images(augImages[gesture]))

        # scale images
        seq = iaa.Sequential(scale, random_order=True)
        augImages[gesture].extend(seq.augment_images(augImages[gesture]))
    return augImages

# main
def main():
    images = readImages()
    augImages = transformImages(images)
    writeImages(augImages)

main()