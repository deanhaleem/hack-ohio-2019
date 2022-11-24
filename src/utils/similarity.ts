import { cv } from "opencv-wasm";

export function similarityScore(
  inputImagePath: string,
  comparingImagesPath: string
) {
  let image = cv.imread(inputImagePath);
  image = cv.resize(image, 500, 500);

  return image;
}
