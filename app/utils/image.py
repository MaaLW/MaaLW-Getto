# For Debug Use
from typing import Optional

from numpy import ndarray, array

from .logger import logger

try:
    from PIL import Image
except ImportError:
    logger.warning("Pillow is not installed. Image Processing out of Maafw will not work.")
    def cvmat_to_image(cvmat: ndarray) -> None:
        return None
    def save_cvmat_as_imagefile(cvmat, path: str, postfix: str) -> Optional[str]:
        return None
    def image_to_cvmat(image) -> None:
        return None
    def load_imagefile_as_cvmat(path: str) -> Optional[ndarray]:
        return None
else:
    def cvmat_to_image(cvmat: ndarray) -> Optional[Image.Image]:
        pil = Image.fromarray(cvmat)
        b, g, r = pil.split()
        return Image.merge("RGB", (r, g, b))

    def save_cvmat_as_imagefile(cvmat, path: str, postfix: str) -> Optional[str]:
        from .datetime import datetime
        filename = datetime.now().strftime("%Y%m%d-%H%M%S-") + postfix + ".png"
        from pathlib import Path
        p = Path(path)
        if not p.exists(): p.mkdir(parents=True, exist_ok=True)
        p1 = p.joinpath(filename)
        try: cvmat_to_image(cvmat).save(p1) # cvmat_to_image(cvmat).save(path + filename)
        except: return None
        return str(p1)

    def image_to_cvmat(image: Image.Image) -> Optional[ndarray]:
        r, g, b = image.split()
        new_image = Image.merge("RGB", (b, g, r))
        return array(new_image)
    
    def load_imagefile_as_cvmat(path: str) -> Optional[ndarray]:
        return image_to_cvmat(Image.open(path))
    