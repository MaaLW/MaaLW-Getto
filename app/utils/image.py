# For Debug Use

from numpy import ndarray, array

from .logger import logger

default_path = "./assets/cache/debug/getto/default_image/"

try:
    from PIL import Image
except ImportError:
    logger.warning("Pillow is not installed. Image Processing out of Maafw will not work.")
    def cvmat_to_image(cvmat: ndarray) -> None:
        return None
    def save_cvmat_as_imagefile(cvmat, path: str, postfix: str) -> str | None:
        return None
    def image_to_cvmat(image) -> None:
        return None
    def load_imagefile_as_cvmat(path: str) -> ndarray | None:
        return None
else:
    def cvmat_to_image(cvmat: ndarray) -> Image.Image | None:
        pil = Image.fromarray(cvmat)
        b, g, r = pil.split()
        return Image.merge("RGB", (r, g, b))

    def save_cvmat_as_imagefile(cvmat, path: str = default_path, postfix: str = "0") -> str | None:
        from .datetime import datetime
        filename = datetime.now().strftime("%Y%m%d-%H%M%S-") + postfix + ".png"
        from pathlib import Path
        p = Path(path)
        if not p.exists(): p.mkdir(parents=True, exist_ok=True)
        p1 = p.joinpath(filename)
        try: cvmat_to_image(cvmat).save(p1) # cvmat_to_image(cvmat).save(path + filename)
        except: return None
        return str(p1)

    def image_to_cvmat(image: Image.Image) -> ndarray | None:
        r = image.getchannel(0)
        g = image.getchannel(1)
        b = image.getchannel(2)
        new_image = Image.merge("RGB", (b, g, r))
        return array(new_image)
    
    def load_imagefile_as_cvmat(path: str) -> ndarray | None:
        return image_to_cvmat(Image.open(path))
    