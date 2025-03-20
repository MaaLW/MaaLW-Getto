

def main():
    from app.player.utils import lostword
    print(lostword.isLostwordRunning())
    lostword.adb_address = lostword.adb_address + '1'
    print(lostword.isLostwordRunning())


    return
    from app.utils.image import load_imagefile_as_cvmat, save_cvmat_as_imagefile

    test_file_path = "assets/cache/debug/errand/20250308-100644-2.png"
    cvmat = load_imagefile_as_cvmat(test_file_path)
    print(save_cvmat_as_imagefile(cvmat, "assets/cache/debug/2", "test"))


if __name__ == "__main__":
    main()
